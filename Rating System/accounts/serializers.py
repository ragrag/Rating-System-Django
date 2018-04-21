from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

from .models import Profile, Team, Comment, Change


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['username','password']

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()


        return user



class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['pk','name','points','avatar']



class UserStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_staff']



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk','content','public']

class ChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Change
        fields = ['value','note']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['group']



class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content','public']


