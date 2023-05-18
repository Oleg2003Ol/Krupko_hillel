from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from project import settings
from django.core.mail import send_mail
from .forms import ContactForm
from .models import Config


class MainView(TemplateView):
    template_name = 'main/index.html'


class ContactFormView(FormView):
    template_name = 'main/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        message = form.cleaned_data['message']

        config = Config()
        send_mail(
            'New Contact Form Submission',
            f'Name: {name}\nMessage: {message}',
            settings.DEFAULT_FROM_EMAIL,
            [config.contact_form_email],
            fail_silently=False,
        )
        messages.success(self.request, 'Messages sent!')
        return super().form_valid(form)

