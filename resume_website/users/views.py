from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.signals import user_logged_in
# Auth
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Generic class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
# Email verification 
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from .emails_handler import send_verification_email

from .forms import UserCreateForm, UserUpdateForm


Profile = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = form.save(commit=False)
            
            if Profile.get_user_by_email(user.email):
                messages.info(request, 'User already exists!')
                return redirect(reverse_lazy('users:login'))
            
            if not user.username:
                user.username = user.email.split('@')[0]
                
            user.username.lower()
            user.save()
            
            # Sending email activation
            mail_subject = 'Please activate your account'
            template_email = 'accounts/account_verification_email.html'
            send_verification_email(request,
                                    user,
                                    template_email,
                                    mail_subject,
                                    is_activation_email=True)
        else:
            messages.error(request, f'{form.errors}')
            return redirect(reverse_lazy('users:register'))
        
    else:
        form = UserCreateForm()
        
    context = {}
    context['form'] = form
    return render(request, 'auth/register.html', context)
 
 
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Profile.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            
            messages.success(request, 'Congratulations! Your account is activated.')
            return redirect(reverse_lazy('users:login'))
    else:
        messages.error(request, 'Invalid activation link')
        return redirect(reverse_lazy('users:register')) 
    
    
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(
                                username=email,
                                password=password
                            )
        print(user)
        
        if user is not None:
            login(
                    request,
                    user
            )
            
            # Setting the time user logged in at
            user_logged_in.send(sender=user.__class__, request=request, user=user)
            
            messages.success(request, f'Logged in as {user.username}')
            return redirect(reverse('users:profile-detail', kwargs={'pk': user.id}))
        
        messages.error(request, 'Invalid credentials!')
        return redirect(reverse_lazy('users:login'))
    
    return render(request, 'auth/login.html')


class ProfileDetail(LoginRequiredMixin,
                    DetailView
                ):
    model = Profile
    template_name = 'profile/profile_detail.html'
    context_object_name = 'profile'

    
@login_required(login_url='login/')
def logout_user(request):
    logout(request)
    return redirect(reverse_lazy('users:login'))


class ProfileDelete(LoginRequiredMixin,
                    DeleteView
                    ):
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


class ProfileUpdate(LoginRequiredMixin,
                    UpdateView
                    ):
    template_name = 'profile/profile-update.html'
    form_class = UserUpdateForm
    
    
    def get_object(self):
        _pk = self.kwargs.get('pk', '')
        try:
            profile = get_object_or_404(Profile, id=_pk)
        except:
            profile = None
        return profile
    
    def get_success_url(self):
        profile = self.get_object()
        success_url = reverse('users:profile-detail', kwargs={
                                                            'pk': profile.id
                                                        }
                              )
        return success_url
    
    
    def post(self, request, *args, **kwargs):
        self.request = request
        profile = self.get_object()
        if profile:
            form = UserUpdateForm(instance=profile, data=request.POST, files=request.FILES)
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
    

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Profile.get_user_by_email(email=email):
            user = Profile.objects.get(email__exact=email)
             # Reset password email
            mail_subject = 'Reset Your Password'
            
            template_email = 'accounts/reset_password_email.html'
            send_verification_email(request, user, template_email, mail_subject)
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('users:login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('users:forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def reset_password_validate(request, pk):
    try:
        user = Profile.objects.get(id=pk)
    except (Profile.DoesNotExist, ValueError):
        user = None

    if user is not None:
        messages.success(request, 'Please reset your password')
        return redirect(reverse('users:resetPassword', kwargs={'pk': pk}))
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('users:login')


def resetPassword(request, pk):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            user = Profile.objects.get(id=pk)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('users:login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect(reverse('users:resetPassword', kwargs={'pk': pk}))
    else:
        return render(request, 'accounts/resetPassword.html', context={'pk': pk})
        
