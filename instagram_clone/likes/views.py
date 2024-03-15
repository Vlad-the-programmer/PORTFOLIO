import logging
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt,csrf_protect
# Auth
from django.contrib.auth import get_user_model
from django.contrib import messages
# Generic class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import edit

from .models import Like
from posts.models import Post
from .forms import LikeCreateDeleteForm
from comments.models import Comment
from comments.utils import paginateComments
from comments.forms import CommentCreateForm


logger = logging.getLogger(__name__)

Profile = get_user_model()


class LikeCreateDeleteView(LoginRequiredMixin, edit.CreateView):
    model = Like
    slug_url_kwarg = 'post_slug'
    context_object_name = 'like'
    template_name = 'posts/post-detail.html'
    form_class = LikeCreateDeleteForm
    
    
    def get_object(self):
        try:
            post = Post.objects.get(slug= self.kwargs.get('post_slug', ''))
        except Post.DoesNotExist:
            post = None
        print("Post liked", post)
        
        if post is None:
            return Http404("Post not found")
        
        likes = Like.objects.filter(post=post, author=self.request.user).all()
        print("Likes", likes)
        created = False
        like = None
        if likes.count() == 1:
            like = likes.first()
        elif likes.count() == 0:
            created = True
            like = Like.objects.create(post=post, author=self.request.user)
        
        return like, created
    
    
    def post(self, request, *args, **kwargs):
        self.request = request
        like, created = self.get_object()
        print("Created", created)
        if created:
            like.post = Post.objects.get(slug=self.kwargs.get('post_slug', ''))
            print("Create like post: ", like.post.title)
            print("Post slug ", self.kwargs.get('post_slug') or None)
            like.author = request.user
            like.save()
            logger.info(f"Like created by {like.author.username} \
                                for post {like.post.title}"
                        )
            return redirect(self.get_success_url())
        else:
            like.delete()
            messages.success(request, f"Like deleted for {like.post.title}")
            
        return redirect(self.get_success_url())
    
    
    def get_success_url(self):
        like, _ = self.get_object()
        return like.post.get_absolute_url()
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _slug = self.kwargs.get('post_slug', '')
        
        context['post'] = Post.objects.get(slug=_slug)
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
