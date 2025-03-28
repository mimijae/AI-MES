from django.db import models
from common.models import CommonModel
from management.models import Organization
from users.models import User

class Category(CommonModel):
    """물품 카테고리 모델"""

    name = models.CharField(max_length=100, unique=True)  # 카테고리명
    description = models.TextField(blank=True)  # 카테고리 설명

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'category'

class Item(CommonModel):
    """재고 물품 모델"""

    STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('discontinued', 'Discontinued'),
    ]

    name = models.CharField(max_length=100)  # 물품명
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")  # 카테고리
    quantity = models.IntegerField(default=0)  # 수량
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # 단가
    received_date = models.DateField(null=True, blank=True)  # 입고 날짜
    expiration_date = models.DateField(null=True, blank=True)  # 만료 날짜
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_stock',
    )  # 재고 상태
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="items")  # 관련 조직
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items_created")  # 물품 생성자

    def __str__(self):
        return f"{self.name} - {self.quantity} units ({self.get_status_display()})"
    class Meta:
        db_table = 'item'