from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
# Auth
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Generic class-based views
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView

from .forms import UserCreateForm, UserLoginForm, UserUpdateForm
# from .models import Profile

Profile = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST or None)
        
        if form.is_valid():
            user = form.save(commit=False)
            if Profile.get_user_by_email(user.email):
                messages.info(request, 'User already exists!')
                return redirect(reverse_lazy('users:login'))
            user.username.lower()
            user.is_active = True
            user.is_stuff = True
            
            user.save()
            
            messages.success(request, 'Account created!')
            return redirect(reverse('users:login'))
        
        messages.error(request, 'Enter valid data!')
        return redirect(reverse_lazy('users:register'))
    else:
        context = {}
        form = UserCreateForm()
        context['form'] = form
        return render(request, 'auth/register.html', context)
    
    
def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST or None)
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Logged in as {user.username}')
            return redirect(reverse('users:profile-detail', kwargs={'pk': user.id}))
        
        messages.error(request, 'User does not exist!')
        return redirect(reverse_lazy('users:register'))
    else:    
        form = UserLoginForm()
    context = {}
    context['form'] = form
    return render(request, 'auth/login.html', context)
    
class ProfileDetail(DetailView):
    model = Profile
    template_name = 'profile/profile_detail.html'
    context_object_name = 'profile'
    

def logout_user(request):
    logout(request)
    return redirect(reverse_lazy('users:login'))


class ProfileDelete(DeleteView):
    template_name = 'profile/profile_delete.html'
    success_url = reverse_lazy('users:register')
    
    def get_object(self):
        _pk = self.kwargs.get('pk', '')
        # print(self.kwargs, _pk)
        try:
            profile = Profile.objects.get(pk=_pk)
        except:
            profile = None
        return profile
    
    def delete(self, request, *args, **kwargs):
        self.request = request
        return super().delete(request, *args, **kwargs)
        
    def form_valid(self, form):
        profile = self.get_object()
        if profile:
            profile.delete()
            messages.success(self.request, 'Profile deleted!')
            return redirect(self.success_url)
        else:
            context={}
            messages.error(self.request, 'Profile does not exist!')
            context['profile'] = profile
            return render(self.request, self.template_name, context)

class ProfileUpdate(UpdateView):
    model = Profile
    template_name = 'profile/profile-update.html'
    form_class = UserUpdateForm
    
    def get_object(self):
        _pk = self.kwargs.get('pk', '')
        try:
            profile = Profile.objects.get(id=_pk)
        except:
            profile = None
        return profile
    
    def get_success_url(self):
        profile = self.get_object()
        success_url = reverse('profile-detail', kwargs={
                                                            'pk': profile.id
                                                        }
                              )
        return success_url
    # needs to be improved
    def post(self, request, *args, **kwargs):
        self.request = request
        profile = self.get_object()
        if profile:
            form = UserUpdateForm(instance=profile, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Updated!')
                return redirect(self.get_success_url())
            else:
                context={}
                form = UserUpdateForm()
                context['form'] = form
            messages.error(request, 'Invalid data!')    
            return redirect(reverse('profile-update'), kwargs={'pk': profile.id})
        
        messages.error(request, 'Profile does not exist!') 
        return render(request, self.template_name, context)
    