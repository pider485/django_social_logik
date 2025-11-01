from django.urls import path
from . import views

urlpatterns = [
    # Визнач тут свої URL-шляхи
    path('', views.home, name='home'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('profile/', views.profile, name='profile'),
    path('post/<int:post_id>/', views.post_info, name='post_info'),
    path('freind/<int:freind_id>/', views.freind_chats, name='freind_chats'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('add_post/', views.add_post, name='add_post'),
    path('add_new_group/', views.add_new_group, name='add_new_group'),
    path('friend_add_to_group/', views.friend_add_to_group, name='friend_add_to_group'),
]