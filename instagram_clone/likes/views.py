import logging
from django.db.models.base import Model as Model
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt,csrf_protect
# Auth
from django.contrib.auth import get_user_model
from django.contrib import messages
# Generic class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import detail, edit

from .models import Like
from posts.models import Post
from .forms import LikeCreateDeleteForm


logger = logging.getLogger(__name__)

Profile = get_user_model()


class LikeCreateDeleteView(LoginRequiredMixin, edit.CreateView):
    model = Like
    slug_url_kwarg = 'post_slug'
    context_object_name = 'like'
    template_name = 'posts/post-detail.html'
    form_class = LikeCreateDeleteForm
    
    def get_object(self):
        _slug = self.kwargs.get('post_slug', '')
        print(_slug)
        like, created = Like.objects.get_or_create(    
                                                    post__slug=_slug, 
                                                    author=self.request.user
                                                )
        return like, created
    

    @csrf_protect
    def post(self, request, *args, **kwargs):
        like, created = self.get_object()

        if created:
            like.post = Post.objects.get(slug=self.kwargs.get('post_slug', ''))
            print(like.post.name)
            print(self.kwargs.get('post_slug') or None)
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
        
        # context["post_likes"] = Like.objects.filter(post__slug=_slug).count()
        return context
