
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from ..tvshows.models import TVShow, TemporarySearchResult

import requests
from django.shortcuts import render


def search_tv_show(request):
    search_query = request.GET.get('query')
    search_results = []

    if search_query:
        TemporarySearchResult.objects.all().delete()

        tvmaze_url = f'https://api.tvmaze.com/search/shows?q={search_query}'
        response = requests.get(tvmaze_url)
        search_data = response.json()

        for result in search_data:
            show = result.get('show', {})
            genres = show.get('genres', [])
            premiered = show.get('premiered')
            description = show.get('summary', '')

            tvmaze_id = show.get('id')
            num_seasons = len(get_show_seasons(tvmaze_id))  # Call the previous function

            # Get the poster image URL if available, or set it to an empty string if not
            poster_data = show.get('image')
            poster = poster_data.get('medium') if poster_data else ''

            # Create a TemporarySearchResult instance
            temp_search_result = TemporarySearchResult.objects.create(
                title=show.get('name'),
                year=premiered if premiered else 'N/A',
                tvmaze_id=tvmaze_id,
                poster=poster,
                genre=', '.join(genres),
                seasons=num_seasons,
                description=description,
            )

            search_results.append({
                'title': show.get('name'),
                'year': premiered if premiered else 'N/A',
                'tvmaze_id': tvmaze_id,
                'poster': poster,
                'genre': ', '.join(genres),
                'seasons': num_seasons,
                'description': description,
            })

    return render(request, 'series/series_search.html', {'search_results': search_results})



def get_show_seasons(tvmaze_id):
    seasons_url = f'https://api.tvmaze.com/shows/{tvmaze_id}/seasons'
    response = requests.get(seasons_url)
    return response.json()




@login_required
def add_to_favorites(request, tvmaze_id):
    # Get the selected TV show from the temporary table
    search_result = get_object_or_404(TemporarySearchResult, tvmaze_id=tvmaze_id)
    user = request.user

    # Create or get the TV show from the TVShow model
    tv_show, created = TVShow.objects.get_or_create(
        tvmaze_id=search_result.tvmaze_id,
        user=user,
        defaults={
            'title': search_result.title,
            'year': search_result.year,
            'poster': search_result.poster,
            'genre': search_result.genre,
            'seasons': search_result.seasons,
            'description': search_result.description,
        }
    )

    if created:
        # The TV show was successfully saved to favorites
        messages.success(request, f'{search_result.title} has been added to your favorites.')
    else:
        # The TV show was already in the user's favorites
        messages.warning(request, f'{search_result.title} is already in your favorites.')

    # Delete the selected TV show from the temporary table
    search_result.delete()
    TemporarySearchResult.objects.all().delete()

    return redirect('series_detail')


@login_required
def saved_shows(request):
    saved_shows = TVShow.objects.filter(user=request.user).order_by('id')
    return render(request, 'series/my_saved_shows.html', {'saved_shows': saved_shows})


def increase_counter(request, pk):
    tv_show = get_object_or_404(TVShow, pk=pk)
    tv_show.episodes_watched += 1
    tv_show.save()

    return redirect(reverse('series_detail'))


def show_details(request, pk):
    tv_show = get_object_or_404(TVShow, pk=pk)
    return render(request, 'series/series_details.html', {'tv_show': tv_show})

