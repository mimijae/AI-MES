from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Accounting
from management.models import Organization
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator

# 회계 기록 목록
@login_required
def accounting_list(request):
    organization_id = request.GET.get('organization_id')
    items_per_page = int(request.GET.get('items_per_page', 5))  # 기본값 5
    organizations = Organization.objects.filter(members__user=request.user)

    # 조직이 없는 경우 예외 처리
    if not organizations.exists():
        return render(request, 'management/no_organization.html')

    # 기본적으로 첫 번째 조직 선택
    if not organization_id:
        organization_id = organizations.first().id

    selected_organization = get_object_or_404(Organization, id=organization_id, members__user=request.user)

    # 회계 기록 목록 가져오기
    accountings = Accounting.objects.filter(
        organization_id=selected_organization.id,
        organization__members__user=request.user
    ).order_by('-accounting_date')

    # 페이지 네이션 설정
    paginator = Paginator(accountings, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 페이지 표시 개수 옵션
    items_per_page_options = [5, 10, 15, 20]

    return render(request, 'accounting/accounting_list.html', {
        'accountings': page_obj,
        'organizations': organizations,
        'selected_organization': selected_organization,
        'items_per_page': items_per_page,
        'items_per_page_options': items_per_page_options,  # 옵션 전달
    })


# 회계 기록 추가
@login_required
def accounting_add(request):
    organization_id = request.GET.get('organization_id')
    if request.method == 'POST':
        accounting_type = request.POST.get('accounting_type')  # 올바르게 변경됨
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        accounting_date = request.POST.get('accounting_date')  # 올바르게 변경됨
        description = request.POST.get('description')
        organization_id = request.POST.get('organization')

        # 로그인한 사용자가 속한 조직인지 확인
        organization = get_object_or_404(Organization, id=organization_id, members__user=request.user)

        # 회계 기록 생성
        Accounting.objects.create(
            organization=organization,
            accounting_type=accounting_type,  # 올바르게 변경됨
            amount=amount,
            payment_method=payment_method,
            accounting_date=accounting_date,  # 올바르게 변경됨
            description=description,
            handled_by=request.user
        )
        messages.success(request, "회계 기록이 성공적으로 추가되었습니다.")
        return redirect(f'{reverse("accounting_list")}?organization_id={organization_id}')

    # 로그인한 사용자가 속한 조직 목록을 가져와 폼에 전달
    organizations = Organization.objects.filter(members__user=request.user)
    return render(request, 'accounting/accounting_add.html', {
        'organizations': organizations,
        'selected_organization': organization_id
    })


# 회계 기록 수정
@login_required
def accounting_edit(request, id):
    accounting = get_object_or_404(Accounting, id=id, organization__members__user=request.user)
    organization_id = accounting.organization.id

    if request.method == 'POST':
        accounting.accounting_type = request.POST.get('accounting_type')  # 변경됨
        accounting.amount = request.POST.get('amount')
        accounting.payment_method = request.POST.get('payment_method')
        accounting.accounting_date = request.POST.get('accounting_date')  # 변경됨
        accounting.description = request.POST.get('description')
        accounting.save()
        messages.success(request, "회계 기록이 성공적으로 수정되었습니다.")
        return redirect(f'{reverse("accounting_list")}?organization_id={organization_id}')

    return render(request, 'accounting/accounting_edit.html', {
        'accounting': accounting,
        'selected_organization': organization_id
    })

# 회계 기록 삭제
@login_required
def accounting_delete(request, id):
    accounting = get_object_or_404(Accounting, id=id, organization__members__user=request.user)
    organization_id = accounting.organization.id

    if request.method == 'POST':
        accounting.delete()
        messages.success(request, "회계 기록이 성공적으로 삭제되었습니다.")
        return redirect(f'{reverse("accounting_list")}?organization_id={organization_id}')

    return render(request, 'accounting/accounting_confirm_delete.html', {
        'accounting': accounting,
        'selected_organization': organization_id
    })
