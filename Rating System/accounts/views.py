
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response


from accounts.models import Team, Comment, Change
from .forms import UserForm, CommentForm, PointUpdate

from .serializers import *



class CreateUser( APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        serialized  = UserSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)




class CreateComment( APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request,id):

        serialized  = CommentPostSerializer(data=request.data)
        if serialized.is_valid():
            team = Team.objects.get(pk=id)
            serialized.save(receiver=team)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

import json

class PointUpdateCL( APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request,id,val):

        serialized  = ChangeSerializer(data=request.data)
        if serialized.is_valid():
            team = Team.objects.get(pk=id)
            serialized.save(team=team)
            team.points +=int(val)
            team.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)







class CommentDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        comment = Comment.objects.get(pk=id)

        if comment:
            comment.delete();
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TeamAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        profile = request.user.profile
        team = profile.group
        serializer = TeamSerializer(team)
        return Response(serializer.data)

class AllTeamsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        teams = Team.objects.order_by('-points')
        serializer = TeamSerializer(teams,many=True)
        return Response(serializer.data)


class TeamIDAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        teams = Team.objects.get(pk=id)
        serializer = TeamSerializer(teams)
        return Response(serializer.data)


class UserIsStaff(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserStaffSerializer(user)
        return Response(serializer.data)

class TeamCommentAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        team = Team.objects.get(pk=id)
        if request.user.is_staff == True or request.user.profile.group == team:
            comments = Comment.objects.filter(receiver=team)
        if request.user.profile.group != team and request.user.is_staff == False:
            comments = Comment.objects.filter(receiver=team, public=True)

        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data)

class TeamChangeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        team = Team.objects.get(pk=id)
        changes = Change.objects.filter(team=team)
        serializer = ChangeSerializer(changes,many=True)
        return Response(serializer.data)

class UserFormView(View):
    form_class = UserForm
    template = 'accounts/registration.html'
    #Displaying the form
    def get(self, request):
        form = self.form_class(None)

        return render(request,self.template, {'form':form})
    #Submitting form
    def post(self,request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            #Checks
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            number = form.cleaned_data['number']
            user.profile.number = form.cleaned_data['number']
            user.save()


            #Auth
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('drops:index')
        return render(request, self.template, {'form': form})

class get_user_profile(View):
    form_class1 = CommentForm
    form_class2 = PointUpdate
    def get(self, request, id):

        if request.user.is_authenticated():


            user = request.user
            profile = user.profile

            team = Team.objects.get(id=id)
            changes = Change.objects.filter(team=team)
            teamusers = Profile.objects.filter(group=team)

            comments = Comment.objects.filter(receiver=team)
            postform = self.form_class1(None)
            pointupdateform = self.form_class2(None)
            return render(request, 'accounts/user_profile.html',
                          {'changes':changes,'user': user,'profile':profile,'team':team,'teamusers':teamusers,'comments':comments,'postform':postform,'pointform':pointupdateform})

        else :
            team = Team.objects.get(id=id)

            teamusers = Profile.objects.filter(group=team)

            comments = Comment.objects.filter(receiver=team)

            return render(request, 'accounts/user_profile.html',
                          { 'team': team, 'teamusers': teamusers,
                           'comments': comments})

    def post(self, request, id):
        postform = self.form_class1(request.POST)
        pointform = self.form_class2(request.POST)

        if request.method == 'POST':
            if 'addcomment' in request.POST:
                if postform.is_valid():
                    postform.save(commit=False)
                    postform.instance.content = postform.instance.content
                    is_public = request.POST.get('is_private', False)
                    if is_public == True:
                        postform.instance.public = True
                team = Team.objects.get(id=id)
                postform.instance.receiver = team
                postform.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif 'addpoints' in request.POST:
                if pointform.is_valid():

                    cd = pointform.cleaned_data
                    points = cd.get('points')
                    notes = cd.get('notes')
                    team= Team.objects.get(id=id)
                    team.points = team.points + points
                    team.save()
                    change = Change.objects.create(team=team, value=points,note=notes)
                    change.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            elif 'subpoints' in request.POST:
                if pointform.is_valid():

                    cd = pointform.cleaned_data
                    points = cd.get('points')
                    notes = cd.get('notes')
                    team= Team.objects.get(id=id)
                    team.points = team.points - points
                    team.save()
                    change = Change.objects.create(team=team, value=-points, note=notes)
                    change.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                
def nogroup(request):
     return render(request, 'accounts/nogroup.html')

def PostDelete(request, id):
    post = Comment.objects.get(pk=id)
    post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
