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
        form = AddBudgetForm()
        return render(request, 'budget/addBudget.html', {"form": form})
    
class EditBudgetView(View):
    def get(self, request):
    # def get(self, request, budget_id):
        # budget = Budget.objects.get(id=budget_id)
        # form = EditBudgetForm(instance=budget)
        
        form = EditBudgetForm()
        return render(request, 'budget/editBudget.html', {"form": form})
    
#saving zone view
class SavingView(View):
    def get(self, request):
        return render(request, 'saving.html')
