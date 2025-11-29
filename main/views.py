from django.shortcuts import render
from main.models import Group, GroupMessage, GroupMember, Freids, Postest , freind_message, Profile, freind_request, subscribe, PostLike, PostDislike
from django.shortcuts import get_object_or_404, redirect
from accounts.forms import ProfileForm
# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'django_social_logik/home.html')
    postets = Postest.objects.order_by('-created_at')[:5]
    freinds = Freids.objects.filter(user_1=request.user) | Freids.objects.filter(user_2=request.user)
    groups = GroupMember.objects.filter(user=request.user)
    profiles = Profile.objects.all()
    like = PostLike.objects.all()
    dislike = PostDislike.objects.all()
    context = {'groups': groups,
                'freinds': freinds,
                'postets': postets,
                'profiles': profiles,
                 'like': like,
                 'duislike': dislike,
               }
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        action = request.POST.get("action")
        post = get_object_or_404(Postest, pk=post_id)
        if action == "like":
            if like.filter(user=request.user, post=post).exists():
                PostLike.objects.filter(user=request.user, post=post).delete()
                return redirect('home')
            else:
                print("like")
                PostLike.objects.create(
                    user=request.user,
                    post=post
                )
                try:
                    PostDislike.objects.get(user=request.user, post=post).delete()
                except PostDislike.DoesNotExist:
                    pass
                return redirect('home')
        elif action == "dislike":
            if dislike.filter(user=request.user, post=post).exists():
                PostDislike.objects.filter(user=request.user, post=post).delete()
                return redirect('home')
            print("dislike")
            PostDislike.objects.create(
                user=request.user,
                post=post
            )
            try:
                PostLike.objects.get(user=request.user, post=post).delete()
            except PostLike.DoesNotExist:
                pass
            return redirect('home')
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

def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'django_social_logik/edit_profile.html', {'form': form})

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
    if request.method == "POST":
        action = request.POST.get("action")
        from_user_id = request.user.id
        to_user_id = request.POST.get("friend_id")
        to_user = get_object_or_404(Profile, pk=to_user_id)
        if action == "subscribe":
            subscribe.objects.create(
                subscribe= from_user_id,
                user = to_user_id 
            )
        else:
            freind_request.objects.create(
                from_user_id=from_user_id,
                to_user=to_user
            )
    return render(request, 'django_social_logik/add_freind.html', {'profiles': profiles})

def add_friend_request(request):
    if request.method == "POST":
        from_user_id = request.user.id
        to_user_id = request.POST.get("friend_id")
        to_user = get_object_or_404(Profile, pk=to_user_id)
        freind_request.objects.create(
            from_user_id=from_user_id,
            to_user=to_user
        )
    return redirect('add_friend')

def add_subscriber_request(request):
    if request.method == "POST":
        from_user_id = request.user
        to_user_id = request.POST.get("friend_id")
        to_user = get_object_or_404(Profile, pk=to_user_id)
        subscribe.objects.create(
            subscribe= from_user_id,
            user = to_user 
        )
    return redirect('add_friend')

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
    if request.method == "POST":
        friend_id = request.POST.get("friend_id")
        group_id = request.POST.get("group_id")
        friend = get_object_or_404(Freids, pk=friend_id)
        group = get_object_or_404(Group, pk=group_id)
        if friend and group:
            if friend.user_1 == request.user:
                GroupMember.objects.create(
                    status='member',
                    group=group,
                    user=friend.user_2
                )
            else:
                GroupMember.objects.create(
                    status='member',
                    group=group,
                    user=friend.user_1
                )
            return redirect('friend_add_to_group/')
    freinds = Freids.objects.filter(user_1=request.user) | Freids.objects.filter(user_2=request.user)
    return render(request, 'django_social_logik/friend_add_to_group.html', {'freinds': freinds})

def freind_requests_view(request,):
    requests = freind_request.objects.filter(to_user_id = request.user)
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")
        fr_request = get_object_or_404(freind_request, pk=request_id)
        if action == "accept":
            Freids.objects.create(
                user_1=fr_request.from_user,
                user_2=fr_request.to_user
            )
            fr_request.status = 'accepted'
            fr_request.save()
        elif action == "reject":
            fr_request.status = 'rejected'
            fr_request.save()
        return redirect('freind_requests_view')
    return render(request, 'django_social_logik/freind_request.html',{'requests': requests})

def profile_check(request,us_id):
    profile = Profile.objects.filter(id=us_id)
    return render(request, "django_social_logik/profile_check.html", {'profile': profile})

def all_post(request, page):
    like = PostLike.objects.all()
    dislike = PostDislike.objects.all()
    if page == 1:
        postets = Postest.objects.all().order_by('-created_at')[:28]
        back_page = page
    else:
        postets = Postest.objects.all().order_by('-created_at')[(page-1)*28:28*(page)]
        back_page = page - 1
    
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        action = request.POST.get("action")
        post = get_object_or_404(Postest, pk=post_id)
        if action == "like":
            if like.filter(user=request.user, post=post).exists():
                PostLike.objects.filter(user=request.user, post=post).delete()
                return redirect('all_post')
            else:
                print("like")
                PostLike.objects.create(
                    user=request.user,
                    post=post
                )
                try:
                    PostDislike.objects.get(user=request.user, post=post).delete()
                except PostDislike.DoesNotExist:
                    pass
                return redirect('all_post')
        elif action == "dislike":
            if dislike.filter(user=request.user, post=post).exists():
                PostDislike.objects.filter(user=request.user, post=post).delete()
                return redirect('all_post')
            print("dislike")
            PostDislike.objects.create(
                user=request.user,
                post=post
            )
            try:
                PostLike.objects.get(user=request.user, post=post).delete()
            except PostLike.DoesNotExist:
                pass
            return redirect('all_post')
    return render(request, 'django_social_logik/all_post.html', {'postets': postets, 'next_page': page + 1, 'back_page': back_page, 'like': like, 'dislike': dislike})