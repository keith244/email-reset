from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.
class PasswordResetToken(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token      = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default = timezone.now)  
    is_used    = models.BooleanField(default=False)

    def __str__(self):
        return f'Password reset token for {self.user.username}'
    
    class Meta:
        verbose_name_plural = 'Password Reset Tokens'

    @property
    def is_valid(self):
        return not self.is_used and (timezone.now() - self.created_at).total_seconds() < 300
    
