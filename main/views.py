from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from main.models import Post, Subscriptions, Сhannel
from django.http import HttpResponseRedirect
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
        context['subscriptions'] = subscriptions
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