
from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Property
from .filters import PropertyFilters
from .forms import PropertyForm
from .models import Property, LikedListing,Negotiation
from users.forms import LocationForm
import logging
from django.http import JsonResponse,HttpResponse
from .forms import PropertyEditForm,InquiryForm
from django.template.loader import get_template
from xhtml2pdf import pisa
from paystackapi.transaction import Transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import redirect
from .models import PaymentTransaction
from paystackapi.transaction import Transaction as PaystackTransaction
import uuid

import logging
logger = logging.getLogger(__name__)


def main_view(request):
    # Get all Property objects
    properties = Property.objects.all()  # This retrieves all the Property records from the database
    # Apply any filtering logic (if needed)
    properties_filter = PropertyFilters(request.GET, queryset=properties)
    # Build the context to pass to the template
    context = {
        'name': 'main', 
        'property_filter': properties_filter  
    }
    
    # Render the template with the updated context
    return render(request, 'views/main.html', context)

def listing_view(request):
    return render(request, 'views/listing.html', {'name': 'listing'})

def about_view(request):
    return render (request, 'views/about.html', {'name': 'about'})

def property_single_view(request):
    return render(request, 'views/property-single.html', {'name' : 'property-single'})

def contact_view(request):
    return render (request, 'views/contact.html', {'name': 'contact'})

def home_view(request):
    profile = None
    photo_url = None

    # Fetch all negotiations
    negotiations = Negotiation.objects.all().order_by('-created_at')

    # Prepare the context
    context = {
        'negotiations': negotiations,
    }

    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, users=request.user)
        photo_url = profile.photo.url if profile.photo else None
        context['photo_url'] = photo_url  # Add photo_url to the context

    return render(request, "views/home.html", context)
    

@login_required
def property_views(request):
    properties = Property.objects.all()
    properties_filter = PropertyFilters(request.GET, queryset=properties)
    user_liked_listings =  LikedListing.objects.filter(profile=request.user.profile).values_list('listing')
    liked_listing_ids = [l[0] for l in user_liked_listings]
    context = {
        # 'listings': listings,
        'property_filter': properties_filter,
         'liked_listing_ids': liked_listing_ids,
    }
    
    return render(request, "views/property_list.html",  context)

def main_view(request):
    properties = Property.objects.all()
    properties_filter = PropertyFilters(request.GET, queryset=properties)
    context = {
        # 'listings': listings,
        'property_filter': properties_filter
    }
    return render(request, 
    
                  "views/main.html",   context)

def aboutus_view(request):
    return render(request, "views/about-us.html", {"name": "aboutus"})

def contact_view(request):
    return render(request, "views/contact-us.html", {"name": "contact"})

def products_view(request):
    return render(request, "pages/products.html", {"name": "products"})


@login_required
def property_add_view(request):
    if request.method == 'POST':
        property_form = PropertyForm(request.POST, request.FILES)
        location_form = LocationForm(request.POST)
        
        print(f"Property form is valid: {property_form.is_valid()}")
        print(f"Location form is valid: {location_form.is_valid()}")
        
        if property_form.is_valid() and location_form.is_valid():
            try:
                property_location = location_form.save()
                print(f"Location saved with id: {property_location.id}")
                
                property = property_form.save(commit=False)
                property.seller = request.user.profile
                property.location = property_location
                property.save()
                print(f"Property saved with id: {property.id}")
                
                messages.success(request, f'{property.property_name} Property Posted Successfully!')
                return redirect('home')
            except Exception as e:
                logging.exception("Error occurred while saving property")
                messages.error(request, f'An error occurred while posting the Property: {str(e)}')
        else:
            print("Form errors:")
            print(property_form.errors)
            print(location_form.errors)
            messages.error(request, 'Please correct the errors in the form.')
    else:
        property_form = PropertyForm()
        location_form = LocationForm()
    
    return render(request, 'views/property_add.html', {
        'property_form': property_form, 
        'location_form': location_form,
    })

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# @login_required
def listing_view(request, id):
    try:
        logger.debug(f"Received ID: {id}")  # Log the ID that was passed
        property = Property.objects.get(id=id)
        logger.debug(f"Property Found: {property}")  # Log the found property
         # Initialize the inquiry form
        form = InquiryForm()
        return render(request, 'views/property-single.html', {'property_listing': property, 'form': form})
    except Property.DoesNotExist:
        messages.error(request, f'Invalid UUID {id} was provided for property.')
        return redirect('home')
    except Exception as e:
        logger.error(f"An error occurred: {e}")  # Log general exceptions
        return redirect('home')
    
@login_required
def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = PropertyEditForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('property_list')
    else:
        form = PropertyEditForm(instance=property)
    
    logging.debug(f"Form fields: {form.fields}")  # Debugging print
    return render(request, 'views/edit_property.html', {'sold_form': form, 'property': property})
    
@login_required
def edit_view(request, id):
    try:
        property = Property.objects.get(id=id)
        
        if property is None:
            raise Exception
        if request.method == 'POST':
            pass
        else:
            pass 
    except Exception as e:
        messages.error(request, f'An error has occured while trying to edit  the property.')
        return redirect('home')
    
    
@login_required
def like_listing_view(request, id):
    print("Listing ID:", id)  # Print the id parameter
    listing = get_object_or_404(Property, id=id)
    liked_listing, created  = LikedListing.objects.get_or_create(profile=request.user.profile, listing=listing)

    if not created:
        liked_listing.delete()
    else:
        liked_listing.save()
    return JsonResponse({
        'is_liked_by_user': created,
    })
    
    
@login_required
def sold_properties_view(request):
    properties = Property.objects.filter(is_sold=True)
    properties_filter = PropertyFilters(request.GET, queryset=properties)
    context = {
        'property_filter': properties_filter
    }
    return render(request, "views/sold_properties.html", context)
    
@login_required
def edit_view(request, id):
    try:
        property_listing = Property.objects.get(id=id)
        if property_listing is None:
            raise Exception
        if request.method == 'POST':
            listing_form = PropertyForm(request.POST, request.FILES,instance=property_listing)
            location_form = LocationForm(request.POST, instance=property_listing.location)
            if listing_form.is_valid and location_form.is_valid:
                listing_form.save()
                location_form.save()
                messages.info(request, f'Listing {id} updated successfully!')
                return redirect('home')
            else:
                messages.error(request, f'An error has occured while trying to edit  the listing.')
                # return reload()


        else:
            listing_form = PropertyForm(instance=property_listing)
            location_form = LocationForm(instance=property_listing.location)
        context = {
            'location_form' : location_form,
            'listing_form' : listing_form
        }
        return render(request, 'views/edit.html', context)
    except Exception as e:
        messages.error(request, f'An error has occured while trying to edit  the listing.')
        return redirect('property_list')
    
from django.http import JsonResponse

def submit_inquiry(request, id):
    try:
        logger.debug(f"Received ID for submission: {id}")  # Log the ID that was passed
        property_listing = Property.objects.get(id=id)
        logger.debug(f"Property Found for submission: {property_listing}")  # Log the found property

        if request.method == "POST":
            form = InquiryForm(request.POST)
            if form.is_valid():
                logger.debug("Form is valid")  # Log form validation success
                inquiry = form.save(commit=False)
                inquiry.property = property_listing
                inquiry.save()
                return JsonResponse({
                    'status': 'success',
                    'message': "Your inquiry has been sent successfully!",
                    'redirect_url': reverse('main')
                })
            else:
                logger.debug(f"Form errors: {form.errors}")  # Log form errors
                return JsonResponse({
                    'status': 'error',
                    'message': "There was an error with your submission. Please try again.",
                    'errors': form.errors
                }, status=400)

        # If the request is not POST, return an error
        return JsonResponse({
            'status': 'error',
            'message': "Invalid request method."
        }, status=405)

    except Property.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': f'Invalid UUID {id} was provided for property.'
        }, status=404)
    except Exception as e:
        logger.error(f"An error occurred during submission: {e}")  # Log general exceptions
        return JsonResponse({
            'status': 'error',
            'message': "An unexpected error occurred. Please try again later."
        }, status=500)
        
        


def submit_negotiation(request, id):
    if request.method == "POST":
        property_listing = Property.objects.get(id=id)
        message = request.POST.get("message")
        receiver_id = property_listing.seller.users.id  # Assuming the seller is the receiver

        if request.user.is_authenticated:
            # Authenticated user (buyer)
            negotiation = Negotiation.objects.create(
                property=property_listing,
                sender=request.user,
                receiver_id=receiver_id,
                message=message,
            )
        else:
            # Guest buyer
            guest_name = request.POST.get("guest_name")
            guest_email = request.POST.get("guest_email")
            guest_amount = request.POST.get("guest_amount")
            guest_phone = request.POST.get("guest_phone")

            negotiation = Negotiation.objects.create(
                property=property_listing,
                receiver_id=receiver_id,
                message=message,
                guest_name=guest_name,
                guest_email=guest_email,
                proposed_amount=guest_amount,
                guest_phone=guest_phone,
            )
        send_mail(
        subject="New Negotiation Message",
        message=f"You have received a new negotiation message for {property_listing.property_name}.",
        from_email="danmamahomes@info.com",
        recipient_list=[property_listing.seller.users.email],
    )

        return JsonResponse({"status": "success", "message": "Negotiation message sent successfully!"})
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

# Generate Smart Contract
def generate_contract(request, property_id):
    # property_listing = Property.objects.get(id=property_id)
    property_listing = get_object_or_404(Property, id=property_id)
    proposed_amount = request.GET.get('amount', property_listing.price)  # Default to property price if no amount is provided
    context = {
        'property': property_listing,
        'proposed_amount': proposed_amount,
    }
    template = get_template('contracts/smart_contract.html')
    context = {
        'property': property_listing,
        'buyer': request.user,
        'seller': property_listing.seller.users,
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contract_{property_id}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response





def accept_negotiation(request):
    if request.method == "POST":
        negotiation_id = request.POST.get("negotiation_id")
        buyer_email = request.POST.get("buyer_email")
        proposed_amount = request.POST.get("proposed_amount")

        # Fetch the negotiation
        negotiation = Negotiation.objects.get(id=negotiation_id)

        # Generate URLs
        contract_url = request.build_absolute_uri(
            reverse('generate_contract', args=[negotiation.property.id])
        )
        payment_url = request.build_absolute_uri(
            reverse('initiate_payment', args=[negotiation.property.id])
        )

        # Render the email template
        email_content = render_to_string('emails/negotiation_email.html', {
            'proposed_amount': proposed_amount,
            'contract_url': contract_url,
            'payment_url': payment_url,
        })

        # Send the email
        send_mail(
            subject="Smart Contract for Property Purchase",
            message="Please enable HTML to view this email.",
            from_email="danmama@info.com",
            recipient_list=[buyer_email],
            html_message=email_content,  # Send the HTML version
        )

        return JsonResponse({"status": "success", "message": "Smart contract link sent to the buyer!"})
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)



def initiate_payment(request, property_id):
    property_listing = get_object_or_404(Property, id=property_id)
    proposed_amount = int(request.GET.get('amount', property_listing.price)) * 100  # Convert to kobo (smallest currency unit)
    cus_email = "customer@gmail.com"
    buyer_email = request.user.email if request.user.is_authenticated else cus_email
     # Generate a unique random alphanumeric reference
    reference = f"property_{property_id}_{uuid.uuid4().hex[:8]}"

    # Log the transaction in the database
    transaction = PaymentTransaction.objects.create(
        property=property_listing,
        buyer=request.user if request.user.is_authenticated else None,
        reference=reference,
        amount=proposed_amount / 100,  # Convert back to the main currency unit
        status='pending',
    )

    # Initialize the transaction with Paystack
    response = PaystackTransaction.initialize(
        reference=reference,
        amount=proposed_amount,
        email=buyer_email,
        callback_url=request.build_absolute_uri(reverse('payment_callback')),  # Callback URL
    )

    # Log the response for debugging
    logger.debug(f"Paystack response: {response}")

    if response['status']:
        # Redirect to Paystack authorization URL
        return redirect(response['data']['authorization_url'])
    else:
        # Handle error
        transaction.status = 'failed'
        transaction.save()
        return JsonResponse({
            'status': 'error',
            'message': 'Payment initialization failed. Please try again.',
            'error_details': response.get('message', 'Unknown error')  # Include error details from Paystack
        }, status=400)


from django.shortcuts import render

def payment_callback(request):
    reference = request.GET.get('reference')  # Get the transaction reference from the callback
    response = PaystackTransaction.verify(reference=reference)  # Verify the transaction with Paystack

    try:
        # Fetch the transaction from the database
        transaction = PaymentTransaction.objects.get(reference=reference)

        if response['status']:
            # Payment successful
            transaction.status = 'successful'
            transaction.save()

            # Update the property status or perform other actions
            transaction.property.status = 'sold'
            transaction.property.save()

            # Generate the receipt URL
            receipt_url = reverse('generate_receipt', args=[reference])

            # Render the success template
            return render(request, 'payment/payment_success.html', {
                'receipt_url': request.build_absolute_uri(receipt_url),
                'transaction_reference': reference,
            })
        else:
            # Payment failed
            transaction.status = 'failed'
            transaction.save()

            return JsonResponse({
                'status': 'error',
                'message': 'Payment verification failed. Please try again.',
            }, status=400)
    except PaymentTransaction.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Transaction not found.',
        }, status=404)
        


def generate_receipt(request, reference):
    # Fetch the transaction using the reference
    transaction = get_object_or_404(PaymentTransaction, reference=reference)

    # Render the receipt template
    template = get_template('receipts/payment_receipt.html')
    context = {
        'transaction': transaction,
    }
    html = template.render(context)

    # Generate the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{reference}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Check for errors
    if pisa_status.err:
        return HttpResponse("Error generating receipt", status=500)

    return response


