from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from emails.models import PasswordResetToken
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.
User = get_user_model()

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user   = User.objects.get(email= email)
            token  = get_random_string(length=32)

            PasswordResetToken.objects.create( user=user, token=token)

            reset_link = f'http://{request.get_host()}/password_reset_confirm/{token}'

            html_message  = render_to_string('emails/password_reset_email.html', {'reset_link':reset_link})
            plain_message = strip_tags(html_message)

            send_mail(
                'Password Reset Request',
                plain_message,
                'from@example.com',
                [email],
                html_message= html_message,
                fail_silently = False,
            )
            messages.success(request, 'Password reset link has been sent to your email.')
        except User.DoesNotExist:
            messages.error(request, 'No user with the email found')
        return redirect('password_reset')
    return render(request, 'emails/password_reset.html')

def password_reset_confirm(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)

        if not reset_token.is_valid:
            messages.error(request, 'This reset link is expired or invalid.')
            return redirect('login')
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('cofirm_password')

            if new_password == confirm_password:
                user = reset_token.user
                user.password = make_password(new_password)
                user.save()

                reset_token.is_used = True
                reset_token.save()

                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Password do not match')

        return render(request, 'emails/password_reset_confirm.html')    

    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid password reset link')
        return redirect('login')