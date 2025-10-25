from django.contrib import admin
from .models import Profile
from main.models import Message, Group, GroupMember, Chat, Chat_message, Blocked, GroupMessage

# Register your models here.
admin.site.register(Profile)
admin.site.register(Message)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Group, GroupAdmin)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'status')
    search_fields = ('group__name', 'user__user__username', 'status')

admin.site.register(GroupMember, GroupMemberAdmin)
admin.site.register(Chat)
admin.site.register(Chat_message)
admin.site.register(Blocked)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'created_at')
    search_fields = ('group__name', 'user__user__username', 'content')

admin.site.register(GroupMessage, GroupMessageAdmin)
