from account.models import Transaction, Notification, Budget
from django.db.models import Sum
from datetime import datetime

class Notify:
    def __init__(self, *args, **kwargs):
        self.transaction = kwargs.pop('transaction', None)
        self.user = kwargs.pop('user', None)
        self.budget = 0

    def check(self):
        # ตรวจสอบเงื่อนไข
        if self.transaction is not None:
            if (Budget.objects.filter(category=self.transaction.category).exists()):
                if self.transaction.transaction_type == "expense":
                    user_accounts = self.user.account_set.all()

                    transactions = Transaction.objects.filter(
                        account__in=user_accounts,
                        category=self.transaction.category,
                        create_at__month=datetime.now().month,
                        transaction_type="expense").aggregate(expense=Sum("amount"))
                    
                    totalExpense = transactions['expense']
                    self.budget = (Budget.objects.get(category=self.transaction.category)).amount
                    
                    percent = (totalExpense/self.budget)*100
                    
                    return percent
        return 0

    def send(self, percent):
        # ส่งการแจ้งเตือน
        if percent >= 100:
            if (not (Notification.objects.filter(notification_date__month=datetime.now().month, user=self.user, notify_type="100% Budget Used", category=self.transaction.category).exists())):
                message = f"หมวดหมู่ {self.transaction.category} ของคุณใช้เงินถึง 100% แล้ว ({(1+(percent/100))*self.budget}/{self.budget})"
                Notification.objects.create(user=self.user, notify_type="100% Budget Used", message=message, category=self.transaction.category)
        elif percent >= 75:
            if (not (Notification.objects.filter(notification_date__month=datetime.now().month, user=self.user, notify_type="75% Budget Used", category=self.transaction.category).exists())):
                message = f"หมวดหมู่ {self.transaction.category} ของคุณใช้เงินถึง 75% แล้ว ({(1+(percent/100))*self.budget}/{self.budget})"
                Notification.objects.create(user=self.user, notify_type="75% Budget Used", message=message, category=self.transaction.category)
        elif percent >= 50:
            if (not (Notification.objects.filter(notification_date__month=datetime.now().month, user=self.user, notify_type="50% Budget Used", category=self.transaction.category).exists())):
                message = f"หมวดหมู่ {self.transaction.category} ของคุณใช้เงินถึง 50% แล้ว ({(percent/100)*self.budget}/{self.budget})"
                Notification.objects.create(user=self.user, notify_type="50% Budget Used", message=message, category=self.transaction.category)

    def execute(self):
        # เรียก check และ send
        percent = self.check()
        if percent >= 50:
            self.send(percent)
