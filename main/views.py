import datetime
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


#------------------------------------------------------------------------------------
class MainListView(ListView):
    model = Сhannel
    template_name = 'main/main_page.html'


#@method_decorator(login_required, name='dispatch')
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
        payments = Payment.objects.all()
        user = self.request.user if self.request.user.is_authenticated else None
        
        if user == None:
            context['subscriptions'] = subscriptions
            context['comments'] = comments
            return context
        
        for item in payments:
            if user.nickname == item.user_nickname:
                context['its_me'] = item
                break
            else:
                context['its_me'] = None
                break

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

@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    fields = '__all__'
    model = Post
    template_name = 'main/create_post.html'
    
    def get_success_url(self) -> str:
        return reverse('main:detail', args=[self.object.channel.name])


@method_decorator(login_required, name='dispatch')
class PostUpdateView(AuthorPostPermissionsMixin, UpdateView):
    fields = '__all__'
    model = Post
    template_name = 'main/edit_post.html'
    
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
        for item in Payment.objects.all():
            if request.user.nickname == item.user_nickname:
                return render(request, 'main/error_payment.html', {'item':item})
        try:
            subscriptions = Subscriptions.objects.get(pk=pk)
            print('fsdfsd   ')
            amount = subscriptions.amount_per_month
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
        except stripe.error.StripeError as e:
            print(f"Ошибка Stripe: {e}")

        return render(request, self.template_name)