from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView

from feedbacks.model_forms import FeedbackModelForm
from feedbacks.models import Feedback
from project.model_choices import FeedbackCacheKeys


class FeedbackView(FormView):
    form_class = FeedbackModelForm
    template_name = 'feedbacks/create.html'
    success_url = reverse_lazy('feedbacks')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class FeedbackList(ListView):
    template_name = 'feedbacks/index.html'
    model = Feedback
    context_object_name = 'feedbacks'

    def get_queryset(self):
        queryset = cache.get(FeedbackCacheKeys.FEEDBACKS)
        if not queryset:
            queryset = Feedback.objects.all()
            cache.set(FeedbackCacheKeys.FEEDBACKS, queryset)

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset
