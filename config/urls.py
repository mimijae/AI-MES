# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('management.urls')),   # 메인 페이지 및 조직 관리 URL 포함
    path('user/', include('users.urls')),    # 사용자 관련 URL 포함
    path('accounting/', include('accounting.urls')),   # 회계 장부 URL 포함
    path('inventory/', include('inventory.urls')),     # 물품 관리 URL 포함
    path('chat/', include('chat.urls')), #  chat 앱 URL 연결
]
# Static files and media configuration for development
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 어드민 페이지 커스터마이징
admin.site.site_title = "AI-MES SmartFactory Admin"  # 프로젝트 이름을 반영한 타이틀
admin.site.site_header = "AI-MES SmartFactory Admin"  # 어드민 페이지의 헤더
admin.site.index_title = "AI-MES SmartFactory Management"  # 어드민 페이지의 인덱스 타이틀