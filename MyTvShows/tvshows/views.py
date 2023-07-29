from django.contrib.auth import  login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import  AuthenticationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import CreateView
from MyTvShows.tvshows.forms import ShowCreateForm, ShowDeleteForm, ShowEditForm, \
    ProfileEditForm, ShowReviewForm, ShowGenreForm, ShowSeasonForm, ShowEpisodesForm, ThreadForm, ReplyForm, \
    UserEditForm, CustomUserCreationForm
from MyTvShows.tvshows.models import Show, Profile, Review, Genre, Season, Episode, Thread, Reply


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'user_auth/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
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
                return redirect('users_info')
            else:
                return redirect('index')
        return render(request, 'user_auth/login.html', {'form': form})


class LogoutUserView(generic.View):
    def get(self, request):
        logout(request)
        return redirect('index')


class AddShowReview(CreateView):
    model = Review
    form_class = ShowReviewForm
    template_name = 'shows/add-review.html'
    context_object_name = 'show'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['show'] = Show.objects.filter(pk=pk).first()
        return context

    def form_valid(self, form):
        pk = self.kwargs['pk']
        form.instance.series_id = pk
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('details_show', kwargs={'pk': pk})


def DeleteReview(request, pk):
    review = get_review(pk)
    review = get_object_or_404(Review, id=review.id)
    show_id = review.series_id
    review.delete()

    return redirect('details_show', pk=show_id)


class AddShowView(View):
    def get(self, request):
        form = ShowCreateForm()
        genre = ShowGenreForm()
        seasons = ShowSeasonForm()
        episodes = ShowEpisodesForm()

        context = {
            'form': form,
            'genre': genre,
            'seasons': seasons,
            'episodes': episodes,
        }

        return render(request, 'shows/add-show.html', context)

    def post(self, request):
        form = ShowCreateForm(request.POST)
        genre = ShowGenreForm(request.POST)
        seasons = ShowSeasonForm(request.POST)
        episodes = ShowEpisodesForm(request.POST)

        if form.is_valid() and genre.is_valid() and seasons.is_valid() and episodes.is_valid():
            show = form.save(commit=False)
            show.user_id = request.user.id
            show.save()

            genre_obj = genre.save(commit=False)
            genre_obj.series_id = show.pk
            genre_obj.save()

            seasons_obj = seasons.save(commit=False)
            seasons_obj.series_id = show.pk
            seasons_obj.save()

            episodes_obj = episodes.save(commit=False)
            episodes_obj.series_id = show.pk
            episodes_obj.save()

            return redirect('index')

        context = {
            'form': form,
            'genre': genre,
            'seasons': seasons,
            'episodes': episodes,
        }

        return render(request, 'shows/add-show.html', context)


class ShowDetailsView(View):
    def get(self, request, pk):
        show = get_object_or_404(Show, pk=pk)

        review = Review.objects.filter(series_id=pk).first()
        reviews = Review.objects.filter(series_id=pk)

        show_genre = Genre.objects.filter(series_id=pk).first()
        genre = show.genre_set.first()

        show_season = Season.objects.filter(series_id=pk).first()
        season = show.season_set.first()

        show_episode = Episode.objects.filter(series_id=pk).first()
        episode = show.episode_set.first()

        context = {
            'show': show,
            'review': review,
            'reviews': reviews,
            'show_genre': show_genre,
            'genre': genre,
            'show_season': show_season,
            'season': season,
            'show_episode': show_episode,
            'episode': episode,
        }

        return render(request, 'shows/show-details.html', context)



class EditShowView(View):
    def get(self, request, pk):
        current_user = get_user(request)
        profile = get_profile(current_user)
        show = get_object_or_404(Show, pk=pk)

        form = ShowEditForm(instance=show)
        genre = ShowGenreForm()
        seasons_instance = get_object_or_404(Season, series_id=pk)
        seasons = ShowSeasonForm(instance=seasons_instance)
        episodes_instance = get_object_or_404(Episode, series_id=pk)
        episodes = ShowEpisodesForm(instance=episodes_instance)

        context = {
            'profile': profile,
            'form': form,
            'show': show,
            'genre': genre,
            'seasons': seasons,
            'episodes': episodes,
        }

        return render(request, 'shows/edit-show.html', context)

    def post(self, request, pk):
        current_user = get_user(request)
        profile = get_profile(current_user)
        show = get_object_or_404(Show, pk=pk)

        form = ShowEditForm(request.POST, instance=show)
        genre = ShowGenreForm(request.POST)
        seasons_instance = get_object_or_404(Season, series_id=pk)
        seasons = ShowSeasonForm(request.POST, instance=seasons_instance)
        episodes_instance = get_object_or_404(Episode, series_id=pk)
        episodes = ShowEpisodesForm(request.POST, instance=episodes_instance)

        if form.is_valid() and genre.is_valid() and seasons.is_valid():
            form.save()

            genre = genre.save(commit=False)
            genre.series_id = show.pk
            genre.save()

            seasons = seasons.save(commit=False)
            seasons.series_id = show.pk
            seasons.save()

            episodes = episodes.save(commit=False)
            episodes.series_id = show.pk
            episodes.save()

            return redirect('details_show', pk=show.pk)

        context = {
            'profile': profile,
            'form': form,
            'show': show,
            'genre': genre,
            'seasons': seasons,
            'episodes': episodes,
        }

        return render(request, 'shows/edit-show.html', context)


def IncreaseCounter(request, pk):
    episode = get_episode(pk)
    Episode.objects.filter(pk=episode.pk).update(episodes_watched=F("episodes_watched") + 1)
    episode.refresh_from_db()

    return redirect('details_show', pk=pk)


def get_episode(pk):
    return Episode.objects.filter(series_id=pk).get()


def get_profile(user):
    return Profile.objects.filter(user=user).first()


def get_user(request):
    current_user = request.user
    return current_user


def get_shows(request):
    if request.user.is_authenticated:
        return Show.objects.filter(user=request.user).order_by('pk')
    else:
        return Show.objects.none()



def get_show(pk):
    return Show.objects.filter(pk=pk).get()


def get_review(pk):
    return Review.objects.filter(pk=pk).get()


def users_Info(request):
    is_admin = request.user.is_superuser

    current_user = request.user
    users = User.objects.exclude(pk=current_user.pk).order_by('pk')  # Exclude the logged-in user

    context = {
        'is_admin': is_admin,
        'current_user': current_user,
        'users': users,
    }

    return render(request, 'core/users-info.html', context)


def shows_info(request):
    is_admin = request.user.is_superuser
    shows = Show.objects.all()

    paginator = Paginator(shows, 4)
    page = request.GET.get('page')
    try:
        shows_page = paginator.page(page)
    except PageNotAnInteger:
        shows_page = paginator.page(1)
    except EmptyPage:
        shows_page = paginator.page(paginator.num_pages)

    context = {
        'is_admin': is_admin,
        'shows': shows,
        'shows_page': shows_page,
    }

    return render(request, 'core/shows-info.html', context)

def index(request):
    shows = get_shows(request)
    episodes = Episode.objects.all()

    paginator = Paginator(shows, 4)
    page = request.GET.get('page')
    try:
        shows_page = paginator.page(page)
    except PageNotAnInteger:
        shows_page = paginator.page(1)
    except EmptyPage:
        shows_page = paginator.page(paginator.num_pages)

    current_user = request.user
    users = User.objects.exclude(pk=current_user.pk)  # Exclude the logged-in user

    context = {
        'shows_page': shows_page,
        'shows': shows,
        'current_user': current_user,
        'users': users,
        'episodes': episodes,
    }

    return render(request, 'core/home-page.html', context)


@login_required
def profile_info(request):
    current_user = get_user(request)
    profile = get_profile(current_user)
    shows = get_shows(request)

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
    return render(request, 'update_profile.html', {'form': form})


def delete_show(request, pk):
    current_user = get_user(request)
    profile = get_profile(current_user)
    show = get_show(pk)

    if request.method == 'GET':
        form = ShowDeleteForm(instance=show)
    else:
        form = ShowDeleteForm(request.POST, instance=show)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {
        'profile': profile,
        'show': show,
        'form': form,
    }

    return render(request, 'shows/delete-show.html', context)


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
    shows = get_shows(request)

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

        return render(request, 'edit_user.html', context)


def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('thread_detail')
    else:
        form = ThreadForm()

    return render(request, 'create_thread.html', {'form': form})


def create_reply(request, thread_id):
    thread = Thread.objects.get(pk=thread_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.thread = thread
            reply.save()
            return redirect('view_thread', thread_id)
    else:
        form = ReplyForm()

    return render(request, 'create_reply.html', {'form': form, 'thread': thread})


def thread_detail(request):
    threads = Thread.objects.all()
    return render(request, 'thread_detail.html', {'threads': threads})


def view_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    replies = Reply.objects.all()

    context = {
        'thread': thread,
        'replies': replies,
    }

    return render(request, 'view_thread.html', context)

