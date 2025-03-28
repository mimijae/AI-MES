from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounting_list, name='accounting_list'),  # 거래 목록 페이지
    path('add/', views.accounting_add, name='accounting_add'),  # 거래 추가 페이지
    path('<int:id>/edit/', views.accounting_edit, name='accounting_edit'),  # 거래 수정 페이지
    path('<int:id>/delete/', views.accounting_delete, name='accounting_delete'),  # 거래 삭제
]
