
from django.urls import  path 

from .views import login_view, RegisterView,ProfileView, logout_view

urlpatterns = [
path('sign-in/', login_view, name='sign-in'),
path('sign-up/', RegisterView.as_view(), name='sign-up'),
path('logout/', logout_view, name= 'logout'),   
path('profile/', ProfileView.as_view(), name= 'profile'),
# path('courses/', fetch_courses, name= 'courses'),
]