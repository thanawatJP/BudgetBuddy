from django import forms
from django.forms import ModelForm
from .models import Budget

class AddBudgetForm(ModelForm):

    amount = forms.DecimalField(min_value=0.0)

    class Meta:
        model = Budget
        fields = [
            "category",
            "amount",
        ]
    
    def __init__(self, *args, **kwargs):
        super(AddBudgetForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'

class EditBudgetForm(ModelForm):

    amount = forms.DecimalField(min_value=0.0)

    class Meta:
        model = Budget
        fields = [
            "category",
            "amount",
        ]
    
    def __init__(self, *args, **kwargs):
        super(EditBudgetForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'