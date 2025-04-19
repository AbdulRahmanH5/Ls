from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

# url patterns for the application
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('', views.home_view, name='home'),
    path('courses/', views.courses_view, name='courses'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('profile/', views.profile_view, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='core/password_change.html',
        success_url='/password_change_done/'
    ), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='core/password_change_done.html'
    ), name='password_change_done'),
    path('courses/<int:course_id>/add_comment/', views.add_comment, name='add_comment'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/complete/', 
         views.mark_lesson_completed, 
         name='mark_lesson_completed'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)