from .forms import *
from account.models import *
from django.db.models import *
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from django.utils import timezone
from .notifications import Notify
from django.contrib import messages
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

#Opens up page as PDF
class ViewPDF(LoginRequiredMixin, View):
    login_url = "/authen/"
    def render_to_pdf(self, template_src, context_dict={}):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None
    
    def get(self, request, *args, **kwargs):
        user_pk = request.user.pk
        user_accounts = request.user.account_set.all()
        user = User.objects.get(pk=user_pk)
        month_report = request.GET.get('month-report')
    
        if month_report:
            # แยก year และ month ออกจากค่า month-report
            year, month = map(int, month_report.split('-'))
        else:
            # ถ้าไม่มีค่า month-report ใช้ค่า year และ month ปัจจุบัน
            year = timezone.now().year
            month = timezone.now().month

        # แปลงปีและเดือนให้เป็น integer
        year = int(year)
        month = int(month)

        if month < 1 or month > 12:
            return HttpResponse("Invalid month", status=400)

        # คำนวณยอดรวมรายรับของเดือนที่เลือก
        total_income_current = Transaction.objects.filter(
            account__in=user_accounts,
            create_at__year=year,
            create_at__month=month,
            transaction_type='income'
        ).aggregate(sum_income=Sum('amount'))['sum_income'] or 0
        
        # คำนวณยอดรวมรายจ่ายของเดือนที่เลือก
        total_expense_current = Transaction.objects.filter(
            account__in=user_accounts,
            create_at__year=year,
            create_at__month=month,
            transaction_type='expense'
        ).aggregate(sum_expense=Sum('amount'))['sum_expense'] or 0

        this_month_income = []
        
        # ถ้ามีรายรับ คำนวณรายรับต่อหมวดหมู่
        if total_income_current > 0:
            this_month_income = Transaction.objects.filter(
                account__in=user_accounts,
                create_at__year=year,
                create_at__month=month,
                transaction_type='income'
            ).values('category__name').annotate(
                total_income=Sum('amount')
            ).annotate(
                income_percent=(F('total_income') / total_income_current) * 100
            ).order_by('income_percent')

        this_month_expense = []
        
        # ถ้ามีรายจ่าย คำนวณรายจ่ายต่อหมวดหมู่
        if total_expense_current > 0:
            this_month_expense = Transaction.objects.filter(
                account__in=user_accounts,
                create_at__year=year,
                create_at__month=month,
                transaction_type='expense'
            ).values('category__name').annotate(
                total_expense=Sum('amount')
            ).annotate(
                expense_percent=(F('total_expense') / total_expense_current) * 100
            ).order_by('expense_percent')

        context = {
            'user': user,
            'create_at': timezone.now(),  # ใช้เวลาปัจจุบันสำหรับการสร้าง PDF
            'this_month_income': this_month_income,
            'this_month_expense': this_month_expense,
            'total_income_current': total_income_current,
            'total_expense_current': total_expense_current,
            'selected_year': year,
            'selected_month': month,
        }
        
        # สร้าง PDF
        pdf = self.render_to_pdf('pdf/monthlyreport.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html', {
            'request': request,
            'path': request.path
        })

class HomeView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def ensure_six_elements(self, data_list):
        # ตรวจสอบว่า list มีสมาชิกครบ 6 ตัวมั้ย
        while len(data_list) < 6:
            data_list.insert(0, 0.0) 
        return data_list
    
    def get(self, request):
        user_pk = request.user.pk
        user_accounts = request.user.account_set.all()
        user = User.objects.get(pk=user_pk)
        selected_account_id = request.GET.get('account', 'all')
        
        #check get account id กัน user ดูข้อมูลคนอื่น
        user_account_ids = [key.id for key in user_accounts]
        if selected_account_id != 'all' and int(selected_account_id) not in user_account_ids:
            selected_account_id = 'all'

        print(selected_account_id)
        # คำนวณรายรับรายจ่ายรวมของ user
        user_income = Transaction.objects.filter(account__in=user_accounts, transaction_type='income').aggregate(total_income=Sum('amount'))
        user_expense = Transaction.objects.filter(account__in=user_accounts, transaction_type='expense').aggregate(total_expense=Sum('amount'))
        total_income = user_income['total_income'] or 0
        total_expense = user_expense['total_expense'] or 0
        
        # คำนวณจำนวน savingGoals และ Budget ที่ user ได้สร้างเอาไว้
        user_savinggoals = SavingsGoal.objects.filter(user_id=user_pk).aggregate(count_saving=Count('id'))
        user_budget = Budget.objects.filter(user_id=user_pk).aggregate(count_budget=Count('id'))
        total_savinggoals = user_savinggoals['count_saving'] or 0
        total_budget = user_budget['count_budget'] or 0
        
        # query transaction ของ user นี้ตาม selected account
        if selected_account_id == 'all':
            user_transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-create_at', '-transaction_type')
        elif selected_account_id:
            user_transactions = Transaction.objects.filter(account_id=selected_account_id).order_by('-create_at', '-transaction_type')
        else:
            user_transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-create_at', '-transaction_type')
        paginator = Paginator(user_transactions, 6)
        page_number = request.GET.get('page')
        transactions_list = paginator.get_page(page_number)
        
        # ทำส่วนของกราฟเส้น
        # คำนวณช่วง 6 เดือนที่ผ่านมา
        six_months_ago = datetime.now() - timedelta(days=6*30)

        # Query รายรับในแต่ละเดือน
        six_month_income = (
            Transaction.objects
            .filter(account__in=user_accounts, create_at__gte=six_months_ago, transaction_type='income')
            .annotate(month=TruncMonth('create_at'))
            .values('month')
            .annotate(total_income=Sum('amount'))
            .order_by('month')
        )
        graph_total_income = self.ensure_six_elements([float(income['total_income']) for income in six_month_income])
        print(six_month_income)
        # Query รายจ่ายในแต่ละเดือน
        six_month_expense = (
            Transaction.objects
            .filter(account__in=user_accounts, create_at__gte=six_months_ago, transaction_type='expense')
            .annotate(month=TruncMonth('create_at'))
            .values('month')
            .annotate(total_expense=Sum('amount'))
            .order_by('month')
        )
        graph_total_expense = self.ensure_six_elements([float(expense['total_expense']) for expense in six_month_expense])
        
        six_month_expense_avg = (
            Transaction.objects
            .filter(account__in=user_accounts, create_at__gte=six_months_ago, transaction_type='expense')
            .annotate(month=TruncMonth('create_at'))
            .values('month')
            .annotate(total_expense=Sum('amount'))
            .aggregate(average_expense=Avg('total_expense'))
        )
        
        six_month_income_avg = (
            Transaction.objects
            .filter(account__in=user_accounts, create_at__gte=six_months_ago, transaction_type='income')
            .annotate(month=TruncMonth('create_at'))
            .values('month')
            .annotate(total_income=Sum('amount'))
            .aggregate(average_income=Avg('total_income'))
        )
        
        #ส่วนของกราฟโดนัท
        current_month_income_sum = (
            Transaction.objects
            .filter(account__in=user_accounts, create_at__month=datetime.now().month, create_at__year=datetime.now().year, transaction_type='income')
            .aggregate(sum_income=Sum('amount'))
        )
        if current_month_income_sum['sum_income'] is None:
            current_month_income_sum['sum_income'] = 0
        
        current_month_expense_sum = (
            Transaction.objects
            .filter(account__in=user_accounts, create_at__month=datetime.now().month, create_at__year=datetime.now().year, transaction_type='expense')
            .aggregate(sum_expense=Sum('amount'))
        )
        if current_month_expense_sum['sum_expense'] is None:
            current_month_expense_sum['sum_expense'] = 0

        context = {
            'user': user,
            'total_income': total_income,
            'total_expense': total_expense,
            'total_savinggoals': total_savinggoals,
            'total_budget': total_budget,
            'user_transactions': transactions_list,
            'user_accounts': user_accounts,
            'income_data': graph_total_income,
            'expense_data': graph_total_expense,
            'six_month_expense_avg': six_month_expense_avg,
            'six_month_income_avg': six_month_income_avg,
            'current_month_income_sum': current_month_income_sum,
            'current_month_expense_sum': current_month_expense_sum,
            'selected_account_id': selected_account_id,
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            'path': request.path
        }
        return render(request, 'home.html', context)

#report zone view
class TransactionView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        categories = Category.objects.all()
        tags = Tag.objects.all()
        
        search_description = request.GET.get('search', '')
        search_date = request.GET.get('searchdate')
        selected_category_id = request.GET.get('category')
        selected_account_id = request.GET.get('account')
        selected_transaction_type = request.GET.get('transactiontype')
        selected_tag_id = request.GET.get('tag')
        
        transactions = Transaction.objects.filter(account__in=accounts).order_by('-create_at')
        
        if search_description:
            transactions = transactions.filter(
                Q(description__icontains=search_description) |
                Q(category__name__icontains=search_description) |
                Q(tags__name__icontains=search_description)
            )
        if search_date:
            transactions = transactions.filter(create_at__date=search_date)
        if selected_category_id:
            transactions = transactions.filter(category_id=selected_category_id)
        if selected_tag_id:
            transactions = transactions.filter(tags=selected_tag_id)
        if selected_account_id:
            transactions = transactions.filter(account_id=selected_account_id)
        if selected_transaction_type:
            transactions = transactions.filter(transaction_type=selected_transaction_type)
    
        paginator = Paginator(transactions, 10)
        page_number = request.GET.get('page')
        transactions_list = paginator.get_page(page_number)
        income = Transaction.objects.filter(account__in = accounts, create_at__day=datetime.now().day, transaction_type="income").aggregate(daily=Sum("amount"))
        expense = Transaction.objects.filter(account__in = accounts, create_at__day=datetime.now().day, transaction_type="expense").aggregate(daily=Sum("amount"))
        return render(request, 'transaction/transactions.html', {
            "transactions": transactions_list,
            "dailyIncome": income['daily'],
            "dailyExpense": expense['daily'],
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path,
            "user_accounts": accounts,
            "categories": categories,
            "tags": tags,
            "selected_category_id": selected_category_id,
            "selected_account_id": selected_account_id,
            "selected_transaction_type": selected_transaction_type,
            "selected_tag_id": selected_tag_id
        })
    
    def delete(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(pk=transaction_id)
            if (transaction.description.startswith("Saving to ")) and (transaction.transaction_type=="expense") and (transaction.category.name=="SavingGoals"):
                saving = SavingsGoal.objects.get(user=request.user, name=transaction.description.split(" ")[-1])
                saving.current_amount -= transaction.amount
                saving.save()
            transaction.delete()
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 500})

class AddTransactionView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request):
        initial_data = {
            'description': request.GET.get('description', ''),
            'transaction_type': request.GET.get('transaction_type', ''),
            'category': request.GET.get('category', '')
        }
        form = TransactionForm(user=request.user, initial=initial_data)
        return render(request, 'transaction/transactionForm.html', {
            "form": form,
            "tag": "Add",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })
    
    def post(self, request):
        initial_data = {
            'description': request.GET.get('description', ''),
            'transaction_type': request.GET.get('transaction_type', ''),
            'category': request.GET.get('category', '')
        }
        form = TransactionForm(request.POST, user=request.user, initial=initial_data)
        if form.is_valid():
            try:
                with transaction.atomic():
                    newTransaction = form.save()
                    if newTransaction.description.startswith("Saving to") and newTransaction.category.name == "SavingGoals":
                        name = newTransaction.description.replace("Saving to ", "")
                        saving = SavingsGoal.objects.get(name=name, user=request.user)
                        saving.current_amount += newTransaction.amount
                        saving.save()
                        notification = Notify(transaction=newTransaction, saving=saving, user=request.user)
                    else:
                        notification = Notify(transaction=newTransaction, user=request.user)
                    notification.execute()
                    return redirect("/account/transaction/")
            except ObjectDoesNotExist:
                messages.error(request, "Saving Not Found")
                return render(request, 'transaction/transactionForm.html', {
                    "form": form,
                    "tag": "Edit",
                    "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
                    "path": request.path
                    })
            except Exception as e:
                messages.error(request, "Something went wrong during registration. Please try again.")
                return render(request, 'transaction/transactionForm.html', {
                    "form": form,
                    "tag": "Edit",
                    "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
                    "path": request.path
                    })
        return render(request, 'transaction/transactionForm.html', {
            "form": form,
            "tag": "Add",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

class EditTransactionView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request, transaction_id):
        transaction = Transaction.objects.get(pk=transaction_id)
        initial_data = {
            'description': transaction.description,
            'transaction_type': transaction.transaction_type,
            'category': transaction.category
        }
        form = TransactionForm(instance=transaction, user=request.user, initial=initial_data)
        return render(request, 'transaction/transactionForm.html', {
            "form": form,
            "tag": "Edit",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })
    
    def post(self, request, transaction_id):
        newTransaction = Transaction.objects.get(pk=transaction_id)
        old_amount = newTransaction.amount
        initial_data = {
            'description': newTransaction.description,
            'transaction_type': newTransaction.transaction_type,
            'category': newTransaction.category
        }
        form = TransactionForm(request.POST, instance=newTransaction, user=request.user, initial=initial_data)
        if form.is_valid():
            try:
                with transaction.atomic():
                    updateTransaction = form.save()
                    if updateTransaction.description.startswith("Saving to") and updateTransaction.category.name == "SavingGoals":
                        name = updateTransaction.description.replace("Saving to ", "")
                        saving = SavingsGoal.objects.get(name=name, user=request.user)
                        saving.current_amount -= old_amount
                        saving.current_amount += updateTransaction.amount
                        saving.save()
                        notification = Notify(transaction=newTransaction, saving=saving, user=request.user)
                    else:
                        notification = Notify(transaction=newTransaction, user=request.user)
                    notification.execute()
                    return redirect("/account/transaction/")
            except ObjectDoesNotExist:
                messages.error(request, "Saving Not Found")
                return render(request, 'transaction/transactionForm.html', {
                    "form": form,
                    "tag": "Edit",
                    "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
                    "path": request.path
                    })
            except Exception as e:
                messages.error(request, "Something went wrong during registration. Please try again.")
                return render(request, 'transaction/transactionForm.html', {
                    "form": form,
                    "tag": "Edit",
                    "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
                    "path": request.path
                    })

        return render(request, 'transaction/transactionForm.html', {
            "form": form,
            "tag": "Edit",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

#budget zone view
class BudgetView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request):
        budgets = Budget.objects.filter(user=request.user)
        for budget in budgets:
            user_accounts = request.user.account_set.all()
            transaction = Transaction.objects.filter(category=budget.category, account__in=user_accounts, create_at__month=datetime.now().month, transaction_type='expense').aggregate(expense=Sum("amount"))
            if transaction['expense'] is None:
                budget.expense = 0
            else:
                budget.expense = transaction['expense']
        return render(request, 'budget/budget.html', {
            "budgets": budgets,
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
        })
    
    def delete(self, request, budget_id):
        try:
            budget = Budget.objects.get(pk=budget_id)
            budget.delete()
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 500})

class AddBudgetView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request):
        form = BudgetForm(user=request.user)
        return render(request, 'budget/budgetForm.html', {
            "form": form,
            "tag": "Add",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
        })

    def post(self, request):
        form = BudgetForm(request.POST, user=request.user)
        
        if form.is_valid():
            Budget.objects.create(category=form.cleaned_data['category'], amount=form.cleaned_data['amount'], user=request.user)
            return redirect("/account/budget/")
        
        return render(request, 'budget/budgetForm.html',{
            "form": form,
            "tag": "Add",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

class EditBudgetView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request, budget_id):
        budget = Budget.objects.get(id=budget_id)
        form = BudgetForm(instance=budget)

        return render(request, 'budget/budgetForm.html', {
            "form": form,
            "tag": "Edit",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

    def post(self, request, budget_id):
        budget = Budget.objects.get(id=budget_id)
        form = BudgetForm(request.POST, instance=budget)
        
        if form.is_valid():
            form.save()
            return redirect("/account/budget/")
        
        return render(request, 'budget/budgetForm.html', {
            "form": form,
            "tag": "Edit",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

#saving zone view
class SavingView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request):
        savings = SavingsGoal.objects.filter(user=request.user)
        for saving in savings:
            saving.percent = (saving.current_amount/saving.target_amount)*100

        return render(request, 'saving/saving.html', {
            "savings": savings,
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
        })
    
    def delete(self, request, saving_id):
        try:
            saving = SavingsGoal.objects.get(pk=saving_id)
            saving.delete()
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 500})

class AddSavingView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request):
        form = SavingForm(user=request.user)
        return render(request, 'saving/savingForm.html', {
            "form": form,
            "tag": "Add",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })
    
    def post(self, request):
        form = SavingForm(request.POST, user=request.user)

        if form.is_valid():
            SavingsGoal.objects.create(user=request.user, **form.cleaned_data)
            return redirect("/account/saving/")

        return render(request, 'saving/savingForm.html', {
            "form": form,
            "tag": "Add",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

class EditSavingView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request, saving_id):
        saving = SavingsGoal.objects.get(pk=saving_id)
        form = SavingForm(instance=saving, user=request.user)
        return render(request, 'saving/savingForm.html', {
            "form": form,
            "tag": "Add",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })
    
    def post(self, request, saving_id):
        saving = SavingsGoal.objects.get(pk=saving_id)
        form = SavingForm(request.POST, instance=saving, user=request.user)

        if form.is_valid():
            form.save()
            return redirect("/account/saving/")

        return render(request, 'saving/savingForm.html', {
            "form": form,
            "tag": "Add",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

#account zone view
class AccountView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        for account in accounts:
            income = Transaction.objects.filter(account=account, transaction_type="income").aggregate(income=Sum("amount"))
            expense = Transaction.objects.filter(account=account, transaction_type="expense").aggregate(expense=Sum("amount"))
            if income['income'] is None:
                income = 0
            else:
                income = income['income']
            if expense['expense'] is None:
                expense = 0
            else:
                expense = expense['expense']
            account.balance = income-expense
            lastestDate = Transaction.objects.filter(account=account).order_by('-create_at').first()
            if lastestDate is None:
                account.lastest = account.create_at
            else:
                account.lastest = lastestDate.create_at
        return render(request, 'account/account.html', {
            "accounts": accounts,
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

    def delete(self, request, account_id):
        try:
            account = Account.objects.get(pk=account_id)
            account.delete()
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 500})

class AddAccountView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request):
        form = AccountForm(user=request.user)
        return render(request, 'account/accountForm.html', {
            "form": form,
            "tag": "Add",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

    def post(self, request):
        form = AccountForm(request.POST, user=request.user)
        
        if form.is_valid():
            Account.objects.create(name=form.cleaned_data['name'], user=request.user)
            return redirect("/account/account")
        
        return render(request, 'account/accountForm.html', {
            "form": form,
            "tag": "Add",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

class EditAccountView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request, account_id):
        account = Account.objects.get(pk=account_id)
        form = AccountForm(instance=account, user=request.user)
        return render(request, 'account/accountForm.html', {
            "form": form,
            "tag": "Edit",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

    def post(self, request, account_id):
        account = Account.objects.get(pk=account_id)
        form = AccountForm(request.POST, instance=account, user=request.user)
        
        if form.is_valid():
            form.save()
            return redirect("/account/account")
        
        return render(request, 'account/accountForm.html', {
            "form": form,
            "tag": "Edit",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })


#notify zone view
class NotifyView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request):
        # อัปเดต is_read เป็น True สำหรับ notifications ที่ยังไม่ได้อ่าน
        Notification.objects.filter(user=request.user).update(is_read=True)
    
        notifications = Notification.objects.filter(user=request.user, is_delete=False).order_by('-notification_date')
        for notification in notifications:
            notification.name = (notification.message.split(" "))[1]
        return render(request, 'notify.html', {
            "notifications": notifications,
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
        })

    def delete(self, request, notification_id):
        try:
            notification = Notification.objects.get(pk=notification_id)
            notification.is_delete = True
            notification.save()
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 500})

class EditProfileView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request):
        user = request.user
        form = EditProfileForm()
        context = {
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            'path': request.path,
            'user': user,
            'form': form
        }
        return render(request, 'setting/editprofile.html', context)

    def post(self, request):
        user = request.user
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('edit-profile')
        context = {
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            'path': request.path,
            'user': user,
            'form': form
        }
        return render(request, 'setting/editprofile.html', context)

class ResetPassWordView(LoginRequiredMixin, View):
    login_url = "/authen/"
    def get(self, request):
        user = request.user
        form = ResetPasswordForm()
        context = {
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            'path': request.path,
            'form': form,
            'user': user
        }
        return render(request, 'setting/resetpassword.html', context)
    
    def post(self, request):
        user = request.user
        form = ResetPasswordForm(request.POST, instance=user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            request.user.set_password(new_password)
            request.user.save()
            login(request, request.user)
            messages.success(request, "Reset password successfully!")
            return redirect('edit-profile')
        context = {
                "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
                'path': request.path,
                'user': user,
                'form': form
            }
        return render(request, 'setting/resetpassword.html', context)



#developer zone view
## categories
class CategoriesDevView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/authen/"
    permission_required = ["category.view_category"]
    def get(self, request):
        categories = Category.objects.all()
        paginator = Paginator(categories, 10)
        page_number = request.GET.get('page')
        categories_list = paginator.get_page(page_number)
        return render(request, 'developer/categories.html', {
            "categories": categories_list,
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
        })

    def delete(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
            category.delete()
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 500})
    
class AddCategoriesDevView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/authen/"
    permission_required = ["category.add_category"]
    def get(self, request):
        form = CategoryDevForm()
        return render(request, 'developer/categoriesForm.html', {
            "form": form,
            "tag": "Add",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })
    
    def post(self, request):
        form = CategoryDevForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("/account/developer/categories/")
        
        return render(request, 'developer/categoriesForm.html', {
            "form": form,
            "tag": "Add",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

class EditCategoriesDevView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/authen/"
    permission_required = ["category.change_category"]
    def get(self, request, category_id):
        category = Category.objects.get(pk=category_id)
        form = CategoryDevForm(instance=category)
        return render(request, 'developer/categoriesForm.html', {
            "form": form,
            "tag": "Edit",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })
    
    def post(self, request, category_id):
        category = Category.objects.get(pk=category_id)
        form = CategoryDevForm(request.POST, instance=category)
        
        if form.is_valid():
            form.save()
            return redirect("/account/developer/categories/")
        
        return render(request, 'developer/categoriesForm.html', {
            "form": form,
            "tag": "Edit",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

## tags
class TagsDevView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/authen/"
    permission_required = ["tag.view_tag"]
    def get(self, request):
        tags = Tag.objects.all()
        paginator = Paginator(tags, 10)
        page_number = request.GET.get('page')
        tags_list = paginator.get_page(page_number)
        return render(request, 'developer/tags.html', {
            "tags": tags_list,
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

    def delete(self, request, tag_id):
        try:
            tag = Tag.objects.get(pk=tag_id)
            tag.delete()
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 500})
    
class AddTagsDevView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/authen/"
    permission_required = ["tag.add_tag"]
    def get(self, request):
        form = TagDevForm()
        return render(request, 'developer/tagsForm.html',{
            "form": form,
            "tag": "Add",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })
    
    def post(self, request):
        form = TagDevForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("/account/developer/tags/")
        
        return render(request, 'developer/tagsForm.html',{
            "form": form,
            "tag": "Add",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

class EditTagsDevView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/authen/"
    permission_required = ["tag.change_tag"]
    def get(self, request, tag_id):
        tag = Tag.objects.get(pk=tag_id)
        form = TagDevForm(instance=tag)
        return render(request, 'developer/tagsForm.html',{
            "form": form,
            "tag": "Edit",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })
    
    def post(self, request, tag_id):
        tag = Tag.objects.get(pk=tag_id)
        form = TagDevForm(request.POST, instance=tag)
        
        if form.is_valid():
            form.save()
            return redirect("/account/developer/tags/")
        
        return render(request, 'developer/tagsForm.html',{
            "form": form,
            "tag": "Edit",
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

class StaffDevView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "/authen/"
    permission_required = ["category.view_category", "tag.view_tag"]
    def get(self, request):
        group = Group.objects.get(name='staff')
        staffs = group.user_set.all()
        users = User.objects.exclude(groups=group)
        return render(request, 'developer/staff.html', {
            "staffs": staffs,
            "users": users,
            "numNotify": Notification.objects.filter(user=request.user, is_read=False).count(),
            "path": request.path
            })

    def post(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            group = Group.objects.get(name='staff')
            group.user_set.add(user)
            return JsonResponse({"status": 200})
        except User.DoesNotExist:
            return JsonResponse({"status": 404, "message": "User not found."})
        except Group.DoesNotExist:
            return JsonResponse({"status": 404, "message": "Group not found."})
        except Exception as e:
            # Handle any other exceptions
            return JsonResponse({"status": 500, "message": str(e)})
        
    def delete(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            group = Group.objects.get(name='staff')
            user.groups.remove(group)
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 500})
