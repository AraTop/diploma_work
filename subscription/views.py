from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from payment.models import Payment
from .models import Subscriptions
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from .permissions import AuthorSubPermissionsMixin


class SubscriptionsListView(ListView):
    model = Subscriptions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sub_user = []
        payments = Payment.objects.filter(user=self.request.user).all()
        for item in payments:
            sub = item.subscriptions
            sub_user.append(sub)

        context['sub_user'] = sub_user
        return context


@method_decorator(login_required, name='dispatch')
class SubscriptionsCreateView(CreateView):
    fields = '__all__'
    model = Subscriptions
    template_name = 'subscription/create_subscriptions.html'

    def get_success_url(self) -> str:
        return reverse('main:detail', args=[self.object.channel.name])


@method_decorator(login_required, name='dispatch')
class SubscriptionsUpdateView(AuthorSubPermissionsMixin, UpdateView):
    fields = '__all__'
    model = Subscriptions
    template_name = 'subscription/edit_subscriptions.html'

    def get_success_url(self) -> str:
        return reverse('main:detail', args=[self.object.channel.name])


@method_decorator(login_required, name='dispatch')
class SubscriptionsDetailView(DetailView):
    model = Subscriptions


@method_decorator(login_required, name='dispatch')
class SubscriptionsDeleteView(AuthorSubPermissionsMixin, DeleteView):
    model = Subscriptions

    def get_success_url(self) -> str:
        return reverse('main:detail', args=[self.object.channel.name])
