from django import forms
from django.forms import ModelForm
from .models import Budget, SavingsGoal, Account, Category, Tag
from django.core.exceptions import ValidationError

from django.contrib.auth.mixins import LoginRequiredMixin

class BudgetForm(ModelForm):

    amount = forms.DecimalField(min_value=0.0)

    class Meta:
        model = Budget
        fields = [
            "category",
            "amount",
        ]
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BudgetForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'

    def clean_category(self):
        category = self.cleaned_data["category"]

        if self.instance.pk is None:
            # กรณีสร้างใหม่
            if Budget.objects.filter(category=category, user=self.user).exists():
                raise ValidationError("คุณใช้หมวดหมู่นี้ ในการสร้างงบประมาณไปแล้ว")
        else:
            # สำหรับ edit
            oldCategory = self.instance.category
            # ตรวจสอบว่า budget ที่มี category นี้มีอยู่แล้วสำหรับ user ปัจจุบันหรือไม่
            if oldCategory != category:
                if Budget.objects.filter(category=category, user=self.instance.user).exists():
                    raise ValidationError("คุณใช้หมวดหมู่นี้ ในการสร้างงบประมาณไปแล้ว")

        return category

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

