from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . import forms
from .models import *
from random import randint
from utils import send_otp_code
from django.contrib import messages
from time import time
from datetime import datetime
from django.contrib.auth import login, logout, authenticate


class UserRegisterView(View):
    form_class = forms.UserCreateForm

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/user_register.html', {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            request.session['user_register'] = {'phone_number': cd['phone_number'],
                                                'password': cd['password1']}
            request.session.modified = True
            code = randint(10000, 99999)
            OtpCode.objects.create(phone_number=cd['phone_number'], code=code)
            send_otp_code(code, cd['phone_number'])
            return redirect('accounts:user_otp_code')
        return render(request, 'accounts/user_register.html', {'form': form})


class UserOtpCodeView(View):
    form_class = forms.OtpCodeForm
    template_name = 'accounts/user_otp_code.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            instance = OtpCode.objects.filter(
                code=code, phone_number=request.session['user_register']['phone_number'])
            if instance.exists():
                instance1 = instance[0]
                now = time()
                t = instance1.created.timestamp()
                if now - t < 120:
                    User.objects.create(
                        phone_number=request.session['user_register']['phone_number'],
                        password=request.session['user_register']['password'])
                    messages.success(request, 'you are now registered !')
                    instance.delete()
                    del request.session['user_register']
                    return redirect('home:home')
                messages.error(request, 'your code time expired !', 'warning')
                return render(request, self.template_name, {'form': form})
            messages.error(request, 'your code is not correct', 'danger')
        return render(request, self.template_name, {'form': form})


class ResendView(View):
    def get(self, request, *args, **kwargs):
        code = randint(10000, 99999)
        OtpCode.objects.create(
            phone_number=request.session['user_register']['phone_number'], code=code)
        send_otp_code(code, request.session['user_register']['phone_number'])
        messages.success(request, 'your code is now sent !')
        return redirect('accounts:user_otp_code')


class UserLoginView(View):
    form_class = forms.UserLoginForm
    template_name = 'accounts/user_login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                phone_number=cd['phone_number'], password=cd['password'])
            if user:
                login(request, user)
                messages.success(request, 'your login was successful')
                return redirect('home:home')
            messages.success(
                request, 'phone number or password is not correct', 'danger')
            return render(request, self.template_name, {'form': self.form_class})
        return render(request, self.template_name, {'form': form})


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home:home')
