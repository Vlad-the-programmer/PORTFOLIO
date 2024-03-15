from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import edit
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Comment
from posts.models import Post
from .forms import CommentCreateForm, CommentUpdateForm
from . import mixins

class CommentCreateView(LoginRequiredMixin, edit.CreateView):
    model = Comment
    template_name = 'posts/post-detail.html'
    form_class = CommentCreateForm
    
    
    def post(self, request, *args, **kwargs):
        self.request = request
        
        post_data = request.POST.copy()
        post_id = post_data.pop('post_id')[0]
        
        post = Post.objects.get(id=post_id)
        form = CommentCreateForm(data=post_data, files=request.FILES)
        print(form.errors)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            print(comment)
            
            messages.success(request, 'Comment added!')
            return redirect(comment.get_absolute_url())
 
        return redirect(post.get_absolute_url())
    
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid data!')
        return redirect(reverse_lazy('comments:comment-create'))
    
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       comment = self.get_object()
       
       context['comment_form'] = self.form_class
       context['post'] = comment.post
       context['comments'] = Comment.objects.filter(post=comment.post)
       
       return context
   
   
class CommentUpdateView(    
                            LoginRequiredMixin, 
                            mixins.GetCommentObjectMixin,
                            edit.UpdateView
                        ):
    template_name = 'comments/comment_update.html'
    form_class = CommentUpdateForm
    
    
    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        form = CommentUpdateForm(   
                                    instance=comment, 
                                    data=request.POST, 
                                    files=request.FILES
                                )
        if form.is_valid() and comment is not None:
            form.save()
            
            messages.success(request, 'Updated!')
            return redirect(comment.get_absolute_url())
        
        return redirect(reverse('comments:comment-update', kwargs={
                                                            'pk': comment.id
                                                        }
                                )
                        )
    
    
    def form_invalid(self, form):
        comment = self.get_object()
        messages.error(self.request, 'Invalid data!')
        return redirect(reverse('comments:comment-update', kwargs={
                                                            'pk': comment.id
                                                        }
                                )
                        )
    
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       comment = self.get_object()
       print(comment)
       context['update_form'] = self.form_class(instance=comment)
       context['post'] = comment.post
       context['comments'] = Comment.objects.filter(post=comment.post)
       print(context)
       return context
   

class CommentDeleteView(    
                            LoginRequiredMixin, 
                            mixins.GetCommentObjectMixin,
                            edit.DeleteView
                        ):
    template_name = 'comments/comment_delete.html'
        
        
    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        
        if comment is not None:
            comment.delete()
            
            messages.success(request, 'Deleted!')
            return redirect(comment.get_absolute_url())
        
        return redirect('comments:comment-delete', kwargs={
                                                            'pk': comment.id
                                                        }
                        )
            