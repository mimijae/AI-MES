from django.db import models
from common.models import CommonModel
from management.models import Organization
from users.models import User

class Accounting(CommonModel):
    """회계 거래 모델"""

    INCOME = 'income'
    EXPENSE = 'expense'
    ACCOUNTING_TYPE_CHOICES = [  # 기존 TRANSACTION_TYPE_CHOICES
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('transfer', 'Bank Transfer'),
        ('other', 'Other'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="accountings")  # 관련 조직
    accounting_type = models.CharField(  # 기존 transaction_type
        max_length=10,
        choices=ACCOUNTING_TYPE_CHOICES,
        default=INCOME,
    )  # 거래 유형
    amount = models.DecimalField(max_digits=15, decimal_places=2)  # 거래 금액
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
    )  # 결제 수단
    accounting_date = models.DateField()  # 기존 transaction_date
    description = models.TextField(blank=True)  # 거래 설명
    handled_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accountings")  # 거래 담당자

    def __str__(self):
        return f"{self.get_accounting_type_display()} - {self.amount} ({self.accounting_date})"  # 기존 get_transaction_type_display
    
    class Meta:
        db_table = 'accounting'  # 테이블 이름 간단히 변경
