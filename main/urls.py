from django.urls import path
from .views import main_view, listing_view, about_view,property_single_view, contact_view,home_view,property_views,property_add_view,edit_view,like_listing_view,edit_property,sold_properties_view,submit_inquiry, submit_negotiation,generate_contract,accept_negotiation, initiate_payment,payment_callback,generate_receipt
from django.conf.urls.static import static 
from django.conf import settings



urlpatterns = [
    path('', main_view, name = 'main'),
    path('about/', about_view, name = 'about'),
    path('property-single/', property_single_view, name = 'property-single'),
    path('contact/', contact_view, name = 'contact'),
    path('home/', home_view, name = 'home'),
    path('edit_listing/<str:id>/edit/', edit_view, name = 'edit'), 
    path('edit_property/<str:property_id>/edit/', edit_property, name='edit_property'),
    path('like_listing/<str:id>/like/', like_listing_view, name = 'like_listing'), 
    path('property_add/', property_add_view, name = 'property_add'),
    path('property/', property_views, name = 'property_list'),
    path('sold_properties/', sold_properties_view, name = 'sold_properties'),
    path('property_listing/<str:id>/', listing_view, name = 'property_listing'),
    path('property_listing/<str:id>/submit_inquiry/', submit_inquiry, name='submit_inquiry'),
    path('property_listing/<str:id>/submit_negotiation/', submit_negotiation, name='submit_negotiation'),
    path('property/<str:property_id>/generate_contract/',generate_contract, name='generate_contract'),
     path('accept-negotiation/',accept_negotiation, name='accept_negotiation'),
    path('property/<str:property_id>/initiate_payment/', initiate_payment, name='initiate_payment'),
    path('payment/callback/', payment_callback, name='payment_callback'),
     path('receipt/<str:reference>/', generate_receipt, name='generate_receipt'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
