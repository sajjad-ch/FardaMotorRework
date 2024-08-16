from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import Persons
from django.http import HttpRequest
from django.contrib.auth import login, logout
from account_module.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }

        return render(request, 'account_module/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            user_password = register_form.cleaned_data.get('password')
            user: bool = Persons.objects.filter(username__iexact=username).exists()
            if user:
                register_form.add_error('user_id', 'کد پرسنلی وارد شده تکراری می باشد')
            else:
                new_user = Persons(
                    username=str(username),
                )
                new_user.set_password(user_password)
                new_user.save()
                return redirect(reverse('login_page'))

        context = {
            'register_form': register_form
        }

        return render(request, 'account_module/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data.get('username')
            user_pass = login_form.cleaned_data.get('password')
            user: Persons = Persons.objects.filter(username__iexact=user_name).first()
            if user is not None:
                is_password_correct = user.check_password(user_pass)
                if is_password_correct:
                    login(request, user)
                    user.is_active = True
                    print('here is the user:')
                    print(user)
                    return redirect('home')
                else:
                    login_form.add_error('username', 'کلمه عبور اشتباه است')
            else:
                login_form.add_error('username', 'کاربری با مشخصات وارد شده یافت نشد')

        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context)


class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm()
        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forgot_password.html', context)

    def post(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            username = forget_pass_form.cleaned_data.get('username')
            user: Persons = Persons.objects.filter(username__exact=username).first()
            if user is not None:
                context = {
                    'user': user
                }
                return render(request, 'account_module/reset_password.html', context)

        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forgot_password.html', context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, username):
        user: Persons = Persons.objects.filter(username__exact=username).first()
        if user is None:
            return redirect(reverse('login_page'))

        reset_pass_form = ResetPasswordForm()

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request: HttpRequest, username):
        reset_pass_form = ResetPasswordForm(request.POST)
        user: Persons = Persons.objects.filter(username__iexact=username).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.save()
            return redirect(reverse('login_page'))

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }

        return render(request, 'account_module/reset_password.html', context)


class LogoutView(View):
    def get(self, request: HttpRequest):
        logout(request)
        request.user.is_active = False
        return redirect(reverse('login_page'))
