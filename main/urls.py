from django.urls import path
from . import views

urlpatterns = [
    # Визнач тут свої URL-шляхи
    path('', views.home, name='home'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
]