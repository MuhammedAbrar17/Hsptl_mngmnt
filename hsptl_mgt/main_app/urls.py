from django.urls import path
from .import views
urlpatterns = [
   path('',views.index, name="index"),
   path('log_in', views.log_in, name = 'log_in'),
   path('home',views.home,name='home'),
   path('signout', views.signout, name = 'signout'),
   path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),  
   
   #user
   path('create_user',views.create_user, name='create_user'),
   path('userlist', views.user_list, name='user_list'),  # Ensure no typo here
   path('delet_user/<int:user_id>/',views.delete_user,name='delete_user'),
   path('edit_user/<int:id>/', views.edit_user, name='edit_user'),
   
   #doctor
   path('add_doctor/',views.add_doctor,name='add_doctor'),
   path('doctor_list/', views.doctor_list, name='doctor_list'),
   path('edit_doctor/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
   path('delete_doctor/<int:doctor_id>/',views.delete_doctor, name='delete_doctor'),

]

    