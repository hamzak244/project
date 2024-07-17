from . import views
from django.urls import path
#from .views import delete_document
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path("", views.home, name="home"),
    path("signup/", views.signup_page, name="signup"),
    path("login/", views.login_page, name="login"),
    path('reset_welcome_modal/', views.reset_welcome_modal, name='reset_welcome_modal'),
    path('check_welcome_modal/', views.check_welcome_modal, name='check_welcome_modal'),
    path('logout/', views.logout_page, name='logout'),
    path("blogs/", views.blog, name="blog"),
    path("students/", views.student, name="student"),
    path("academicians/", views.academician, name="academician"),
    path("researchers/", views.researcher, name="researcher"),
    path("features/", views.feature, name="feature"),
    path('reference/', views.reference_page, name='reference_page'),
    path('fetch/', views.fetch_data, name='fetch_data'),
    path('select_project/', views.select_project, name='select_project'),
    path("account/", views.account_page, name="account_page"),
    path('chat/', views.chat_view, name='chat_view'),
    path('help/', views.help, name='help'),
    path('pricing/', views.pricing, name='pricing'),
    path('projects/create/', views.create_project, name='create_project'),
    path('delete_project/', views.delete_project, name='delete_project'),
    path('fetch_projects/', views.fetch_projects, name='fetch_projects'),
     path('verify_email/<str:username>/', views.verify_email, name='verify_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)