from django.urls import path

from account.views import *

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('account/', HomeView.as_view(), name="home"),
    #report
    path('account/transaction/', TransactionView.as_view(), name="transaction"),
    path('account/transaction/delete/<int:transaction_id>/', TransactionView.as_view(), name="transaction"),
    path('account/transaction/add/', AddTransactionView.as_view(), name="addTransaction"),
    path('account/transaction/edit/<int:transaction_id>/', EditTransactionView.as_view(), name="editTransaction"),
    #budget
    path('account/budget/', BudgetView.as_view(), name="budget"),
    path('account/budget/delete/<int:budget_id>/', BudgetView.as_view(), name="deleteBudget"),
    path('account/budget/add/', AddBudgetView.as_view(), name="addBudget"),
    path('account/budget/edit/<int:budget_id>/', EditBudgetView.as_view(), name="editBudget"),
    #saving
    path('account/saving/', SavingView.as_view(), name="saving"),
    path('account/saving/delete/<int:saving_id>/', SavingView.as_view(), name="deleteSaving"),
    path('account/saving/add/', AddSavingView.as_view(), name="addSaving"),
    path('account/saving/edit/<int:saving_id>/', EditSavingView.as_view(), name="editSaving"),
    #account
    path('account/account/', AccountView.as_view(), name="account"),
    path('account/account/add/', AddAccountView.as_view(), name="addAccount"),
    path('account/account/delete/<int:account_id>/', AccountView.as_view(), name="deleteAccount"),
    path('account/account/edit/<int:account_id>/', EditAccountView.as_view(), name="editAccount"),
    #notify
    path('account/notify/', NotifyView.as_view(), name="notify"),
    path('account/notify/delete/<int:notification_id>/', NotifyView.as_view(), name="deleteNotify"),
    
    #Edit Profile
    path('editprofile/', EditProfileView.as_view(), name="edit-profile"),
    path('editprofile/resetpassword', ResetPassWordView.as_view(), name="reset-password"),
    
    # dev zone
    ## categories
    path('account/developer/categories/', CategoriesDevView.as_view(), name="categoriesDev"),
    path('account/developer/categories/delete/<int:category_id>/', CategoriesDevView.as_view(), name="deleteCategoryDev"),
    path('account/developer/categories/add', AddCategoriesDevView.as_view(), name="addCategoriesDev"),
    path('account/developer/categories/edit/<int:category_id>/', EditCategoriesDevView.as_view(), name="editCategoryDev"),
    ## tags
    path('account/developer/tags/', TagsDevView.as_view(), name="tagsDev"),
    path('account/developer/tags/delete/<int:tag_id>/', TagsDevView.as_view(), name="deleteTagDev"),
    path('account/developer/tags/add', AddTagsDevView.as_view(), name="addTagsDev"),
    path('account/developer/tags/edit/<int:tag_id>/', EditTagsDevView.as_view(), name="editTagDev"),

    #PDF FILE
    path('account/monthlyreport/', ViewPDF.as_view(), name="monthly-report"),
]