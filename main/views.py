from django.shortcuts import render
from main.models import Group, GroupMessage, GroupMember
from django.shortcuts import get_object_or_404, redirect

# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'django_social_logik/home.html')
    
    groups = GroupMember.objects.filter(user=request.user)
    context = {'groups': groups}
    return render(request, 'django_social_logik/dashboard.html', context)



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
            # redirect нужен чтобы избежать повторной отправки формы
            return redirect('group_detail', group_id=group.id)
    messages = GroupMessage.objects.all().filter(group=group).order_by('created_at')
    return render(request, 'django_social_logik/group_detail.html', {'group': group, 'messages': messages})

def profile(request):
    return render(request, 'django_social_logik/profile.html')