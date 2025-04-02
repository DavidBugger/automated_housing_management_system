import django_filters

from .models import Property 

class PropertyFilters(django_filters.FilterSet):
    class Meta:
        model = Property 
        fields = {'property_name': {'exact'}, 'seller': {'exact'}, 'color': {'exact'}, 'date_created': {'exact'} }