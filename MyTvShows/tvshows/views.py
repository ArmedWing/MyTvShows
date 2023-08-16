from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import  AuthenticationForm

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy

from django.views import generic, View
from django.views.generic import CreateView, DetailView
from imdb import IMDb

from MyTvShows.tvshows.forms import  \
    ProfileEditForm, ShowReviewForm,  ThreadForm, ReplyForm, \
    UserEditForm, CustomUserCreationForm
from MyTvShows.tvshows.models import Profile, Review, Thread, Reply


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












def get_profile(user):
    return Profile.objects.filter(user=user).first()


def get_user(request):
    current_user = request.user
    return current_user








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




def index(request):
    ia = IMDb()
    latest_tv_shows = ia.get_keyword('Marvel', results=5)
    latest_tv_show_titles = [show['title'] for show in latest_tv_shows]

    # shows = get_shows(request)
    episodes = Episode.objects.all()

    # paginator = Paginator(shows, 4)
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
        'latest_tv_show_titles': latest_tv_show_titles,
    }

    return render(request, 'core/home-page.html', context)


@login_required
def profile_info(request):
    current_user = get_user(request)
    profile = get_profile(current_user)
    # shows = get_shows(request)

    context = {
        'profile': profile,
        # 'shows_length': len(shows),
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
    # shows = get_shows(request)

    if request.method == 'GET':
        profile.delete()
        # shows.delete()
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


def custom_404(request, exception):
    return render(request, 'core/custom_404_template.html', status=404)
