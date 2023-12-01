from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.urls import reverse
from post.models import Post, Сomments
from post.permissions import AuthorCommentPermissionsMixin, AuthorPostPermissionsMixin
from django.views import View
import datetime


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    fields = '__all__'
    model = Post
    template_name = 'post/create_post.html'

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
    template_name = 'post/edit_post.html'

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

# -----------------------------------------------------------------------------------


@method_decorator(login_required, name='dispatch')
class СommentsCreateView(CreateView):
    fields = '__all__'
    model = Сomments
    template_name = 'post/create_comments.html'

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

# ----------------------------------------------------------------------------


@method_decorator(login_required, name='dispatch')
class UpdateLikesView(View):
    template_name = 'post/update_likes.html'

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
