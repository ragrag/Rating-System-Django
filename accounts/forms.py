from accounts.models import User, Profile, Comment, Team
from django import forms

class UserForm(forms.ModelForm):

    username = forms.CharField(widget=forms.Textarea(attrs={'cols': 36, 'rows': 1,'placeholder': 'Username'}),label='')
    number = forms.IntegerField(required=True,widget=forms.Textarea(attrs={'cols': 36, 'rows': 1,'placeholder': 'Phone Number'}),
                               label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'size':35,'placeholder': 'Password'}), label='')
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'size':35, 'placeholder': 'Repeat Password'}),
                               label='')
    username.widget.attrs.update({'id': 'message'})
    number.widget.attrs.update({'id': 'message'})
    password.widget.attrs.update({'id': 'message'})
    password_repeat.widget.attrs.update({'id': 'message'})

    class Meta:
        model = User
        fields = ['username','number','password','password_repeat']

    def clean(self):
        number = self.cleaned_data['number']
        if number  and Profile.objects.filter(number=number).count() > 0:
            raise forms.ValidationError("Number Already exists")
        username = self.cleaned_data['username']
        if username and User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError("Username Already exists")

        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']
        if password != password_repeat:
            raise forms.ValidationError("Passwords do not match.")






class CommentForm(forms.ModelForm):

    content = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 40, 'rows': 5,'placeholder': 'Add Comment'}),label='')
    public = forms.BooleanField(required=False)

    content.widget.attrs.update({'id': 'message'})

    class Meta:
        model = Comment
        fields = ['content','public']


class PointUpdate(forms.Form):

    points = forms.IntegerField(required=True,widget=forms.Textarea(attrs={'cols': 5, 'rows': 1,'placeholder': ''}),label='')
    points.widget.attrs.update({'id': 'message'})
    notes = forms.CharField(required=False,widget=forms.Textarea(attrs={'cols': 20, 'rows': 1,'placeholder': 'Change note'}),label='')

    class Meta:

        fields = ['points', 'notes']


