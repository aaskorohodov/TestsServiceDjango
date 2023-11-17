from django.urls import path
from .views import *


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('logout/', logout_user, name='logout'),
    path('tests/<str:test_slug>/<int:sequence_number>/', TestGenerator.as_view(), name='test_generator')
]
