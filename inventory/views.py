from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Item, Category
from management.models import Organization
from django.contrib import messages
from django.core.paginator import Paginator

# 물품 목록
@login_required
def item_list(request):
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

    # 물품 목록 가져오기
    items = Item.objects.filter(
        organization_id=selected_organization.id,
        organization__members__user=request.user
    ).order_by('-id')  # 최근에 추가된 물품 순으로 정렬

    # 페이지 네이션 설정
    paginator = Paginator(items, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 페이지 표시 개수 옵션
    items_per_page_options = [5, 10, 15, 20]

    return render(request, 'inventory/item_list.html', {
        'items': page_obj,
        'organizations': organizations,
        'selected_organization': selected_organization,
        'items_per_page': items_per_page,
        'items_per_page_options': items_per_page_options,  # 옵션 전달
    })


# 물품 추가
@login_required
def item_add(request):
    organization_id = request.GET.get('organization_id')
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        quantity = request.POST.get('quantity')
        price_per_unit = request.POST.get('price_per_unit')
        organization_id = request.POST.get('organization')

        # 조직 및 카테고리 가져오기
        organization = get_object_or_404(Organization, id=organization_id, members__user=request.user)
        category = get_object_or_404(Category, id=category_id)

        # 물품 생성
        Item.objects.create(
            name=name,
            category=category,
            quantity=quantity,
            price_per_unit=price_per_unit,
            organization=organization,
            created_by=request.user
        )
        messages.success(request, "물품이 성공적으로 추가되었습니다.")
        return redirect(f'{reverse("item_list")}?organization_id={organization_id}')

    organizations = Organization.objects.filter(members__user=request.user)
    categories = Category.objects.all()
    return render(request, 'inventory/item_add.html', {
        'organizations': organizations,
        'categories': categories,
        'selected_organization': organization_id
    })

# 물품 수정
@login_required
def item_edit(request, item_id):
    item = get_object_or_404(Item, id=item_id, organization__members__user=request.user)
    organization_id = item.organization.id

    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.category_id = request.POST.get('category')
        item.quantity = request.POST.get('quantity')
        item.price_per_unit = request.POST.get('price_per_unit')
        item.save()
        messages.success(request, "물품이 성공적으로 수정되었습니다.")
        return redirect(f'{reverse("item_list")}?organization_id={organization_id}')

    categories = Category.objects.all()
    return render(request, 'inventory/item_edit.html', {
        'item': item,
        'categories': categories,
        'selected_organization': organization_id
    })

# 물품 삭제
@login_required
def item_delete(request, item_id):
    item = get_object_or_404(Item, id=item_id, organization__members__user=request.user)
    organization_id = item.organization.id

    if request.method == 'POST':
        item.delete()
        messages.success(request, "물품이 성공적으로 삭제되었습니다.")
        return redirect(f'{reverse("item_list")}?organization_id={organization_id}')

    return render(request, 'inventory/item_confirm_delete.html', {
        'item': item,
        'selected_organization': organization_id
    })