from main.permissions import AuthorPermissionsMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_list_or_404
from main.models import Сhannel
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from payment.models import Payment
from django.urls import reverse
from post.models import Post, Сomments


class MainListView(ListView):
    model = Сhannel
    template_name = 'main/main_page.html'


class СhannelDetailView(DetailView):
    model = Сhannel

    def get_object(self, queryset=None):
        channel_name = self.kwargs.get('channel_name')
        return Сhannel.objects.get(name=channel_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        channel = self.get_object()
        subscriptions = channel.subscriptions_set.all()
        comments = self.get_comments(channel)
        user = self.request.user if self.request.user.is_authenticated else None
        free_posts = self.get_free_posts(channel)
        payments_channel = Payment.objects.filter(subscriptions__channel=channel).all()

        if user is None:
            paid_posts = self.get_paid_posts(channel)
            context.update({
                'free_posts': free_posts,
                'paid_posts': paid_posts,
                'subscriptions': subscriptions,
                'comments': comments,
            })
            return context

        if user.channel and user.channel.name == channel.name:
            context['all_posts'] = Post.objects.filter(channel=channel)

        payment = Payment.objects.filter(
            user=self.request.user,
            subscriptions__channel=channel
        ).first()

        if payment:
            payments_user, payments_user_not_check = self.get_user_payments(channel, payment)
            context.update({
                'payments_user': payments_user,
                'payments_user_not_check': payments_user_not_check,
            })
        else:
            paid_posts = self.get_paid_posts(channel)
            context['paid_posts'] = paid_posts

        context.update({
            'payments_channel': payments_channel,
            'payment': Payment.objects.filter(user=self.request.user, subscriptions__channel=channel),
            'free_posts': free_posts,
            'subscriptions': subscriptions,
            'comments': comments,
        })
        return context

    def get_comments(self, channel):
        return get_list_or_404(Сomments, post__channel=channel) if Сomments.objects.filter(post__channel=channel).exists() else None

    def get_free_posts(self, channel):
        return Post.objects.filter(subscription_level__isnull=True, channel=channel)

    def get_paid_posts(self, channel):
        return Post.objects.filter(subscription_level__isnull=False, channel=channel)

    def get_user_payments(self, channel, payment):
        user_sub = payment.subscriptions
        payments_user = [item for item in Post.objects.filter(subscription_level__isnull=False, channel=channel)
                         if user_sub.strength_of_subscription >= item.subscription_level.strength_of_subscription]
        payments_user_not_check = [item for item in Post.objects.filter(subscription_level__isnull=False, channel=channel)
                                   if user_sub.strength_of_subscription < item.subscription_level.strength_of_subscription]
        return payments_user, payments_user_not_check


@method_decorator(login_required, name='dispatch')
class СhannelCreateView(CreateView):
    fields = '__all__'
    model = Сhannel
    template_name = 'main/create_channel.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.channel:
            return HttpResponseRedirect(f'/channel/{self.request.user.channel.name}/')
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()

        self.request.user.channel = self.object
        self.request.user.save()

        return HttpResponseRedirect(reverse('main:detail', args=[self.object.name]))


@method_decorator(login_required, name='dispatch')
class СhannelUpdateView(AuthorPermissionsMixin, UpdateView):
    model = Сhannel
    fields = '__all__'

    def get_success_url(self) -> str:
        return reverse('main:detail', args=[self.object.name])
