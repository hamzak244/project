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
    path('logout/', views.logout_page, name='logout'),
    path("blogs/", views.blog, name="blog"),
    path("students/", views.student, name="student"),
    path("academicians/", views.academician, name="academician"),
    path("researchers/", views.researcher, name="researcher"),
    path("features/", views.feature, name="feature"),
    path('reference/', views.reference_page, name='reference_page'),
    path('fetch/', views.fetch_data, name='fetch_data'),
    path('select_project/', views.select_project, name='select_project'),
    #path("user/", views.my_view, name="my_view"),
    path("account/", views.account_page, name="account_page"),
    #path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('chat/', views.chat_view, name='chat_view'),
    path('help/', views.help, name='help'),
    path('pricing/', views.pricing, name='pricing'),
    #path('delete_document/', views.delete_document, name='delete_document'),

    #path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),
    #path('update_project/', views.update_project, name='update_project'),
    path('delete_project/', views.delete_project, name='delete_project'),
    path('fetch_projects/', views.fetch_projects, name='fetch_projects'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)