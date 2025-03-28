from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import User
from django.core.paginator import Paginator

@login_required
def user_list(request):
    # 페이지당 표시할 사용자 개수 설정
    items_per_page = int(request.GET.get('items_per_page', 5))  # 기본값 5
    users = User.objects.all().order_by('-id')  # 사용자 목록 정렬

    # 페이지 네이션 설정
    paginator = Paginator(users, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 페이지 표시 개수 옵션
    items_per_page_options = [5, 10, 15, 20]

    return render(request, 'user/user_list.html', {
        'users': page_obj,
        'items_per_page': items_per_page,
        'items_per_page_options': items_per_page_options,  # 옵션 전달
    })


# 로그인 뷰
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "로그인에 성공했습니다.")
            return redirect('index')
        else:
            messages.error(request, "유효하지 않은 사용자명 또는 비밀번호입니다.")
    
    return render(request, 'user/login.html')

# 회원가입 뷰
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "회원가입이 완료되었습니다. 로그인 해주세요.")
            return redirect('users:login')
        else:
            messages.error(request, "회원가입에 실패했습니다. 다시 시도해주세요.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'user/register.html', {'form': form})

# 로그아웃 뷰
def logout_view(request):
    logout(request)
    messages.success(request, "로그아웃 되었습니다.")
    return redirect('users:login')

# 사용자 상세 보기 뷰
@login_required
def user_detail(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, 'user/user_detail.html', {'user': user})

# 사용자 수정 뷰
@login_required
def user_edit(request, id):
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "사용자 정보가 성공적으로 수정되었습니다.")
            return redirect('users:user_detail', id=user.id)
        else:
            messages.error(request, "수정 중 오류가 발생했습니다. 다시 시도해주세요.")
    else:
        form = CustomUserCreationForm(instance=user)
    
    return render(request, 'user/user_edit.html', {'form': form, 'user': user})

# 사용자 삭제 뷰
@login_required
def user_delete(request, id):
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, "사용자가 성공적으로 삭제되었습니다.")
        return redirect('users:user_list')
    
    return render(request, 'user/user_confirm_delete.html', {'user': user})