
from django.core.mail import send_mail
from django.conf import settings
# from .models import Property  # Assuming your model is called PropertyListing

def send_property_listing_email(property_id):
    # Retrieve the property listing details from the database
    property = Property.objects.get(id=property_id)

    # Construct the email content
    subject = f"Property Listing: {property.title}"
    message = f"""
    Property Title: {property.title}
    Location: {property.location}
    Price: {property.price}
    Description: {property.description}
    Contact: {property.contact_number}

    Visit the property at: {property.url}
    """

    # Send the email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # From email address
        ['recipient@example.com'],    # To email address (can be a list of recipients)
        fail_silently=False
    )

    print("Email sent successfully!")

def user_property_directory_path(instance, filename):
    return 'user_{0}/property/{1}'.format(instance.seller.users.id, filename)