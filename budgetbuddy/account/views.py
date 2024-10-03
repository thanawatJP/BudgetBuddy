from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.db.models import Sum
from .models import Transaction, Account, Tag, Category

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'test.html')


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


#saving zone view
class SavingView(View):
    def get(self, request):
        return render(request, 'saving/saving.html')

class AddSavingView(View):
    def get(self, request):
        form = SavingForm()
        return render(request, 'saving/addSaving.html', {"form": form})

#account zone view
class AccountView(View):
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
            lastestDate = Transaction.objects.order_by('-create_at').first()
            if lastestDate is None:
                account.lastest = account.create_at
            else:
                account.lastest = lastestDate
        return render(request, 'account/account.html', {"accounts": accounts})

    def delete(self, request, account_id):
        try:
            account = Account.objects.get(pk=account_id)
            account.delete()
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 500})

class AddAccountView(View):
    def get(self, request):
        form = AccountForm()
        return render(request, 'account/accountForm.html', {
            "form": form,
            "tag": "Add New Account"}
        )

    def post(self, request):
        form = AccountForm(request.POST)
        
        if form.is_valid():
            Account.objects.create(name=form.cleaned_data['name'], user=request.user)
            return redirect("/account/account")
        
        return render(request, 'account/accountForm.html', {
            "form": form,
            "tag": "Add New Account"}
        )

class EditAccountView(View):
    def get(self, request, account_id):
        account = Account.objects.get(pk=account_id)
        form = AccountForm(instance=account)
        return render(request, 'account/accountForm.html', {
            "form": form,
            "tag": "Edit Account"}
        )

    def post(self, request, account_id):
        account = Account.objects.get(pk=account_id)
        form = AccountForm(request.POST, instance=account)
        
        if form.is_valid():
            form.save()
            return redirect("/account/account")
        
        return render(request, 'account/accountForm.html', {
            "form": form,
            "tag": "Edit Account"}
        )


#notify zone view
class NotifyView(View):
    def get(self, request):
        return render(request, 'notify.html')



#developer zone view
## categories
class CategoriesDevView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'developer/categories.html', {"categories": categories})

    def delete(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
            category.delete()
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 500})
    
class AddCategoriesDevView(View):
    def get(self, request):
        form = CategoryDevForm()
        return render(request, 'developer/categoriesForm.html', {
            "form": form,
            "tag": "Add"}
        )
    
    def post(self, request):
        form = CategoryDevForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("/account/developer/categories/")
        
        return render(request, 'developer/categoriesForm.html', {
            "form": form,
            "tag": "Add"}
        )

class EditCategoriesDevView(View):
    def get(self, request, category_id):
        category = Category.objects.get(pk=category_id)
        form = CategoryDevForm(instance=category)
        return render(request, 'developer/categoriesForm.html', {
            "form": form,
            "tag": "Edit"}
        )
    
    def post(self, request, category_id):
        category = Category.objects.get(pk=category_id)
        form = CategoryDevForm(request.POST, instance=category)
        
        if form.is_valid():
            form.save()
            return redirect("/account/developer/categories/")
        
        return render(request, 'developer/categoriesForm.html', {
            "form": form,
            "tag": "Edit"}
        )

## tags
class TagsDevView(View):
    def get(self, request):
        tags = Tag.objects.all()
        return render(request, 'developer/tags.html', {"tags": tags})

    def delete(self, request, tag_id):
        try:
            tag = Tag.objects.get(pk=tag_id)
            tag.delete()
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 500})
    
class AddTagsDevView(View):
    def get(self, request):
        form = TagDevForm()
        return render(request, 'developer/tagsForm.html',{
            "form": form,
            "tag": "Add"}
        )
    
    def post(self, request):
        form = TagDevForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("/account/developer/tags/")
        
        return render(request, 'developer/tagsForm.html',{
            "form": form,
            "tag": "Add"}
        )

class EditTagsDevView(View):
    def get(self, request, tag_id):
        tag = Tag.objects.get(pk=tag_id)
        form = TagDevForm(instance=tag)
        return render(request, 'developer/tagsForm.html',{
            "form": form,
            "tag": "Edit"}
        )
    
    def post(self, request, tag_id):
        tag = Tag.objects.get(pk=tag_id)
        form = TagDevForm(request.POST, instance=tag)
        
        if form.is_valid():
            form.save()
            return redirect("/account/developer/tags/")
        
        return render(request, 'developer/tagsForm.html',{
            "form": form,
            "tag": "Edit"}
        )
