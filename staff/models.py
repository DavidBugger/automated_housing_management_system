from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# class Staff(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     position = models.CharField(max_length=100)
#     is_approving_officer = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.user.username} - {self.position}"
    

# running staff on existing users
# python manage.py shell
# from django.contrib.auth.models import User
# from staff.models import Staff
# for user in User.objects.all():
#     Staff.objects.get_or_create(user=user)



class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approving_officer = models.BooleanField(default=False)
    # ... other fields ...

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_staff(sender, instance, created, **kwargs):
    if created:
        Staff.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_staff(sender, instance, **kwargs):
    instance.staff.save()
    
    
    
    
class LandDocument(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='land_documents/')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_documents')
    approved_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_documents')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
