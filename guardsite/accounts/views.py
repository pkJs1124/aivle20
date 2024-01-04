from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from accounts.forms import LoginForm, SignupForm, FindForm, FindpasswordForm, ResetPasswordForm
from django.urls import reverse
from accounts.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash

# 로딩페이지
def loading_view(request):
    return render(request, 'accounts/loading.html')

# 로그인
def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse("main"))
    
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            role = form.cleaned_data["role"]
            # print(username)
            # print(role)
            
            # 해당하는 사용자가 있는지 확인
            user = authenticate(username=username, password=password)
            
            # 사용자가 존재하면 로그인 후 메인페이지로 이동
            if user and user.role == role:
                login(request, user)
                return redirect(reverse("main"))
            # 없으면 로그인 실패 문구 출력
            else:
                error_message = "로그인 실패."
                return render(request, 'accounts/login.html', {'error_message': error_message})

        # 유효하지 않으면 토글 선택문구 출력
        else:
            error_message = "유저 유형을 선택하세요."
            return render(request, 'accounts/login.html', {'error_message': error_message, 'form':form})
            # context = {"form": form}
            # return render(request, "accounts/login.html", context)
    else:
        form = LoginForm()
        context = {"form": form}
        return render(request, "accounts/login.html", context)

# 로그아웃    
def logout_view(request):
    logout(request)
    return redirect(reverse("accounts:login"))

# 회원가입
def signup(request):
    # 폼에 에러가 없으면 user 생성 및 로그인 후 메인페이지 이동
    if request.method == "POST":
        form = SignupForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            role = form.cleaned_data["role"]
            person_name = form.cleaned_data["person_name"]
            phone_number = form.cleaned_data["phone_number"]
            company = form.cleaned_data["company"]
            
            # 선택된 역할에 따라 적절한 모델로 사용자 생성
            if role == 'admin':
                user = User.objects.create_user(username=username, password=password1, role='admin', person_name=person_name, phone_number=phone_number, company=company)
            elif role == 'worker':
                user = User.objects.create_user(username=username, password=password1, role='worker', person_name=person_name, phone_number=phone_number, company=company)
                
            login(request, user)
            return redirect(reverse("main"))
        # 폼에 에러가 있으면 에러를 포함한 폼을 사용해 회원가입 페이지로 이동
        else:
            # print(form.errors)
            context = {"form":form}
            return render(request, "accounts/signup_active.html", context)
    else:
        form = SignupForm()
        context = {"form": form}
        return render(request, "accounts/signup_active.html", context)
    
# 아이디 찾기
def find(request):
    if request.method == 'POST':
        form = FindForm(request.POST)
        if form.is_valid():
            person_name = form.cleaned_data['person_name']
            phone_number = form.cleaned_data['phone_number']

            try:
                user = User.objects.get(person_name=person_name, phone_number=phone_number)
                return render(request, 'accounts/find.html', {'username': user.username})
            except User.DoesNotExist:
                error_message = '일치하는 사용자를 찾을 수 없습니다.'
                return render(request, 'accounts/find.html', {'form': form, 'error_message': error_message})
    else:
        form = FindForm()

    return render(request, 'accounts/find.html', {'form': form})

# 비번 확인
def findpassword(request):
    if request.method == 'POST':
        form = FindpasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            phone_number = form.cleaned_data['phone_number']
            print(form.cleaned_data['username'])
            print(form.cleaned_data['phone_number'])
            
            try:
                user = User.objects.get(username=username, phone_number=phone_number)
                request.session['user_id'] = user.id
                return redirect(reverse("accounts:resetpassword"))
            except User.DoesNotExist:
                error_message = '일치하는 사용자를 찾을 수 없습니다.'
                return render(request, 'accounts/find_password.html', {'form': form, 'error_message': error_message})
        else:
            form = FindpasswordForm()
            return render(request, 'accounts/find_password.html', {'form': form})
    else:
        form = FindpasswordForm()
        return render(request, 'accounts/find_password.html', {'form': form})

# 비번 재설정
def resetpassword(request):
    user_id = request.session.get('user_id')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            # user = request.user
            user = User.objects.get(id=user_id)
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']

            # 비밀번호 업데이트
            user.set_password(new_password1)
            user.save()

            # 세션에서 사용자 정보 삭제
            del request.session['user_id']
            print(user)

            return redirect(reverse("accounts:login"))
        
        else:
            return render(request, 'accounts/reset_password.html', {'form': form})
        
    else:
        form = ResetPasswordForm()
        return render(request, 'accounts/reset_password.html', {'form': form})



def toscheck(request):
    return render(request, "accounts/signup_check.html")