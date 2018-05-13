

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class Team(models.Model):
    name = models.CharField(max_length=500,blank=True,default=' ')
    points = models.IntegerField(default=0, blank=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, default='avatars/defaultdp.jpg')

    class Meta:
        verbose_name_plural = 'Team '
    def __str__(self):
        return str(self.name)


class Change(models.Model):
    team = models.ForeignKey(Team, related_name='Team', blank=True, null=True, on_delete=models.CASCADE)
    value = models.IntegerField(default=0, blank=False)
    note = models.CharField(max_length=200,blank=True,default=' ')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Point Changes '
        ordering = ['-date_created', ]

    def __str__(self):
        return str(self.team) + " " + str(self.value)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=500,blank=True,default=' ')
    group = models.ForeignKey(Team, related_name='current_group',blank=True,null=True, on_delete=models.SET_NULL)
    username2 = models.CharField(max_length=40, blank=True)


    def __str__(self):
        return str(self.user.username)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,username2=instance.username)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()




class Comment(models.Model):
    receiver = models.ForeignKey(Team ,related_name="receivedby", on_delete=models.CASCADE)
    content = models.CharField(max_length=500,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Comments'
        ordering = ['-date_created', ]

    def __str__(self):
        return str(self.content)





