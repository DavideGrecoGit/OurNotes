from django.urls import path
from notes import views

app_name = 'notes'

urlpatterns = [
    path('', views.search, name='search'),
    path('faq/', views.faq, name='faq'),
    path('<slug:studyGroup_slug>/', views.show_group, name='show_group'),
]