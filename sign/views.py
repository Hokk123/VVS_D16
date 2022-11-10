import random

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, View

from .forms import BaseRegisterForm, OTPcodeForm
from .models import NewUserOTP


class UserCreation(TemplateView):
    """Представление для регистрации нового пользователя"""
    template_name = 'sign/signup.html'

    # Добавляем нашу форму регистрации(переменная для шаблона)
    form = BaseRegisterForm
    extra_context = {'form': BaseRegisterForm}

    def post(self, request, *args, **kwargs):
        form = BaseRegisterForm(request.POST)

        if form.is_valid():
            instance_email_name = form.instance.email.split('@')[0]
            signup_username = form.instance.username = f"{instance_email_name}_{random.randint(1, 1000)}"
            deactivated_user = User.objects.filter(email=form.instance.email, is_active=False)

            # Если пользователь не активен, то удалить, если есть активный с такой почтой, то отсылаем на страницу,
            # что такой пользователь уже есть.
            if deactivated_user:
                deactivated_user.delete()
            if User.objects.filter(email=form.instance.email):
                return render(request, template_name='sign/user_already_exists.html',
                              context={'email': form.instance.email}
                              )
            else:
                form.instance.is_active = False
                form.save()
                signup_user = User.objects.filter(username=signup_username).first()
                return HttpResponseRedirect(reverse('otp_page', kwargs={'pk': signup_user.id}))


class OTPVerif(View):
    """Представление проверки одноразового пароля"""

    def post(self, request, *args, **kwargs):
        form = OTPcodeForm(request.POST)
        user_id = self.kwargs.get('pk')
        new_user_obj = NewUserOTP.objects.get(user_id=user_id)
        otp = new_user_obj.otp
        user = User.objects.get(pk=user_id)

        if form.is_valid():
            # Какими бы ни были данные, представленные в форме, как только они будут успешно проверены вызовом
            # is_valid() (и is_valid() вернет True), проверенные данные формы окажутся в словаре form.cleaned_data.
            user_code_answer = form.cleaned_data['code']
            if otp == user_code_answer:  # Сравниваем указанный пользователем код с отправленным
                user.is_active = True
                user.save()
                new_user_obj.delete()  # Удаляем объект NewUserOTP с кодом

                # Отправляем письмо
                send_mail(
                    subject=f'Регистрация на VVS_D16 подтверждена!',
                    message=f'Здравствуйте, {user.username}, спасибо за регистрацию!',
                    from_email='hokk1234@yandex.ru',
                    recipient_list=[user.email]
                )
                return HttpResponseRedirect(reverse('account_login'))
            else:
                user.delete()
                return HttpResponseRedirect(reverse('signup'))

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        user_q = User.objects.filter(pk=user_id)
        # если нет пользователь с таким ID
        if not user_q.exists():
            return HttpResponseRedirect(reverse('signup'))
        # если пользователь с таким ID уже активен
        user = user_q.get()
        if user.is_active:
            return HttpResponseRedirect(reverse('account_login'))

        otp = random.randrange(1000, 9999)
        # Если из-за ошибки NewUserOTP уже будет запись(-и) для юзера с user_id, то ее(их) нужно удалить и созадть заново.
        if NewUserOTP.objects.filter(user_id=user_id).exists():
            NewUserOTP.objects.filter(user_id=user_id).delete()
        NewUserOTP.objects.create(user_id=user_id, otp=otp)

        form = OTPcodeForm()
        send_mail(
            subject=f'Пароль для подтверждения регистрации VVS_D16!',
            message=f'Здравствуйте, {user.email}, ваш пароль: {otp}',
            from_email='hokk1234@yandex.ru',
            recipient_list=[user.email]
        )

        return render(request, 'sign/confirm_otp.html', {'form': form})
