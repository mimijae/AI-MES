from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Organization, OrganizationMember
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator


# 메인 페이지
from django.shortcuts import render, redirect

def index(request):
    if request.user.is_authenticated:
        return redirect('chat_page')  # 로그인 시 채팅 페이지로 리디렉션
    return render(request, 'management/index.html', {'request': request})  # 비로그인 시 메인 페이지


# 조직 목록
@login_required
def organization_list(request):
    # 페이지당 표시할 조직 개수 설정
    items_per_page = int(request.GET.get('items_per_page', 5))  # 기본값 5
    organizations = Organization.objects.filter(members__user=request.user).order_by('-id')

    # 페이지 네이션 설정
    paginator = Paginator(organizations, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 페이지 표시 개수 옵션
    items_per_page_options = [5, 10, 15, 20]

    return render(request, 'management/organization_list.html', {
        'organizations': page_obj,
        'items_per_page': items_per_page,
        'items_per_page_options': items_per_page_options,  # 옵션 전달
    })


# 조직 추가
@login_required
def organization_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        organization_type = request.POST.get('organization_type')

        # 조직 생성
        organization = Organization.objects.create(
            name=name,
            description=description,
            organization_type=organization_type,
            created_by=request.user
        )

        # 생성한 사용자를 조직의 관리자로 추가
        OrganizationMember.objects.create(
            organization=organization,
            user=request.user,
            role='admin'
        )

        messages.success(request, "조직이 성공적으로 추가되었습니다.")
        return redirect('organization_list')

    return render(request, 'management/organization_add.html')

# 조직 수정
@login_required
def organization_edit(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id, members__user=request.user)

    if request.method == 'POST':
        organization.name = request.POST.get('name')
        organization.description = request.POST.get('description')
        organization.organization_type = request.POST.get('organization_type')
        organization.save()
        
        messages.success(request, "조직이 성공적으로 수정되었습니다.")
        return redirect('organization_list')

    return render(request, 'management/organization_edit.html', {'organization': organization})

# 조직 삭제
@login_required
def organization_delete(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id, members__user=request.user)

    if request.method == 'POST':
        organization.delete()
        messages.success(request, "조직이 성공적으로 삭제되었습니다.")
        return redirect('organization_list')

    return render(request, 'management/organization_confirm_delete.html', {'organization': organization})