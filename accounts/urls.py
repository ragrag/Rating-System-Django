from django.conf.urls import url

from accounts.views import get_user_profile

app_name = 'accounts'

urlpatterns = [


    url(r'(?P<id>\d+)$', get_user_profile.as_view(), name = 'userprofile'),


]
