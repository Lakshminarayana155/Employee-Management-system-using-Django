from . import views
from django.urls import path, include


urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    #emp_data
    path('all_emply',views.all_emply,name='all_emply'),
    path('add_emply',views.add_emply,name='add_emply'),
    path('filter_emply',views.filter_emply,name='filter_emply'),
    path('remove_emply/<int:emp_id>/',views.remove_emply,name='remove_emply'),
    path('remove_emply/',views.remove_emply,name='remove_emply'),

    path('all_emply/<int:page_n>/',views.all_emply)
]