from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include


urlpatterns = [
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('', include('TestsGUI.urls'))
]
