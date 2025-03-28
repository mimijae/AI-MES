from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 메인 페이지
    path('organization/', views.organization_list, name='organization_list'),  # 조직 목록 페이지
    path('organization/add/', views.organization_add, name='organization_add'),  # 조직 추가 페이지
    path('organization/edit/<int:organization_id>/', views.organization_edit, name='organization_edit'),  # 조직 수정 페이지
    path('organization/delete/<int:organization_id>/', views.organization_delete, name='organization_delete'),  # 조직 삭제 페이지
]