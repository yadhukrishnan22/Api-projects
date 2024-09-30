
from django.urls import path

from notes import views

from rest_framework.authtoken.views import ObtainAuthToken



urlpatterns=[

    path('user/', views.UserCreationView.as_view()),
    path('tasks/', views.TaskCreateView.as_view()),
    path('tasks/<int:pk>', views.TaskRetrieveUpdateDestroyView.as_view()),
    path('tasks/summary/', views.TaskSummaryApiView.as_view()),
    path('tasks/category/', views.CategoryListApiView.as_view()),
    path('token/', ObtainAuthToken.as_view())
    
]