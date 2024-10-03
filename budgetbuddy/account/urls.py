from django.urls import path

from account.views import *

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('budget/', BudgetView.as_view(), name="budget"),
    path('budget/add/', AddBudgetView.as_view(), name="addBudget"),
    path('budget/edit/', EditBudgetView.as_view(), name="editBudget"),
    path('saving/', SavingView.as_view(), name="saving"),
    path('saving/add/', AddSavingView.as_view(), name="addSaving"),
    path('account/', AccountView.as_view(), name="account"),
    path('account/add/', AddAccountView.as_view(), name="addAccount"),
    path('notify/', NotifyView.as_view(), name="notify"),
]