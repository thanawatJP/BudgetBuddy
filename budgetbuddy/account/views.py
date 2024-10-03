from django.shortcuts import render
from django.views import View
from .forms import *

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
        return render(request, 'account/account.html', {"accounts": accounts})

class AddAccountView(View):
    def get(self, request):
        form = AddAccountForm()
        return render(request, 'account/addAccount.html', {"form": form})

#notify zone view
class NotifyView(View):
    def get(self, request):
        return render(request, 'notify.html')

