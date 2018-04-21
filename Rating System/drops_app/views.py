
from django.shortcuts import render

# Create your views here.
from accounts.models import Team


def index(request):
        template = 'accounts/index.html'

        groups = Team.objects.order_by('-points')


        if request.user.is_authenticated():
                user = request.user
                groups = Team.objects.order_by('-points')
                profile = user.profile

                return render(request, template,
                              {'user': user, 'teams': groups, 'profile': profile})

        else:

                return render(request, template,
                              {'teams': groups})



