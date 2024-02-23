from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.utils.text import slugify
# Auth
from django.contrib.auth import get_user_model
from django.contrib import messages
# Generic class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import detail, edit, list

from .forms import MessageCreateUpdateForm
from .models import Chat, Message

Profile = get_user_model()


class ChatListView(LoginRequiredMixin, list.ListView):
    model = Chat
    template_name = 'chats/chats-list.html'
    context_object_name = 'chats'
        
        
    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)
    
    
    def get_queryset(self):
        return Chat.objects.filter(author=self.request.user)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    
class ChatDetailView(LoginRequiredMixin, detail.DetailView):
    model = Chat
    template_name = 'chats/chat-detail.html'
    context_object_name = 'chat'
    slug_field = 'chat_slug'
    
    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)
    
    def get_object(self):
        slug_ = self.kwargs.get(self.slug_field, '')
        try:
            chat = get_object_or_404(Profile, id=slug_)
        except Chat.DoesNotExist:
            chat = None
        return chat
        
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["_"] = None
        return context
        

class CreateChatView(LoginRequiredMixin, edit.CreateView):
    template_name = 'chats/chat-create.html'
    model = Chat
    context_object_name = 'chat'
    
    
    def post(self, request, *args, **kwargs):
        self.request = request
        messages.success(request, 'Created!')
        return super().post(request, *args, **kwargs)
    
    # Chat chat_to_user_id ??
    def form_valid(self, form):
        chat_to_user_id = self.kwargs.get('chat_to_user_id', '')
        
        chat = form.save(commit=False)
        chat.set_slug()
        chat.author = self.request.user
        chat.chat_to_user = Profile.objects.get(id=chat_to_user_id)
        chat.save()
        return redirect(self.get_success_url())
    
    def get_success_url(self, *args, **kwargs):
        print(kwargs)
        context = self.get_context_data(**kwargs)
        chat = context['chat']
        return chat.get_absolute_url()
      
      
class ChatDeleteView(LoginRequiredMixin, edit.DeleteView):
    model = Chat
    context_object_name = 'chat'
    template_name = 'chats/chats-list.html'
    
    def get_object(self):
        _slug = self.kwargs.get('chat_slug', '')
        try:
            chat = get_object_or_404(Chat, slug=_slug)
        except Chat.DoesNotExist:
            chat = None
        return chat
    
    
    def delete(self, request, *args, **kwargs):
        self.request = request
        return super().delete(request, *args, **kwargs)
    
    
    def get_success_url(self):
        return reverse('chats:user-chats', kwargs={
                                            'user_id': self.request.user.id
                                            }
                        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = Chat.objects.filter(author=self.request.user)
        return context    
    
    
class MessageCreateView(LoginRequiredMixin, edit.CreateView):
    template_name = 'chats/chat-detail.html'
    model = Message
    context_object_name = 'message'
    form_class = MessageCreateUpdateForm
    
    
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Created!')
        return super().post(request, *args, **kwargs)
    
 
    def form_valid(self, form):
        chat = Chat.objects.filter(author=self.request.user)
        
        message = form.save(commit=False)
        message.author = self.request.user
        message.chat = chat
        message.sent_for = chat.chat_to_user
        chat.save()
        return redirect(self.get_success_url())
    
    def get_success_url(self, *args, **kwargs):
        print(kwargs)
        context = self.get_context_data(**kwargs)
        message = context['message']
        return message.chat.get_absolute_url()
        
        
class MessageUpdateView(LoginRequiredMixin, edit.UpdateView):
    template_name = 'chats/chat-detail.html'
    context_object_name = 'message'
    form_class = MessageCreateUpdateForm
    
    
    def get_object(self):
        _slug = self.kwargs.get('slug', '')
        try:
            message = get_object_or_404(Message, slug=_slug)
        except Message.DoesNotExist:
            message = None
        return message
    
    
    def post(self, request, slug, *args, **kwargs):
        message = self.get_object()
        
        print(request.POST)
        form = MessageCreateUpdateForm(
                                        instance=message,
                                        data=request.POST,
                                        files=request.FILES
                                    )
            
        if form.is_valid():
            message = form.save(commit=False)
            print(message)
            
            message.author = request.user
            message.save()
                
            messages.success(request, 'Updated!')    
            return redirect(message.chat.get_absolute_url())
        
        messages.error(request, 'Invalid data!')    
        return redirect(message.chat.get_absolute_url())

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message = self.get_object()
        context['form'] = MessageCreateUpdateForm(instance=message)
        context['chat'] = context['message'].chat
        return context
        
    
    def get_success_url(self, *args, **kwargs):
        print(kwargs)
        context = self.get_context_data(**kwargs)
        message = context['message']
        return message.chat.get_absolute_url()
        

class MessageDeleteView(LoginRequiredMixin, edit.DeleteView):
    model = Message
    context_object_name = 'message'
    template_name = 'chats/chat-detail.html'
    
    def get_object(self):
        _pk = self.kwargs.get('pk', '')
        try:
            message = get_object_or_404(Message, id=_pk)
        except Message.DoesNotExist:
            message = None
        return message
    
    
    def delete(self, request, *args, **kwargs):
        self.request = request
        return super().delete(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat'] = context['message'].chat
        return context
    
    
    def get_success_url(self, *args, **kwargs):
        message = self.get_object()
        return reverse(message.chat.get_absolute_url())
            
    
    
    