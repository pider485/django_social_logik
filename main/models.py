from django.db import models
from accounts.models import Profile

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    send_time = models.DateTimeField(auto_now_add=True)

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    registration = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)

class GroupMember(models.Model):
    STATUS_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('banned', 'Banned'),
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='member')

class Chat(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user1 = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user1 = models.ForeignKey(Profile, on_delete=models.CASCADE)
    last_message = models.ForeignKey(Message, on_delete=models.CASCADE)

class Chat_message(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    send_time = models.DateTimeField(auto_now_add=True)

class Blocked(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank = True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, blank = True)

class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Postest(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='posts/')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Freids(models.Model):
    user_1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_user_1')
    user_2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_user_2')

class freind_message(models.Model):
    freind = models.ForeignKey(Freids, on_delete=models.CASCADE, related_name='freind_messages')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class freind_request(models.Model):
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_friend_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')

class subscribe(models.Model):
    subscribe = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='subscribe')
    user = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='user')