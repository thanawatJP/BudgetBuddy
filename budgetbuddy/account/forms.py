from django import forms
from django.forms import ModelForm
from .models import Budget, SavingsGoal, Account, Category, Tag, Transaction
from django.core.exceptions import ValidationError
from datetime import date

class TransactionForm(ModelForm):

    amount = forms.DecimalField(min_value=0.0)

    class Meta:
        model = Transaction
        fields = [
            "description",
            "amount",
            "transaction_type",
            "account",
            "category",
            "tags"
        ]
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        # Filter the account field to only show accounts for the current user

        request = kwargs.get('initial', {})
        if self.instance.pk is not None:
            description = self.instance.description
            transaction_type = self.instance.transaction_type
            category = self.instance.category

            # หากตรงตามเงื่อนไขให้ล็อคฟิลด์
            if description.startswith("Saving to") and transaction_type == "expense" and category == Category.objects.get(name=category):
                self.fields['description'].disabled = True
                self.fields['transaction_type'].disabled = True
                self.fields['category'].disabled = True

        elif request['description']!='' and request['transaction_type']!='' and request['category']!='':
            self.initial['description'] = request.get('description', '')
            self.initial['transaction_type'] = request.get('transaction_type', '')
            category = Category.objects.get(name=request.get('category', ''))
            self.initial['category'] = category

            # ล็อค fields
            self.fields['description'].disabled = True
            self.fields['transaction_type'].disabled = True
            self.fields['category'].disabled = True

        self.fields['account'].queryset = Account.objects.filter(user=self.user)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'


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
        self.user = kwargs.pop('user', None)
        super(SavingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'
    
    def clean_name(self):
        name = self.cleaned_data["name"]

        if self.instance.pk is None:
            # กรณีสร้างใหม่
            if SavingsGoal.objects.filter(name=name, user=self.user).exists():
                raise ValidationError("คุณใช้ชื่อนี้ ในการสร้างการสะสมเงินไปแล้ว")
        else:
            # สำหรับ edit
            oldname = self.instance.name
            if oldname != name:
                if SavingsGoal.objects.filter(name=name, user=self.instance.user).exists():
                    raise ValidationError("คุณใช้ชื่อนี้ ในการสร้างการสะสมเงินไปแล้ว")
        return name
    
    def clean_target_date(self):
        target_date = self.cleaned_data["target_date"]
        if target_date < date.today():
            raise ValidationError("วันที่ของคุณเป็นอดีต")
        return target_date

class AccountForm(ModelForm):

    class Meta:
        model = Account
        fields = [
            "name"
        ]
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AccountForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full border border-gray-600 rounded'

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Account.objects.filter(name=name, user=self.user).exists():
            raise ValidationError("คุณใช้ชื่อนี้ในการสร้างบัญชีไปแล้ว")
        return name

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

