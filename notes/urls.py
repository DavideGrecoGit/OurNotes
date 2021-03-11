from django.urls import path
from notes import views

app_name = 'notes'

urlpatterns = [
    path('', views.search, name='search'),
    path('faq/', views.faq, name='faq'),
]