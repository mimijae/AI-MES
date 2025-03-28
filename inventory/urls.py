# inventory/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='item_list'),                   # 물품 목록 페이지
    path('add/', views.item_add, name='item_add'),                 # 물품 추가 페이지
    path('<int:item_id>/edit/', views.item_edit, name='item_edit'),     # 물품 수정 페이지
    path('<int:item_id>/delete/', views.item_delete, name='item_delete'), # 물품 삭제
]