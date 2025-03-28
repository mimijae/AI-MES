from django.urls import path
from . import views

app_name = 'users'  # 네임스페이스 설정

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.user_list, name='user_list'),
    path('<int:id>/detail/', views.user_detail, name='user_detail'),  # 상세 보기 URL
    path('<int:id>/edit/', views.user_edit, name='user_edit'),  # 수정 URL
    path('<int:id>/delete/', views.user_delete, name='user_delete'),  # 삭제 URL
]