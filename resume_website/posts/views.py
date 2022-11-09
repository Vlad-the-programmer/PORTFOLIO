from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .utils import searchPosts
from .models import Post, Tags
from .forms import UpdateForm, CreateForm

class PostsView(ListView):
    queryset = Post.objects.filter(active=True)
    model = Post
    template_name = 'index.html'
    # context_object_name = 'posts'
    
    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts, search_query = searchPosts(self.request)
        # custom_range, projects = paginateProjects(self.request, projects, 6)
        context['search_query'] = search_query
        context['posts'] = posts or self.get_queryset()
        return context
    
    
class PostDetail(DetailView):
        model = Post
        template_name = 'index.html'
        slug_url_kwarg = 'slug'
        
        def get_object(self):
            _slug = self.kwargs.get('slug', '')
            post = Post.objects.filter(active=True).get(slug=_slug)
            return post
        

class PostUpdate(UpdateView):
    model = Post
    template_name = 'post-create.html'
    form_class = UpdateForm
    
    def get_object(self):
        user = self.request.user
        _slug = self.kwargs.get('slug', '')
        post = Post.objects.filter(user=user).get(slug=_slug)
        return post
    
    def post(self, request, slug, *args, **kwargs):
        user = request.user
        post = self.get_object()
        form = UpdateForm(instance=post, data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.slug = post.title
            post.save()
            messages.success(request, 'Updated!')    
            return redirect(reverse('posts:post-detail', kwargs={'slug': post.slug}))
        
        messages.error(request, 'Invalid data!')    
        return redirect(reverse('posts:post-detail', kwargs={'slug': post.slug}))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['form'] = UpdateForm(instance=post)
        return context
    

class DeletePost(DeleteView):
    model = Post
    
    def get_object(self):
        user = self.request.user
        _slug = self.kwargs.get('slug', '')
        post = Post.objects.filter(user=user).get(slug=_slug)
        return post
    
    
class CreatePost(CreateView):
    model = Post
    form_class = CreateForm
    template_name = 'post-create.html'
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            if not post.slug:
                post.slug = post.title
            post.save()
            
            messages.success(request, 'Created!')    
            return redirect(reverse('posts:post-detail', kwargs={'slug': post.slug}))
        
        return redirect(reverse_lazy('post-create'))
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid data!')    
        return redirect(reverse_lazy('posts:post-create'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context
        