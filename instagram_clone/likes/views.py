import logging
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.http import Http404
# Auth
from django.contrib.auth import get_user_model
from django.contrib import messages
# Generic class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import edit

from .models import Like, Dislike
from posts.models import Post
from .forms import LikeCreateDeleteForm
from comments.models import Comment
from comments.utils import paginateComments
from comments.forms import CommentCreateForm

logger = logging.getLogger(__name__)

Profile = get_user_model()


class LikeCreateView(LoginRequiredMixin, edit.CreateView):
    model = Like
    slug_url_kwarg = 'post_slug'
    context_object_name = 'like'
    template_name = 'posts/post-detail.html'
    # form_class = LikeCreateDeleteForm
    
    
    def get_object(self):
        try:
            post = Post.objects.get(slug= self.kwargs.get('post_slug', ''))
        except Post.DoesNotExist:
            post = None
        print("Post liked", post)
        
        if post is None:
            return Http404("Post not found")
        
        like, created = Like.objects.get_or_create( 
                                                    post=post, 
                                                    author=self.request.user
                                                )
        print("Like", like)
        
        return like, created, post
    
    
    def post(self, request, *args, **kwargs):
        self.request = request
        like, created, post = self.get_object()
        print("Created", created)
        
        if created:
            print("Create like post: ", like.post.title)
            print("Post slug ", self.kwargs.get('post_slug') or None)
            like.post = post
            like.author = request.user
            like.save()
            logger.info(f"Like created by {like.author.username} \
                                for post {like.post.title}"
                        )
            return redirect(self.get_success_url())
        return redirect(self.get_success_url())
        
    
    def form_valid(self, form):
        like, created, _ = self.get_object()
        if created:
            logger.info(f"Like created by {like.author.username} \
                                        for post {like.post.title}"
                        )
        return self.get_success_url()
    
    
    def get_success_url(self):
        like, _, post = self.get_object()
        return post.get_absolute_url()
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        like, _, post = self.get_object()
        context['post'] = post
        
        likes = Like.objects.filter(post__slug=post.slug).all()
        user_like = like
        
        context['user_like'] = user_like
        context['post_likes'] = likes.count()
        return context


class DislikeCreateView(LoginRequiredMixin, edit.DeleteView):
    model = Dislike
    slug_url_kwarg = 'post_slug'
    context_object_name = 'dislike'
    template_name = 'posts/post-detail.html'
    # form_class = LikeCreateDeleteForm
    
    
    def get_object(self):
        try:
            post = Post.objects.get(slug= self.kwargs.get('post_slug', ''))
        except Post.DoesNotExist:
            post = None
        print("Post disliked", post)
        
        if post is None:
            return Http404("Post not found")
        
        dislike, created = Dislike.objects.get_or_create(  
                                                      post=post,
                                                      author=self.request.user
                                                    )
        print("Dislike", dislike)
        dislikes = Dislike.objects.filter(post__slug=post.slug).all()
        print("Dislikes: ", dislikes)
        return dislike, created, post
    
    
    def post(self, request, *args, **kwargs):
        self.request = request
        dislike, created, post = self.get_object()
        print("Created", created)
        
        if created:
            print("Create dislike post: ", dislike.post.title)
            print("Post slug ", self.kwargs.get('post_slug') or None)
            dislike.post = post
            dislike.author = request.user
            dislike.save()
            logger.info(f"Dislike created by {dislike.author.username} \
                                for post {dislike.post.title}"
                        )
            return redirect(self.get_success_url())
        return redirect(self.get_success_url())
        
    
    def form_valid(self, form):
        dislike, created, _ = self.get_object()
        if created:
            logger.info(f"Dislike created by {dislike.author.username} \
                                        for post {dislike.post.title}"
                        )
        return self.get_success_url()
    
    
    def get_success_url(self):
        dislike, _, post = self.get_object()
        return post.get_absolute_url()
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        dislike, _, post = self.get_object()
        context['post'] = post
        
        dislikes = Dislike.objects.filter(post__slug=post.slug).all()
        user_dislike = dislike

        context['user_dislike'] = user_dislike
        context['post_dislikes'] = dislikes.count()
        return context
