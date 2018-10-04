from django.urls import path
from application import views, models
from .views import PeopleListView
urlpatterns = [
    path('', PeopleListView.as_view(), name='list'),
    # path('post/', PeopleCreateView.as_view(), name='post'),
    path('home/', views.home, name='home'),
    path('list/', views.people_list, name='people_list'),
    path('list/detail/<int:pk>/', views.people_detail, name='people_detail'),
    path('list/detail/<int:pk>/update', views.people_update, name='people_update'),
    path('list/detail/<int:pk>/delete', views.delete_people, name='people_delete'),
    path('post/', views.people_create, name='post'),
    path('main/', views.main, name='main'),
    path('male/', views.male, name='male'),
]