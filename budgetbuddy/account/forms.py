from django import forms
from django.forms import ModelForm
from .models import Budget, SavingsGoal, Account

class BudgetForm(ModelForm):

    amount = forms.DecimalField(min_value=0.0)

    class Meta:
        model = Budget
        fields = [
            "category",
            "amount",
        ]
    
    def __init__(self, *args, **kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'

# class AddBudgetForm(ModelForm):

#     amount = forms.DecimalField(min_value=0.0)

#     class Meta:
#         model = Budget
#         fields = [
#             "category",
#             "amount",
#         ]
    
#     def __init__(self, *args, **kwargs):
#         super(AddBudgetForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'

# class EditBudgetForm(ModelForm):

#     amount = forms.DecimalField(min_value=0.0)

#     class Meta:
#         model = Budget
#         fields = [
#             "category",
#             "amount",
#         ]
    
#     def __init__(self, *args, **kwargs):
#         super(EditBudgetForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'


class AddSavingForm(ModelForm):

    target_amount = forms.DecimalField(min_value=0.0)

    class Meta:
        model = SavingsGoal
        fields = [
            "name",
            "target_amount",
            "target_date",
        ]
        widgets = {
            "target_date": forms.TextInput(attrs={"type": "date"})
        }
    
    def __init__(self, *args, **kwargs):
        super(AddSavingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'

class AddAccountForm(ModelForm):

    class Meta:
        model = Account
        fields = [
            "name"
        ]
    
    def __init__(self, *args, **kwargs):
        super(AddAccountForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'
