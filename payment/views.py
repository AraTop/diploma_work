from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponseServerError
import stripe
from .models import Payment
from project import settings
from main.models import Subscriptions
from users.models import User
import datetime
from django.shortcuts import get_object_or_404, redirect, render


@method_decorator(login_required, name='dispatch')
class PaymentRetrieveView(View):
    template_name = 'payment/retrieve_payment.html'

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
            return render(request, 'payment/add_nickname.html')

        if request.user.channel:
            if subscrip.channel.name == request.user.channel.name:
                return render(request, 'payment/error_payment_mychannel.html')

        if existing_payment:

            for item in existing_payment:
                if item.subscriptions.channel.name == subscrip.channel.name:
                    subscriptions_user = item.subscriptions

                    if subscrip == subscriptions_user:
                        return render(request, 'payment/error_payment.html', {'subscription': subscrip})

                    item.delete()

                    subscriptions = Subscriptions.objects.get(pk=pk)
                    amount = subscriptions.amount_per_month

                    five_percent = amount * 0.05
                    amount_after_deduction = amount - five_percent
                    # нужно вписать почту хозяина сайта чтоб 5 процентов уходило ему на счет с каждой покупки
                    admin_user = User.objects.filter(email='lololohka057@gmail.com').first()
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
                    return redirect('payment:retrieve', payment_intent_id=payment_intent_id)

                else:
                    # Если у пользователя нет подписки на этот канал,
                    # создаем новую подписку
                    subscriptions = get_object_or_404(Subscriptions, pk=pk)
                    amount = subscriptions.amount_per_month

                    five_percent = amount * 0.05
                    amount_after_deduction = amount - five_percent

                    admin_user = User.objects.filter(email='lololohka057@gmail.com').first()
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

                    return redirect('payment:retrieve', payment_intent_id=payment_intent_id)
        else:
            subscriptions = get_object_or_404(Subscriptions, pk=pk)
            amount = subscriptions.amount_per_month

            five_percent = amount * 0.05
            amount_after_deduction = amount - five_percent

            admin_user = User.objects.filter(email='lololohka057@gmail.com').first()
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

            return redirect('payment:retrieve', payment_intent_id=payment_intent_id)
