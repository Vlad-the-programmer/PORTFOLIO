from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .utils import searchPosts, postsFilter

from comments.forms import CommentCreateForm
from comments.models import Comment
from .models import Post, Tags
from .forms import UpdateForm, CreateForm


class PostsView(ListView):
    queryset = Post.objects.filter(active=True)
    template_name = 'index.html'
    paginate_by = 5
    
    
    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts, filter = postsFilter(self.request, self.get_queryset())
        
        # Get post by querying posts by a search_query value
        search_query = ''
        if self.request.GET.get('search_query'):
            posts, search_query = searchPosts(self.request, self.get_queryset())
            
        context['search_query'] = search_query
        context['posts'] = posts
        context['filter'] = filter
        
        return context
    
    
class CreatePost(CreateView):
    model = Post
    form_class = CreateForm
    template_name = 'posts/post_create.html'
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if not post.slug:
                post.slug = post.title
            post.save()
            
            cleaned_tags = form.cleaned_data.get('tags')
            for title in cleaned_tags:
                tag = Tags.objects.get(title=title)
                post.tags.add(tag)
            
            messages.success(request, 'Created!')    
            return redirect(reverse('posts:post-detail', kwargs={'slug': post.slug}))
        
        return redirect(reverse_lazy('posts:post-create'))
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid data!')    
        return redirect(reverse_lazy('posts:post-create'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context
    
      
class PostDetail(DetailView):
        model = Post
        template_name = 'posts/post-detail.html'
        slug_url_kwarg = 'slug'
        
        def get_object(self):
            _slug = self.kwargs.get('slug', '')
            post = Post.objects.filter(active=True).get(slug=_slug)
            return post
        
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            post = context['post']
            comments = Comment.objects.filter(post=post)
            context['comment_form'] = CommentCreateForm
            context['comments'] = comments
            
            return context
        
        
class PostUpdate(UpdateView):
    template_name = 'posts/post_create.html'
    form_class = UpdateForm
    
    def get_object(self):
        user = self.request.user
        _slug = self.kwargs.get('slug', '')
        post = Post.objects.filter(author=user).get(slug=_slug)
        return post
    
    def post(self, request, slug, *args, **kwargs):
        user = request.user
        post = self.get_object()
        
        print(request.POST)
        form = UpdateForm(instance=post, data=request.POST, files=request.FILES)
            
        if form.is_valid():
            post = form.save(commit=False)
            print(post)
            post.author = user
            post.slug = post.title
            post.save()
            
            cleaned_tags = form.cleaned_data.get('tags')
            for title in cleaned_tags:
                tag = Tags.objects.get(title=title)
                post.tags.add(tag)
                
            messages.success(request, 'Updated!')    
            return redirect(reverse('posts:post-detail', kwargs={'slug': post.slug}))
        
        messages.error(request, 'Invalid data!')    
        return redirect(reverse('posts:post-detail', kwargs={'slug': post.slug}))

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['form'] = UpdateForm(instance=post)
        return context
        

class PostDelete(DeleteView):
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('posts:posts-list')
    
    def get_object(self):
        _slug = self.kwargs.get('slug', '')
        try:
            post = Post.objects.filter(author=self.request.user).get(slug=_slug)
        except:
            post = None
        return post
    
    def delete(self, request, *args, **kwargs):
        self.request = request
        return super().delete(request, *args, **kwargs)
        
    def form_valid(self, form):
        post = self.get_object()
        if post:
            post.delete()
            messages.success(self.request, 'Post deleted!')
            return redirect(self.success_url)
        else:
            context={}
            messages.error(self.request, 'Post does not exist!')
            context['post'] = post
            return render(self.request, self.template_name, context)


