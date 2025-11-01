from django.shortcuts import render
from main.models import Group, GroupMessage, GroupMember, Freids, Postest , freind_message, Profile
from django.shortcuts import get_object_or_404, redirect

# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'django_social_logik/home.html')
    postets = Postest.objects.all()
    freinds = Freids.objects.filter(user_1=request.user) | Freids.objects.filter(user_2=request.user)
    groups = GroupMember.objects.filter(user=request.user)
    profiles = Profile.objects.all()
    context = {'groups': groups
               , 'freinds': freinds
               , 'postets': postets,
                'profiles': profiles
               }
    return render(request, 'django_social_logik/dashboard.html', context)



def group_detail(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    groupMember = GroupMember.objects.filter(group=group, user=request.user)
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
    return render(request, 'django_social_logik/group_detail.html', {'group': group, 'messages': messages, 'groupMember': groupMember})

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
    query = request.GET.get('search', None)
    if query:
        profiles = profiles.filter(username__icontains=query)
    return render(request, 'django_social_logik/add_freind.html', {'profiles': profiles})

def add_post(request):
    if request.method == "POST":
        content = request.POST.get("content")
        image = request.FILES.get("image")
        if content:
            Postest.objects.create(
                user=request.user,
                content=content,
                img=image
            )
            return redirect('home')
    return render(request, 'django_social_logik/add_post.html')

def add_new_group(request):
    if request.method == "POST":
        group_name = request.POST.get("group_name")
        if group_name:
            new_group = Group.objects.create(name=group_name,
                                             creator=request.user)
            GroupMember.objects.create(
                status='admin',
                group=new_group,
                user=request.user
            )
            return redirect('home')
    return render(request, 'django_social_logik/add_new_group.html')

def friend_add_to_group(request):
    freinds = Freids.objects.filter(user_1=request.user) | Freids.objects.filter(user_2=request.user)
    return render(request, 'django_social_logik/friend_add_to_group.html', {'freinds': freinds})