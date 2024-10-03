from django import forms
from django.forms import ModelForm
from .models import Budget, SavingsGoal, Account, Category, Tag

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

class SavingForm(ModelForm):

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
        super(SavingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'

class AccountForm(ModelForm):

    class Meta:
        model = Account
        fields = [
            "name"
        ]
    
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'

class CategoryDevForm(ModelForm):

    class Meta:
        model = Category
        fields = [
            "name"
        ]
    
    def __init__(self, *args, **kwargs):
        super(CategoryDevForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'


class TagDevForm(ModelForm):

    class Meta:
        model = Tag
        fields = [
            "name"
        ]
    
    def __init__(self, *args, **kwargs):
        super(TagDevForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'

