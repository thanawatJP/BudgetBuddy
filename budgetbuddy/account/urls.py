from django.urls import path

from account.views import *

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    #report
    path('transaction/', TransactionView.as_view(), name="transaction"),
    path('transaction/add/', AddTransactionView.as_view(), name="addTransaction"),
    path('transaction/edit/<int:transaction_id>', TransactionView.as_view(), name="editTransaction"),
    #budget
    path('budget/', BudgetView.as_view(), name="budget"),
    path('budget/delete/<int:budget_id>/', BudgetView.as_view(), name="deleteBudget"),
    path('budget/add/', AddBudgetView.as_view(), name="addBudget"),
    path('budget/edit/<int:budget_id>/', EditBudgetView.as_view(), name="editBudget"),
    #saving
    path('saving/', SavingView.as_view(), name="saving"),
    path('saving/add/', AddSavingView.as_view(), name="addSaving"),
    #account
    path('account/', AccountView.as_view(), name="account"),
    path('account/add/', AddAccountView.as_view(), name="addAccount"),
    path('account/delete/<int:account_id>/', AccountView.as_view(), name="deleteAccount"),
    path('account/edit/<int:account_id>/', EditAccountView.as_view(), name="editAccount"),
    #notify
    path('notify/', NotifyView.as_view(), name="notify"),
    
    # dev zone
    ## categories
    path('developer/categories/', CategoriesDevView.as_view(), name="categoriesDev"),
    path('developer/categories/delete/<int:category_id>/', CategoriesDevView.as_view(), name="deleteCategoryDev"),
    path('developer/categories/add', AddCategoriesDevView.as_view(), name="addCategoriesDev"),
    path('developer/categories/edit/<int:category_id>/', EditCategoriesDevView.as_view(), name="editCategoryDev"),
    ## tags
    path('developer/tags/', TagsDevView.as_view(), name="tagsDev"),
    path('developer/tags/delete/<int:tag_id>/', TagsDevView.as_view(), name="deleteTagDev"),
    path('developer/tags/add', AddTagsDevView.as_view(), name="addTagsDev"),
    path('developer/tags/edit/<int:tag_id>/', EditTagsDevView.as_view(), name="editTagDev"),

    #PDF FILE
    path('monthlyreport/', ViewPDF.as_view(), name="monthly-report"),
]