from django.db import models
import uuid
from django.conf import settings
from users.models import Profile, Location, User
from django.contrib.auth.models import User
from .utils import user_property_directory_path
from django.core.mail import send_mail
from .consts import PROPERTY_TYPES, SOLD_CHOICES
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class Property(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
    ]


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=100, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    property_photo = models.ImageField(upload_to=user_property_directory_path)
    property_location = models.CharField(max_length=100, blank=False)
    year_built = models.DateField()
    price = models.CharField(max_length=20, blank=False)
    garages = models.BigIntegerField()
    plot_size = models.CharField(max_length=200, blank=False)
    area = models.CharField(max_length=200, blank=False)
    bathroom = models.CharField(max_length=20, blank=False)
    bedroom = models.CharField(max_length=20, blank=False)
    color = models.CharField(max_length=24, default='White')
    description = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    is_sold = models.BooleanField(choices=SOLD_CHOICES, default=False)
    
    def __str__(self):
        return f'{self.seller.users.username} \'s Listing '
    

class LikedListing(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    listing = models.ForeignKey(Property, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.listing.property_name} listing liked by {self.profile.users.username}'
    



class PurchasedProperty(models.Model):

    property_name = models.CharField(max_length=100)
    property_type = models.CharField(max_length=5, choices=PROPERTY_TYPES)
    house_type = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100, db_index=True)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    size_unit = models.CharField(max_length=20)
    purchase_date = models.DateField()
    price = models.DecimalField(max_digits=15, decimal_places=2)

    @property
    def purchase_month(self):
        return self.purchase_date.strftime('%B')

    def __str__(self):
        return f"{self.property_name} in {self.city}"

    class Meta:
        indexes = [
            models.Index(fields=['purchase_date'], name='purchase_date_idx'),
        ]
        verbose_name_plural = "Properties"
        

class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="inquiries")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Render the HTML email template
        html_content = render_to_string('emails/inquiry_email.html', {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'message': self.message,
            'property_name': self.property.property_name,
        })

        # Create the email
        email = EmailMultiAlternatives(
            subject=f"Inquiry for {self.property.property_name}",
            body=f"Name: {self.name}\nEmail: {self.email}\nPhone: {self.phone}\n\nMessage:\n{self.message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.property.seller.users.email],
        )
        email.attach_alternative(html_content, "text/html")  # Attach the HTML version
        email.send()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Inquiry by {self.name} for {self.property.property_name}"
    


class Negotiation(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="negotiations")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_negotiations", null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_negotiations")
    message = models.TextField()
    proposed_amount = models.IntegerField(max_length=100, null=True)
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    guest_phone = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.sender:
            return f"Negotiation for {self.property.property_name} by {self.sender.username}"
        return f"Negotiation for {self.property.property_name} by Guest ({self.guest_name})"
        


class PaymentTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="transactions")
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.reference} - {self.status}"