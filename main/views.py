from django.shortcuts import render
from main.models import Group, GroupMessage, GroupMember, Freids, Postest , freind_message, Profile
from django.shortcuts import get_object_or_404, redirect

# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'django_social_logik/home.html')
    groups = GroupMember.objects.filter(user=request.user)
    return render(request, 'django_social_logik/dashboard.html', {'groups': groups})



def group_detail(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            GroupMessage.objects.create(
                group=group,
                user=request.user,
                content=content
            )
            return redirect('group_detail', group_id=group.id)
    messages = GroupMessage.objects.all().filter(group=group).order_by('created_at')
    return render(request, 'django_social_logik/group_detail.html', {'group': group, 'messages': messages})

def post_info(request, post_id):
    post = get_object_or_404(Postest, pk=post_id)
    return render(request, 'django_social_logik/post_info.html', {'post': post})

def profile(request):
    return render(request, 'django_social_logik/profile.html')

def freind_chats(request, freind_id):
    freind = get_object_or_404(Freids, pk=freind_id)
    all_messages = freind_message.objects.filter(freind=freind).order_by('created_at')
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            freind_message.objects.create(
                freind=freind,
                user=request.user,
                content=content
            )
    return render(request, 'django_social_logik/freind_chats.html', {'freind': freind, 'messages': all_messages})

def add_friend(request):
    profiles = Profile.objects.all()
    return render(request, 'django_social_logik/add_freind.html', {'profiles': profiles})

def add_post(request):
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Postest.objects.create(
                user=request.user,
                content=content
            )
            return redirect('home')
    return render(request, 'django_social_logik/add_post.html')

def add_new_group(request):
    return render(request, 'django_social_logik/add_new_group.html')