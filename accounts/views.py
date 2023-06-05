from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.core.cache import cache
from django.views.generic import FormView, ListView, RedirectView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView as AuthLoginView

from accounts.forms import UserUpdateForm
from accounts.model_forms import RegistrationForm, AuthenticationForm, User


class RegistrationView(FormView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('main')
    email_template_name = "registration/registration_email.html"
    extra_email_context = None
    from_email = None
    html_email_template_name = None
    token_generator = default_token_generator

    def form_valid(self, form):
        messages.success(self.request,
                         _('We will send email with registration link. '
                           'Please follow link and continue your '
                           'registration flow.'))
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


class RegistrationConfirmView(RedirectView):
    url = reverse_lazy('login')

    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )
        self.user = self.get_user(kwargs["uidb64"])
        if self.user is None:
            raise Http404
        if not default_token_generator.check_token(self.user, kwargs["token"]):
            raise Http404
        return super().dispatch(*args, **kwargs)

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
                TypeError,
                ValueError,
                OverflowError,
                User.DoesNotExist,
                ValidationError,
        ):
            user = None
        return user

    def get(self, request, *args, **kwargs):
        self.user.is_active = True
        self.user.save()
        return super().get(request, *args, **kwargs)


class LoginView(AuthLoginView):
    form_class = AuthenticationForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        messages.success(self.request, _('Welcome back!'))
        return super().form_valid(form)


class ProfileListView(LoginRequiredMixin, ListView):
    template_name = 'profile/profile.html'
    context_object_name = 'user'
    form_class = UserUpdateForm

    def get_queryset(self):
        return User.objects.filter(email=self.request.user.email)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = self.form_class(
                self.request.POST, instance=self.get_queryset().first())
        else:
            context['form'] = self.form_class(
                instance=self.get_queryset().first())
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,
                               instance=self.get_queryset().first())
        if form.is_valid():
            user = form.save(commit=False)
            if form.has_changed() and 'phone' in form.changed_data:
                user.is_phone_valid = False
            user.save()
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('profile')


class VerificationPhoneView(LoginRequiredMixin, View):
    def get(self, request):
        phone = request.user.phone
        cache_key = f'verify_code_{phone}'

        code = '1234'

        cache.set(cache_key, code, timeout=60)

        return render(request, 'profile/verification_phone.html',
                      {'user': request.user})

    def post(self, request):
        code = request.POST.get('code')
        phone = request.POST.get('phone')
        cache_key = f'verify_code_{phone}'

        saved_code = cache.get(cache_key)

        if code == saved_code:
            request.user.is_phone_valid = True
            request.user.save()

            cache.delete(cache_key)
            messages.success(request, 'Phone number is verify!')
            return HttpResponseRedirect(reverse('profile'))
        else:
            messages.error(
                request, 'The code is not correct, you can replace!')
            return HttpResponseRedirect(reverse('verify_phone'))
