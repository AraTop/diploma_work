from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from main.models import Post, Subscriptions, Сhannel, Сomments
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse


#------------------------------------------------------------------------------------
class MainListView(ListView):
    model = Сhannel
    template_name = 'main/main_page.html'


@method_decorator(login_required, name='dispatch')
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
            return HttpResponseRedirect(reverse('detail', args=[self.request.user.channel.name]))
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()

        self.request.user.channel = self.object
        self.request.user.save()

        return HttpResponseRedirect(reverse('detail', args=[self.object.name]))
    

@method_decorator(login_required, name='dispatch')
class СhannelDeleteView(DeleteView):
    model = Сhannel


@method_decorator(login_required, name='dispatch')
class СhannelUpdateView(UpdateView):
    model = Сhannel
    fields = '__all__'
    success_url = '/'

#------------------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class SubscriptionsCreateView(CreateView):
    fields = '__all__'
    model = Subscriptions
    template_name = 'main/create_subscriptions.html'
    success_url = '/'


@method_decorator(login_required, name='dispatch')
class SubscriptionsUpdateView(UpdateView):
    fields = '__all__'
    model = Subscriptions
    template_name = 'main/edit_subscriptions.html'
    success_url = '/'


@method_decorator(login_required, name='dispatch')
class SubscriptionsDeleteView(DeleteView):
    model = Subscriptions
    success_url = '/'

#------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    fields = '__all__'
    model = Post
    template_name = 'main/create_post.html'
    success_url = '/'


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    fields = '__all__'
    model = Post
    template_name = 'main/edit_post.html'
    success_url = '/'


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

#-----------------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class СommentsCreateView(CreateView):
    fields = '__all__'
    model = Сomments
    template_name = 'main/create_comments.html'
    success_url = '/'

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
class СommentsDeleteView(DeleteView):
    model = Сomments
    success_url = '/'


@method_decorator(login_required, name='dispatch')
class СommentsUpdateView(UpdateView):
    model = Сomments
    fields = '__all__'
    success_url = '/'

#----------------------------------------------------------------------------

class UpdateLikesView(View):
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id)

        # Получаем текущее количество лайков для данного пользователя
        user_likes_key = f"user_likes_{post_id}"
        user_likes = request.session.get(user_likes_key, 0)

        # Проверяем, был ли уже лайк от данного пользователя
        if user_likes == 0:
            # Увеличиваем количество лайков
            post.likes += 1
            post.save()

            # Устанавливаем флаг, что пользователь поставил лайк
            request.session[user_likes_key] = 1
        else:
            # Уменьшаем количество лайков
            post.likes -= 1
            post.save()

            # Сбрасываем флаг, что пользователь поставил лайк
            request.session[user_likes_key] = 0

        return JsonResponse({'likes': post.likes})