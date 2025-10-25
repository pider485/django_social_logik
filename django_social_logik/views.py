from django.shortcuts import render
from main.models import GroupMember, Group
from django.shortcuts import get_object_or_404


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'django_social_logik/home.html')
    
    groups = GroupMember.objects.filter(user=request.user)
    context = {'groups': groups}
    return render(request, 'django_social_logik/dashboard.html', context)

