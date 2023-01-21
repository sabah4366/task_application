from django.urls import path
from tasks import views

urlpatterns=[
    path('',views.LoginView.as_view(),name="signin"),
    path('home',views.IndexView.as_view(),name="home")  ,
    path("register",views.SignUpView.as_view(),name='register-page'),
    path('logout',views.signout,name='signout'),
    path('tasks/add',views.TaskCreateView.as_view(),name="task-create"),
    path('tasks/all',views.TasksListView.as_view(),name="task-list"),
    path('tasks/<int:pk>',views.TaskDetailView.as_view(),name="task-details"),
    path('tasks/<int:pk>/remove',views.TaskDeleteView.as_view(),name="task-delete")

]