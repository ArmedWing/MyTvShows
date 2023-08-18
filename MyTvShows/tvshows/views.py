from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.generic import ListView
from imdb import IMDb
from MyTvShows.tvshows.forms import \
    ProfileEditForm, ThreadForm, ReplyForm, \
    UserEditForm, CustomUserCreationForm, AddRatingForm
from MyTvShows.tvshows.models import Profile, Thread, Reply, TVShow, Rating


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'user_auth/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('series_detail')
        return render(request, 'user_auth/register.html', {'form': form})


class LoginUserView(generic.View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'user_auth/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('series_detail')
            else:
                return redirect('index')
        return render(request, 'user_auth/login.html', {'form': form})


class LogoutUserView(generic.View):
    def get(self, request):
        logout(request)
        return redirect('index')


@method_decorator(login_required, name='dispatch')
class UsersInfoListView(ListView):
    template_name = 'core/users-info.html'
    context_object_name = 'users'
    ordering = 'pk'


    def get_queryset(self):
        current_user = self.request.user
        return User.objects.exclude(pk=current_user.pk).order_by(self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = self.request.user.is_superuser
        context['current_user'] = self.request.user
        context['users'] = User.objects.annotate(shows_count=Count('tvshow')).exclude(pk=context['current_user'].pk)
        return context


class CreateThreadView(View):
    template_name = 'forum/create_thread.html'

    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('thread_detail')
        return render(request, self.template_name, {'form': form})


class ThreadDeleteView(View):
    template_name = 'forum/delete_thread.html'

    def get(self, request, thread_id, *args, **kwargs):
        thread = get_object_or_404(Thread, id=thread_id)
        return render(request, self.template_name, {'thread': thread})

    def post(self, request, thread_id, *args, **kwargs):
        thread = get_object_or_404(Thread, id=thread_id)
        thread.delete()
        return redirect('thread_detail')


class CreateReplyView(View):
    template_name = 'forum/create_reply.html'
    form_class = ReplyForm

    def get(self, request, thread_id):
        thread = Thread.objects.get(pk=thread_id)
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'thread': thread})

    def post(self, request, thread_id):
        thread = Thread.objects.get(pk=thread_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.thread = thread
            reply.save()
            return redirect('view_thread', thread_id)
        return render(request, self.template_name, {'form': form, 'thread': thread})


class DeleteReplyView(View):
    def post(self, request, pk):
        reply = get_object_or_404(Reply, pk=pk)
        thread_id = reply.thread_id  # Save the thread ID before deleting the reply
        reply.delete()
        return redirect('view_thread', thread_id)


def get_profile(user):
    return Profile.objects.filter(user=user).first()


def get_user(request):
    current_user = request.user
    return current_user


def index(request):
    ia = IMDb()
    latest_tv_shows = ia.get_keyword('Marvel', results=5)
    latest_tv_show_titles = [show['title'] for show in latest_tv_shows]
    context = {
        'latest_tv_show_titles': latest_tv_show_titles,
    }

    return render(request, 'core/home-page.html', context)


@login_required
def profile_info(request):
    current_user = get_user(request)
    profile = get_profile(current_user)
    shows = TVShow.objects.filter(user=request.user)

    context = {
        'profile': profile,
        'shows_length': len(shows),
    }

    return render(request, 'profile/profile-details.html', context)


def update_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('details_profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'profile/update_profile.html', {'form': form})


def details_profile(request):
    current_user = get_user(request)
    profile = get_profile(current_user)

    context = {
        'profile': profile,
    }

    return render(request, 'profile/profile-details.html', context)


def delete_profile(request):
    current_user = get_user(request)
    profile = get_profile(current_user)
    shows = TVShow.objects.filter(user=request.user)

    if request.method == 'GET':
        profile.delete()
        shows.delete()
        return redirect('index')

    context = {
        'profile': profile
    }

    return render(request, 'profile/profile-delete.html', context)


def delete_user(request, user_id):
    if request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('users_info')


def edit_user(request, user_id):
    if request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            form = UserEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('users_info')
        else:
            form = UserEditForm(instance=user)

        context = {
            'form': form,
            'user': user,
        }

        return render(request, 'profile/edit_user.html', context)


def thread_detail(request):
    threads = Thread.objects.all()
    return render(request, 'forum/thread_detail.html', {'threads': threads})


def view_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    replies = Reply.objects.all()

    context = {
        'thread': thread,
        'replies': replies,
    }

    return render(request, 'forum/view_thread.html', context)


def custom_404(request, exception):
    return render(request, 'core/custom_404_template.html', status=404)


def add_rating(request, tv_show_id):
    if request.method == 'POST':
        user = request.user
        rating_value = int(request.POST.get('rating_value'))  # Extract rating_value from the form
        existing_rating = Rating.objects.filter(user=user, tv_show_id=tv_show_id).first()

        if existing_rating:
            existing_rating.rating_value = rating_value
            existing_rating.save()
        else:
            tv_show = get_object_or_404(TVShow, id=tv_show_id)
            rating = Rating(user=user, tv_show=tv_show, rating_value=rating_value)
            rating.save()

        return redirect('show_details', tv_show_id)
    else:
        return HttpResponseBadRequest("Invalid request method.")
