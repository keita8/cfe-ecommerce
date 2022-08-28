from datetime import timezone
from datetime import datetime
# from tabnanny import verbose
from time import timezone
from django.db import models

class GuestEmail(models.Model):
    email = models.EmailField(max_length=255)

    
    class Meta:
        verbose_name = 'Invité'
        verbose_name_plural = 'Invités'
        
    def __str__(self):
        return f" {self.email} "