from account.models import Transaction, Notification, Budget
from django.db.models import Sum
from datetime import datetime

class Notify:
    def __init__(self, *args, **kwargs):
        self.transaction = kwargs.pop('transaction', None)
        self.budget = kwargs.pop('budget', None)
        self.user = kwargs.pop('user', None)

    def check(self):
        # ตรวจสอบเงื่อนไข
        if self.transaction is not None:
            if self.transaction.transaction_type == "expense":
                user_accounts = self.user.account_set.all()

                transactions = Transaction.objects.filter(
                    account__in=user_accounts,
                    category=self.transaction.category,
                    create_at__month=datetime.now().month,
                    transaction_type="expense").aggregate(expense=Sum("amount"))
                
                totalExpense = transactions['expense']
                budget = (Budget.objects.get(category=self.transaction.category)).amount
                print(totalExpense)
                print(budget)
                
                percent = (totalExpense/budget)*100
                print(percent)
                
                return percent
        return 0

    def send(self):
        # ส่งการแจ้งเตือน
        print(f"Notification: Transaction {self.transaction.id} has reached the threshold!")

    def execute(self):
        # เรียก check และ send
        if self.check() >= 100:
            self.send()
        elif self.check() >= 75:
            self.send()
        elif self.check() >= 50:
            self.send()
