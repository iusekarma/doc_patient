from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', user_views.register, name='register'),
    path('doctor/login/', auth_views.LoginView.as_view(template_name='users/login_doctor.html'), name='doctor-login'),
    path('doctor/register/', user_views.register_doctor, name='doctor-register'),
    path('logout/', user_views.user_logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)