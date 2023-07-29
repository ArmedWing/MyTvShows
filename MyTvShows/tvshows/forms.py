from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Show, Review, Genre, Episode, Season, Thread, Reply, UserModel


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

class ShowBaseForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = '__all__'
        exclude = ['profile', 'user']
        labels = {
            'image_url': 'Image URL',
        }


class ShowReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        exclude = ['series']


class ShowGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'
        exclude = ['series']


class ShowSeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = '__all__'
        exclude = ['episodes', 'series']
        labels = {
            'number': 'Number of seasons',
        }


class ShowEpisodesForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = '__all__'
        exclude = ['series', 'title', 'description', 'duration']

class ShowCreateForm(ShowBaseForm):
    pass


class ShowEditForm(ShowBaseForm):
    pass


class ShowDeleteForm(ShowBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_disabled_fields()

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance

    def __set_disabled_fields(self):
        for field in self.fields.values():
            field.widget.attrs['disabled'] = 'disabled'
            field.required = False



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


