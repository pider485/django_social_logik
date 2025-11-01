from django.shortcuts import render
from main.models import GroupMember, Freids, Postest,Profile
from django.shortcuts import get_object_or_404


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

