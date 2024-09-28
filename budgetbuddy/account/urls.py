from django.urls import path

from account.views import *

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('budget/', BudgetView.as_view(), name="budget"),
    path('addBudget/', AddBudgetView.as_view(), name="addBudget"),
    path('editBudget/', EditBudgetView.as_view(), name="editBudget"),
    path('saving/', SavingView.as_view(), name="saving"),

]