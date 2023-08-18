from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Thread, Reply, UserModel, Rating


class ProfileBaseForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'profile_picture': 'Profile Picture',
        }


class ProfileCreateForm(ProfileBaseForm):
    pass


class ProfileEditForm(ProfileBaseForm):
    # ProfileBaseForm.Meta.fields.append('profile_picture')
    pass



class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name']



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password1', 'password2']

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None


class AddRatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = '__all__'


