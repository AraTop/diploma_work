import datetime
from typing import Any
from main.permissions import AuthorCommentPermissionsMixin, AuthorPermissionsMixin, AuthorPostPermissionsMixin, AuthorSubPermissionsMixin
from project import settings
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from main.models import Payment, Post, Subscriptions, Сhannel, Сomments
from django.http import HttpResponseRedirect, HttpResponseServerError, JsonResponse
from django.urls import reverse
import stripe

from users.models import User


#------------------------------------------------------------------------------------
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
        comments = get_list_or_404(Сomments, post__channel=channel) if Сomments.objects.filter(post__channel=channel).exists() else None
        user = self.request.user if self.request.user.is_authenticated else None
        free_posts = Post.objects.filter(subscription_level__isnull=True, channel=channel)
        payments_channel = Payment.objects.filter(subscriptions__channel=channel).all()

        if user == None:
            paid_posts = Post.objects.filter(subscription_level__isnull=False, channel=channel)
            context['free_posts'] = free_posts
            context['paid_posts'] = paid_posts
            context['subscriptions'] = subscriptions
            context['comments'] = comments
            return context
        
        payment = Payment.objects.filter(
            user_nickname=self.request.user.nickname,
            subscriptions__channel=channel
            ).first()
        
        if user.channel:
            if user.channel.name == channel.name:
                context['all_posts'] = Post.objects.filter(channel=channel)
        
        if payment:
            user_sub = payment.subscriptions
            payments_user = []
            payments_user_didnt_check = []

            for item in Post.objects.filter(subscription_level__isnull=False, channel=channel):
                if user_sub.strength_of_subscription >= item.subscription_level.strength_of_subscription:
                    payments_user.append(item)

                else:
                    payments_user_didnt_check.append(item)

            context['payments_user'] = payments_user
            context['payments_user_not_check'] = payments_user_didnt_check

        else:
            paid_posts = Post.objects.filter(subscription_level__isnull=False, channel=channel)
            context['paid_posts'] = paid_posts

        context['payments_channel'] = payments_channel
        context['payment'] = Payment.objects.filter(user_nickname=self.request.user.nickname, subscriptions__channel=channel)
        context['free_posts'] = free_posts
        context['subscriptions'] = subscriptions
        context['comments'] = comments
        return context


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

#------------------------------------------------------------------------------------
class SubscriptionsListView(ListView):
    model = Subscriptions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sub_user = []
        payments = Payment.objects.filter(user_nickname=self.request.user.nickname).all()
        for item in payments:
            sub = item.subscriptions
            sub_user.append(sub)

        context['sub_user'] = sub_user
        return context


@method_decorator(login_required, name='dispatch')
class SubscriptionsCreateView(CreateView):
    fields = '__all__'
    model = Subscriptions
    template_name = 'main/create_subscriptions.html'

    def get_success_url(self) -> str:
        return reverse('main:detail', args=[self.object.channel.name])

@method_decorator(login_required, name='dispatch')
class SubscriptionsUpdateView(AuthorSubPermissionsMixin, UpdateView):
    fields = '__all__'
    model = Subscriptions
    template_name = 'main/edit_subscriptions.html'
    
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

#------------------------------------------------------------------
from django.utils import timezone
@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    fields = '__all__'
    model = Post
    template_name = 'main/create_post.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        moscow_time = timezone.now() + datetime.timedelta(hours=3)
        current_date = timezone.now().date()
        formatted_date = current_date.strftime('%Y-%m-%d')
        context['time'] = moscow_time.time()
        context['date'] = formatted_date
        return context

    def get_success_url(self) -> str:
        return reverse('main:detail', args=[self.object.channel.name])


@method_decorator(login_required, name='dispatch')
class PostUpdateView(AuthorPostPermissionsMixin, UpdateView):
    fields = '__all__'
    model = Post
    template_name = 'main/edit_post.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        moscow_time = timezone.now() + datetime.timedelta(hours=3)
        current_date = timezone.now().date()
        formatted_date = current_date.strftime('%Y-%m-%d')
        context['time'] = moscow_time.time()
        context['date'] = formatted_date
        return context

    def get_success_url(self) -> str:
        return reverse('main:detail', args=[self.object.channel.name])


@method_decorator(login_required, name='dispatch')
class PostDeleteView(AuthorPostPermissionsMixin, DeleteView):
    model = Post
    
    def get_success_url(self) -> str:
        return reverse('main:detail', args=[self.object.channel.name])

#-----------------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class СommentsCreateView(CreateView):
    fields = '__all__'
    model = Сomments
    template_name = 'main/create_comments.html'
    
    def get_success_url(self) -> str:
        return reverse('main:detail', args=[self.object.post.channel.name])

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = post
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        context['post_my'] = post
        moscow_time = timezone.now() + datetime.timedelta(hours=3)
        current_date = timezone.now().date()
        formatted_date = current_date.strftime('%Y-%m-%d')
        context['time'] = moscow_time.time()
        context['date'] = formatted_date
        return context


@method_decorator(login_required, name='dispatch')
class СommentsDeleteView(AuthorCommentPermissionsMixin, DeleteView):
    model = Сomments
    
    def get_success_url(self) -> str:
        return reverse('main:detail', args=[self.object.post.channel.name])


@method_decorator(login_required, name='dispatch')
class СommentsUpdateView(AuthorCommentPermissionsMixin, UpdateView):
    model = Сomments
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        moscow_time = timezone.now() + datetime.timedelta(hours=3)
        current_date = timezone.now().date()
        formatted_date = current_date.strftime('%Y-%m-%d')
        context['time'] = moscow_time.time()
        context['date'] = formatted_date
        return context
    
    def get_success_url(self) -> str:
        return reverse('main:detail', args=[self.object.post.channel.name])

#----------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class UpdateLikesView(View):
    template_name = 'main/update_likes.html' 

    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id)

        user_likes_key = f"user_likes_{post_id}"
        user_likes = request.session.get(user_likes_key, 0)

        if user_likes == 0:
            post.likes += 1
            post.save()

            request.session[user_likes_key] = 1
        else:
            post.likes -= 1
            post.save()

            request.session[user_likes_key] = 0

        redirect_url = reverse('main:detail', args=[post.channel.name])
        return render(request, self.template_name, {'redirect_url': redirect_url})
    

@method_decorator(login_required, name='dispatch')
class PaymentRetrieveView(View):
    template_name = 'main/retrieve_payment.html'

    def get(self, request, payment_intent_id):
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            payment_info = {
                "id": payment_intent.id,
                "amount": payment_intent.amount,
                "currency": payment_intent.currency,
            }
            return render(request, self.template_name, {'payment_info': payment_info})
        except stripe.error.StripeError as e:
            print(f"Ошибка Stripe: {e}")
            return HttpResponseServerError("Ошибка Stripe")


@method_decorator(login_required, name='dispatch')
class PaymentCreateView(View):
    template_name = 'main/create_payment.html'

    def post(self, request, pk):
        existing_payment = Payment.objects.filter(user_nickname=request.user.nickname).all()
        subscrip = Subscriptions.objects.get(pk=pk)
        
        if request.user.nickname:
            pass
        else:
            return render(request, 'main/add_nickname.html')

        if request.user.channel:
            if subscrip.channel.name == request.user.channel.name:
                return render(request, 'main/error_payment_mychannel.html')

        if existing_payment:

            for item in existing_payment:
                if item.subscriptions.channel.name == subscrip.channel.name:
                    subscriptions_user = item.subscriptions

                    if subscrip == subscriptions_user:
                        return render(request, 'main/error_payment.html', {'subscription':subscrip})

                    item.delete()

                    subscriptions = Subscriptions.objects.get(pk=pk)
                    amount = subscriptions.amount_per_month

                    five_percent = amount * 0.05
                    amount_after_deduction = amount - five_percent

                    admin_user = User.objects.filter(email='lololohka057@gmail.com').first() # нужно вписать почту хозяина сайта чтоб 5 процентов уходило ему на счет с каждой покупки
                    if admin_user:
                        admin_user.balance += five_percent
                        admin_user.save()

                    for user in User.objects.all():
                        if user.channel == subscriptions.channel:
                            user.balance += amount_after_deduction
                            user.save()

                    currency = 'RUB'
                    stripe.api_key = settings.STRIPE_SECRET_KEY
                    payment_intent = stripe.PaymentIntent.create(
                        amount=amount * 100,
                        currency=currency,
                        payment_method_types=['card'])
                        
                    payment_intent_id = payment_intent.id
                    payment = Payment(
                        user_nickname=request.user.nickname,
                        payment_date=datetime.date.today(),
                        subscriptions=subscriptions,
                        amount=amount * 100,
                        payment_method='Stripe')
                        
                    payment.save()
                    return redirect('main:retrieve', payment_intent_id=payment_intent_id)
                        
                else: 
                    # Если у пользователя нет подписки на этот канал,
                    # создаем новую подписку
                    subscriptions = get_object_or_404(Subscriptions, pk=pk)
                    amount = subscriptions.amount_per_month

                    five_percent = amount * 0.05
                    amount_after_deduction = amount - five_percent

                    admin_user = User.objects.filter(email='lololohka057@gmail.com').first() # нужно вписать почту хозяина сайта чтоб 5 процентов уходило ему на счет с каждой покупки
                    if admin_user:
                        admin_user.balance += five_percent
                        admin_user.save()

                    for user in User.objects.all():
                        if user.channel == subscriptions.channel:
                            user.balance += amount_after_deduction
                            user.save()

                    currency = 'RUB'
                    stripe.api_key = settings.STRIPE_SECRET_KEY
                    payment_intent = stripe.PaymentIntent.create(
                        amount=amount * 100,
                        currency=currency,
                        payment_method_types=['card']
                        )

                    payment_intent_id = payment_intent.id
                    payment = Payment(
                        user_nickname=request.user.nickname,
                        payment_date=datetime.date.today(),
                        subscriptions=subscriptions,
                        amount=amount * 100,
                        payment_method='Stripe'
                    )
                    payment.save()

                    return redirect('main:retrieve', payment_intent_id=payment_intent_id)
        else:
            subscriptions = get_object_or_404(Subscriptions, pk=pk)
            amount = subscriptions.amount_per_month

            five_percent = amount * 0.05
            amount_after_deduction = amount - five_percent

            admin_user = User.objects.filter(email='lololohka057@gmail.com').first() # нужно вписать почту хозяина сайта чтоб 5 процентов уходило ему на счет с каждой покупки
            if admin_user:
                admin_user.balance += five_percent
                admin_user.save()

            for user in User.objects.all():
                if user.channel == subscriptions.channel:
                    user.balance += amount_after_deduction
                    user.save()

            currency = 'RUB'
            stripe.api_key = settings.STRIPE_SECRET_KEY
            payment_intent = stripe.PaymentIntent.create(
                amount=amount * 100,
                currency=currency,
                payment_method_types=['card']
                )

            payment_intent_id = payment_intent.id
            payment = Payment(
                user_nickname=request.user.nickname,
                payment_date=datetime.date.today(),
                subscriptions=subscriptions,
                amount=amount * 100,
                payment_method='Stripe'
            )
            payment.save()

            return redirect('main:retrieve', payment_intent_id=payment_intent_id)