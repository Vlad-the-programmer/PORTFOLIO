from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
# Auth
from django.contrib.auth import get_user_model
from django.contrib import messages
# Generic class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import detail, edit
from django.views.generic.edit import DeleteView, UpdateView

from .models import Chat, Message

Profile = get_user_model()


class ChatDetailView(LoginRequiredMixin, detail.DetailView):
    model = Chat
    template_name = 'chat/chat_detail.html'
    context_object_name = 'chat'
    slug_field = 'chat_slug'
    
    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)
    
    def get_object(self):
        slug_ = self.kwargs.get(self.slug_field, '')
        try:
            chat = get_object_or_404(Profile, id=slug_)
        except:
            chat = None
        return chat
        
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["_"] = None
        return context
        

class CreateChatView(edit.CreateView):
    template_name = 'chats/chat-create.html'
    model = Chat
    
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Created!')
        return super().post(request, *args, **kwargs)
    
    # def get_success_url(self):
    #     return reverse('messages:chat-detail', kwargs={
    #                                                      'chat_slug': self.request.
    #     })
            