from account.models import Transaction, Notification, Budget, SavingsGoal
from django.db.models import Sum
from datetime import datetime

class Notify:
    # Check and Send Notification
    def __init__(self, *args, **kwargs):
        self.transaction = kwargs.pop('transaction', None)
        self.saving = kwargs.get('saving', None)
        self.user = kwargs.pop('user', None)
        self.budget = 0

    def checkBudget(self):
        if self.transaction is not None:
            if (Budget.objects.filter(user=self.user, category=self.transaction.category).exists()):
                if self.transaction.transaction_type == "expense":
                    user_accounts = self.user.account_set.all()

                    transactions = Transaction.objects.filter(
                        account__in=user_accounts,
                        category=self.transaction.category,
                        create_at__month=datetime.now().month,
                        transaction_type="expense").aggregate(expense=Sum("amount"))
                    
                    totalExpense = transactions['expense']
                    self.budget = (Budget.objects.get(user=self.user, category=self.transaction.category)).amount
                    
                    percent = (totalExpense/self.budget)*100
                    
                    return percent
        return 0

    def checkSaving(self):
        if self.saving is not None:
            if (SavingsGoal.objects.filter(user=self.user, name=self.saving.name).exists()):
                if (self.saving.current_amount >= self.saving.target_amount):
                    percent = (self.saving.current_amount/self.saving.target_amount)*100
                    return percent
        return 0

    def send(self, percentBudget, percentSaving):
        # ส่งการแจ้งเตือน
        if percentBudget >= 100:
            if (not (Notification.objects.filter(notification_date__month=datetime.now().month, user=self.user, notify_type="100% Budget Used", category=self.transaction.category).exists())):
                message = f"หมวดหมู่ {self.transaction.category} ของคุณใช้เงินถึง 100% แล้ว ({(percentBudget/100)*self.budget}/{self.budget})"
                Notification.objects.create(user=self.user, notify_type="100% Budget Used", message=message, category=self.transaction.category)
        elif percentBudget >= 75:
            if (not (Notification.objects.filter(notification_date__month=datetime.now().month, user=self.user, notify_type="75% Budget Used", category=self.transaction.category).exists())):
                message = f"หมวดหมู่ {self.transaction.category} ของคุณใช้เงินถึง 75% แล้ว ({(percentBudget/100)*self.budget}/{self.budget})"
                Notification.objects.create(user=self.user, notify_type="75% Budget Used", message=message, category=self.transaction.category)
        elif percentBudget >= 50:
            if (not (Notification.objects.filter(notification_date__month=datetime.now().month, user=self.user, notify_type="50% Budget Used", category=self.transaction.category).exists())):
                message = f"หมวดหมู่ {self.transaction.category} ของคุณใช้เงินถึง 50% แล้ว ({(percentBudget/100)*self.budget}/{self.budget})"
                Notification.objects.create(user=self.user, notify_type="50% Budget Used", message=message, category=self.transaction.category)

        if percentSaving >= 100:
            if (not (Notification.objects.filter(notification_date__month=datetime.now().month, user=self.user, notify_type="100% Saving Goal", message__icontains=self.saving.name).exists())):
                message = f"การออมเงิน {self.saving.name} ของคุณออมถึง 100% แล้ว ({self.saving.current_amount}/{self.saving.target_amount})"
                Notification.objects.create(user=self.user, notify_type="100% Saving Goal", message=message, category=self.transaction.category)

    
    
    def execute(self):
        # เรียก check และ send
        percentBudget = self.checkBudget()
        percentSaving = self.checkSaving()
        if percentBudget >= 50 or percentSaving >= 100:
            self.send(percentBudget, percentSaving)

