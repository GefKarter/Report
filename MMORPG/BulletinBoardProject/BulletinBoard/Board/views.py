from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import ProductFilter
from .forms import NotificationForm, ResponsesForm
from .models import Notification, Responses
from .tasks import send_response, send_response_accept, send_response_reject


class NotificationList(ListView):
    model = Notification
    ordering = '-date_creation', 'rating'
    template_name = 'Board/notification_list.html'
    context_object_name = 'notification_list'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NotificationDetail(DetailView):
    model = Notification
    template_name = 'Board/notification_detail.html'
    context_object_name = 'notification_detail'

    # Настройки низкоуровнего кэширования
    def get_object(self, *args, **kwargs):
        notification = cache.get(f'notification-{self.kwargs["pk"]}',
                        None)

        if not notification:
            notification = super().get_object(queryset=self.queryset)
            cache.set(f'notification-{self.kwargs["pk"]}', notification)

        return notification

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Responses.objects.filter(responses_user=self.request.user,
                                                        responses_advertising=self.object.id)
        context['my_responses'] = Responses.objects.filter(responses_advertising__notification_user=self.request.user)
        return context


class NotificationSearch(ListView):
    model = Notification
    ordering = '-date_creation', 'rating'
    template_name = 'Board/notification_search.html'
    context_object_name = 'search'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NotificationCreate(LoginRequiredMixin, CreateView):
    form_class = NotificationForm
    model = Notification
    template_name = 'Board/notification_create.html'

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.notification_user = self.request.user
        fields.save()
        return super().form_valid(form)


class NotificationUpdate(LoginRequiredMixin, UpdateView):
    form_class = NotificationForm
    model = Notification
    template_name = 'Board/notification_create.html'

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.notification_user = self.request.user
        fields.save()
        return super().form_valid(form)


class NotificationDelete(LoginRequiredMixin, DeleteView):
    model = Notification
    template_name = 'Board/notification_delete.html'
    success_url = reverse_lazy('Board:notification_list')


class ResponsesCreate(LoginRequiredMixin, CreateView):
    form_class = ResponsesForm
    model = Responses
    template_name = 'Board/responses_create.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        ad = Notification.objects.get(id=kwargs['pk'])
        notification_user_email = ad.notification_user.email  # Получаю email автора объявления, что бы использовать его при отправке email
        if form.is_valid():
            resp = form.save(commit=False)
            resp.responses_user = request.user
            resp.responses_advertising = ad
            response_text = resp.text  # Получаю текст отклика из формы, что бы использовать его в email
            ad_id = resp.responses_advertising.id  #  Получаю идентификатор объявления, что бы использовать его в ссылке, в email
            resp.save()
            send_response.delay(response_text, ad_id, notification_user_email)  # Используется таска, для отправки email
            return self.form_valid(form)

    def get_success_url(self):
        return reverse('Board:notification_detail', args=(self.kwargs['pk'],))


class ResponsesUpdate(LoginRequiredMixin, UpdateView):
    form_class = ResponsesForm
    model = Responses
    template_name = 'Board/responses_create.html'
    pk_url_kwarg = 'response_id'

    def dispatch(self, request, *args, **kwargs):
        resp = Responses.objects.get(id=kwargs['response_id'])
        if resp.responses_user != self.request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        responses = form.save(commit=False)
        responses.responses_user = self.request.user
        responses.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Board:notification_detail', args=(self.kwargs['notification_id'],))


class ResponsesDelete(LoginRequiredMixin, DeleteView):
    model = Responses
    template_name = 'Board/responses_delete.html'
    pk_url_kwarg = 'response_id'

    def get_success_url(self):
        return reverse('Board:notification_detail', args=(self.kwargs['notification_id'],))


@login_required
def response_accept(request, response_id, notification_id):
    response = get_object_or_404(Responses, id=response_id)
    response.status = 1  # Изменяем статус на "Подтвержден"
    response.save()
    send_response_accept.delay(response_id)
    return redirect('Board:notification_detail', pk=notification_id)

@login_required
def response_reject(request, response_id, notification_id):
    response = get_object_or_404(Responses, id=response_id)
    response.status = 2  # Изменяем статус на "Отклонен"
    response.save()
    send_response_reject.delay(response_id)
    return redirect('Board:notification_detail', pk=notification_id)


class CategoryList(ListView):
    pass
