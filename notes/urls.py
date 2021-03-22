from django.urls import path
from notes import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'notes'

urlpatterns = [
    path('', views.Search.as_view(), name='search'),
    path('search/', views.Search.as_view(), name='search'),
    path('faq/', views.Faq.as_view(), name='faq'),
    path('search/<slug:studyGroup_slug>/', views.Show_group.as_view(), name='show_group'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('myaccount/<slug:username>/', views.Account.as_view(), name='account'),
    path('myaccount/<slug:username>/create_group/', views.Create_group.as_view(), name='create_group'),
    path('remove_group/', views.Remove_group.as_view(), name='remove_group'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)