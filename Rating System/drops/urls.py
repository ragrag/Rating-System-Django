"""drops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url , include
from django.contrib import admin
import django.contrib.auth.views
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

import accounts.views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework.authtoken import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^oauth', include('social_django.urls', namespace='social')),


    url(r'^login/$', django.contrib.auth.views.login,{'template_name': 'accounts/login.html'},name="login" ),
    url(r'^register/', accounts.views.UserFormView.as_view(), name='register'),
    url(r'^logout/$', django.contrib.auth.views.logout, {'next_page': '/index/'}, name='logout'),
    url(r'^index/', include('drops_app.urls')),
    url(r'', include('drops_app.urls')),
    url(r'^team/', include('accounts.urls'),name='Profile'),
    url(r'^nogroup/', accounts.views.nogroup,name='No Group'),
    url(r'^delete/(?P<id>\d+)$', accounts.views.PostDelete, name='delete_post'),









    url(r'^api/auth/token/', views.obtain_auth_token),
    url(r'^api/user/create/', accounts.views.CreateUser.as_view()),
    url(r'^api/teams/', accounts.views.AllTeamsAPI.as_view(),name="teams" ),
    url(r'^api/team/(?P<id>\d+)$', accounts.views.TeamIDAPI.as_view(),name="teamids" ),
    url(r'^api/user/team', accounts.views.TeamAPI.as_view(),name="specteam" ),
    url(r'^api/comment/create/(?P<id>\d+)$', accounts.views.CreateComment.as_view(),name="Create Comment" ),
    url(r'^api/points/(?P<id>\d+)/(?P<val>-?\d+)$', accounts.views.PointUpdateCL.as_view(),name="Update Points" ),
    url(r'^api/user/staff', accounts.views.UserIsStaff.as_view(),name="is staff" ),
    url(r'^api/comments/(?P<id>\d+)$', accounts.views.TeamCommentAPI.as_view(),name="team_comments" ),
    url(r'^api/comment/delete/(?P<id>\d+)$', accounts.views.CommentDeleteAPI.as_view(),name="team_comments" ),
    url(r'^api/changes/(?P<id>\d+)$', accounts.views.TeamChangeAPI.as_view(),name="team_changes" ),


]

urlpatterns = format_suffix_patterns(urlpatterns)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
