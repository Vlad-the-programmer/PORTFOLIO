from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
# Auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
# Generic views
from django.views.generic import list, detail, edit

from comments.forms import CommentCreateForm
from comments.models import Comment
from comments.utils import paginateComments
from .models import Post, Tags
from likes.models import Like
from .forms import UpdateForm, CreateForm
from .utils import searchPosts, postsFilter, paginatePosts


class PostsListView(list.ListView):
    queryset = Post.objects.filter(active=True)
    template_name = 'index.html'
    context_object_name = 'posts'
    
    
    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']
        _ , context['filter'] = postsFilter(self.request, self.get_queryset())
        
        if (len(posts) < 5):
            custom_range, page_obj = paginatePosts(self.request, posts, 5) 
        else:                         
            custom_range, page_obj = paginatePosts(self.request, posts, 1)
            
        if self.request.GET.get('content'):
            posts, _ = postsFilter(self.request, self.get_queryset())
            _ , page_obj = paginatePosts(self.request, posts, 5)
        
        # Get post by querying posts by a search_query value
        if self.request.GET.get('search_query'):
            posts, search_query = searchPosts(self.request, self.get_queryset())
            _ , page_obj = paginatePosts(self.request, posts, 5)
            context['search_query'] = search_query
            
        context['page_obj'] = page_obj
        context['custom_range'] = custom_range
        context['posts'] = posts 
        
        print(context)
        return context
    
    
@method_decorator(permission_required("post.add", raise_exception=True), name='dispatch')
class CreatePostView(LoginRequiredMixin, edit.CreateView):
    model = Post
    form_class = CreateForm
    template_name = 'posts/post_create.html'
    
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # if not post.slug:
            #     post.slug = slugify(post.title) # slug - AutoSlugField
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
    
      
class PostDetailView(detail.DetailView):
        model = Post
        template_name = 'posts/post-detail.html'
        slug_url_kwarg = 'slug'
        
        
        def get_object(self):
            _slug = self.kwargs.get('slug', '')
            try:
                post = get_object_or_404(Post, slug=_slug, active=True)
            except Post.DoesNotExist:
                post = None
            print(post)
            return post
        
        
        def delete(self, request, *args, **kwargs):
            self.request = request
            
            post = self.get_object()
            
            if post is None:
                messages.error(request, 'Post does not exist!')    
                return redirect(reverse_lazy("posts:posts-list"))
            return super().delete(request, *args, **kwargs)
    
    
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            post = context['post']
            
            comments = Comment.objects.filter(post=post)
            likes = Like.objects.filter(post__slug=post.slug)
            user_like = likes.filter(author=self.request.user.pk).first()
            
            custom_range, page_obj = paginateComments(self.request, comments, 5)
            
            context['comment_form'] = CommentCreateForm
            context['comments'] = comments
            context['page_obj'] = page_obj
            context['custom_range'] = custom_range
            context['user_like'] = user_like
            context['post_likes'] = likes.count()
            return context
        
 
@method_decorator(permission_required("post.update", raise_exception=True), name='dispatch')       
class PostUpdateView(LoginRequiredMixin, edit.UpdateView):
    template_name = 'posts/post_create.html'
    form_class = UpdateForm
    
    def get_object(self):
        _slug = self.kwargs.get('slug', '')
        try:
            post = get_object_or_404(Post, slug=_slug, active=True)
        except Post.DoesNotExist:
            post = None
        return post
    
    def post(self, request, slug, *args, **kwargs):
        user = request.user
        post = self.get_object()
        
        if post is None:
            messages.error(request, 'Post does not exist!')    
            return redirect(reverse_lazy("posts:posts-list"))
        
        print(request.POST)
        form = UpdateForm(instance=post, data=request.POST, files=request.FILES)
            
        if form.is_valid():
            post = form.save(commit=False)
            print(post)
            post.author = user
            # if not post.slug:
            #     post.slug = slugify(post.title) # slug - AutoSlugField
            post.save()
            
            cleaned_tags = form.cleaned_data.get('tags')
            post.tags.clear()
            
            for cleaned_tag in cleaned_tags:
                tag = Tags.objects.get(title=cleaned_tag.title)
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
        

@method_decorator(permission_required("post.delete", raise_exception=True), name='dispatch')
class PostDeleteView(LoginRequiredMixin, edit.DeleteView):
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('posts:posts-list')
    
    def get_object(self):
        _slug = self.kwargs.get('slug', '')
        try:
            post = get_object_or_404(Post, slug=_slug, active=True)
        except Post.DoesNotExist:
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
            messages.error(self.request, 'Post does not exist!')
            
            context={}
            context['post'] = post
            
            return render(self.request, self.template_name, context)


