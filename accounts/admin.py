from django.contrib import admin
from .models import Profile
from main.models import Message, Group, GroupMember, Chat, Chat_message, Blocked, GroupMessage, Postest, Freids, freind_message

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
class PostestAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__user__username', 'content')
admin.site.register(Postest, PostestAdmin)

class FreidsAdmin(admin.ModelAdmin):
    list_display = ('user_1', 'user_2')
    search_fields = ('user_1__user__username', 'user_2__user__username')
admin.site.register(Freids, FreidsAdmin)

class freind_messageAdmin(admin.ModelAdmin):
    list_display = ('freind', 'user', 'created_at')
    search_fields = ('freind__user_1__user__username', 'freind__user_2__user__username', 'user__user__username', 'content')
admin.site.register(freind_message, freind_messageAdmin)