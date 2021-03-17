from django.urls import path
from notes import views

app_name = 'notes'

urlpatterns = [
    path('', views.search, name='search'),
    path('search/', views.search, name='search'),
    path('faq/', views.faq, name='faq'),
    path('search/<slug:studyGroup_slug>/', views.show_group, name='show_group'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
]