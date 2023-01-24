from django.dispatch import receiver
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
# AllAuth
from allauth.account.signals import user_signed_up, email_confirmed
from allauth.account.models import EmailAddress, EmailConfirmation


User = get_user_model()


@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    user.is_active = False
    print('u', user)
    # Group.objects.get(name='BlogManager').user_set.add(user)

    user.save()
    
    email_address = EmailAddress.objects.get_for_user(user, user.email)
    # Sending confirmation
    confirmation=EmailConfirmation.create(email_address)
    confirmation.send(request, signup=True)
    
    messages.add_message(
        request, 
        messages.INFO,
        message=f"Confirmation email has been sent to {user.email}",
    )
     
     
@receiver(email_confirmed)
def email_confirmed_(request, email_address, *args, **kwargs):
    user = User.objects.get(
        email=email_address.email)
    user.is_active = True
    user.save()