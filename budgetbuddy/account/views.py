from django.shortcuts import render, get_object_or_404
from django.views import View
from .forms import *
from django.db.models import Sum
from .models import Transaction, Account
from django.contrib.auth.models import User
from account.models import *
from django.db.models import *
from django.core.paginator import Paginator
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta

# Create your views here.
class HomeView(View):
    def get(self, request):
        user_pk = request.user.pk
        user_accounts = request.user.account_set.all()
        user = User.objects.get(pk=user_pk)
        selected_account_id = request.GET.get('account', None)
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
        graph_total_income = [float(income['total_income']) for income in six_month_income]
        # Query รายจ่ายในแต่ละเดือน
        six_month_expense = (
            Transaction.objects
            .filter(account__in=user_accounts, create_at__gte=six_months_ago, transaction_type='expense')
            .annotate(month=TruncMonth('create_at'))
            .values('month')
            .annotate(total_expense=Sum('amount'))
            .order_by('month')
        )
        graph_total_expense = [float(expense['total_expense']) for expense in six_month_expense]
        
        six_month_income_avg = (
            Transaction.objects
            .filter(account__in=user_accounts, create_at__gte=six_months_ago, transaction_type='income')
            .aggregate(average_income=Avg('amount'))
        )
        
        six_month_expense_avg = (
            Transaction.objects
            .filter(account__in=user_accounts, create_at__gte=six_months_ago, transaction_type='expense')
            .aggregate(average_expense=Avg('amount'))
        )
        
        current_month_income_sum = (
            Transaction.objects
            .filter(account__in=user_accounts, create_at__month=datetime.now().month, create_at__year=datetime.now().year, transaction_type='income')
            .aggregate(sum_income=Sum('amount'))
        )
        
        current_month_expense_sum = (
            Transaction.objects
            .filter(account__in=user_accounts, create_at__month=datetime.now().month, create_at__year=datetime.now().year, transaction_type='expense')
            .aggregate(sum_expense=Sum('amount'))
        )
        
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
            'current_month_expense_sum': current_month_expense_sum
        }
        return render(request, 'test.html', context)

#budget zone view
class BudgetView(View):
    def get(self, request):
        return render(request, 'budget/budget.html')

class AddBudgetView(View):
    def get(self, request):
        form = BudgetForm()
        return render(request, 'budget/addBudget.html', {"form": form})

class EditBudgetView(View):
    def get(self, request, budget_id):
        budget = Budget.objects.get(id=budget_id)
        form = BudgetForm(instance=budget)

        form = BudgetForm()
        return render(request, 'budget/editBudget.html', {"form": form})

# class AddBudgetView(View):
#     def get(self, request):
#         form = AddBudgetForm()
#         return render(request, 'budget/addBudget.html', {"form": form})
    
# class EditBudgetView(View):
#     def get(self, request):
#     # def get(self, request, budget_id):
#         # budget = Budget.objects.get(id=budget_id)
#         # form = EditBudgetForm(instance=budget)
        
#         form = EditBudgetForm()
#         return render(request, 'budget/editBudget.html', {"form": form})


#saving zone view
class SavingView(View):
    def get(self, request):
        return render(request, 'saving/saving.html')

class AddSavingView(View):
    def get(self, request):
        form = AddSavingForm()
        return render(request, 'saving/addSaving.html', {"form": form})

#account zone view
class AccountView(View):
    def get(self, request):
        accounts = Account.objects.all()
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
            lastestDate = Transaction.objects.order_by('-create_at').first()
            if lastestDate is None:
                account.lastest = account.create_at
            else:
                account.lastest = lastestDate
        return render(request, 'account/account.html', {"accounts": accounts})

class AddAccountView(View):
    def get(self, request):
        form = AddAccountForm()
        return render(request, 'account/addAccount.html', {"form": form})

#notify zone view
class NotifyView(View):
    def get(self, request):
        return render(request, 'notify.html')

