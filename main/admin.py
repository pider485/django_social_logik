from django.contrib import admin
from .models import Message, Group, GroupMember, Chat, Chat_message, Blocked

# Register your models here.
admin.site.register(Message)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Chat)
admin.site.register(Chat_message)
admin.site.register(Blocked)
