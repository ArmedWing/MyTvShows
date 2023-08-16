import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from ..tvshows.models import TVShow, TemporarySearchResult


def search_tv_show(request):
    search_query = request.GET.get('query')
    search_results = []

    if search_query:
        TemporarySearchResult.objects.all().delete()

        omdb_url = f'https://www.omdbapi.com/?s={search_query}&type=series&apikey=52155298'
        response = requests.get(omdb_url)
        search_data = response.json()


        for result in search_data.get('Search', []):
            omdb_details_url = f'https://www.omdbapi.com/?i={result.get("imdbID")}&apikey=52155298'
            details_response = requests.get(omdb_details_url)
            details_data = details_response.json()
            print(details_data)

            total_seasons = details_data.get('totalSeasons', 'N/A')
            genre = details_data.get('Genre', 'N/A')

            if total_seasons != 'N/A':
                num_seasons = int(total_seasons)
            else:
                num_seasons = 0

            TemporarySearchResult.objects.create(
                title=result.get('Title'),
                year=result.get('Year'),
                imdb_id=result.get('imdbID'),
                poster=result.get('Poster'),
                genre=genre,
                seasons=num_seasons,  # Assign the calculated value
            )

            search_results.append({
                'title': result.get('Title'),
                'year': result.get('Year'),
                'imdb_id': result.get('imdbID'),
                'poster': result.get('Poster'),
                'genre': genre,
                'seasons': num_seasons,
            })

    return render(request, 'shows/series_search.html', {'search_results': search_results})


@login_required
def add_to_favorites(request, imdb_id):
    # Get the selected TV show from the temporary table
    search_result = get_object_or_404(TemporarySearchResult, imdb_id=imdb_id)

    # Create or get the TV show from the TVShow model
    tv_show, created = TVShow.objects.get_or_create(
        imdb_id=search_result.imdb_id,
        defaults={
            'title': search_result.title,
            'year': search_result.year,
            'poster': search_result.poster,
            'genre': search_result.genre,
            'seasons': search_result.seasons

        }
    )

    if created:
        # The TV show was successfully saved to favorites
        messages.success(request, f'{search_result.title} has been added to your favorites.')
    else:
        # The TV show was already in the user's favorites
        messages.warning(request, f'{search_result.title} is already in your favorites.')

    # Delete all TV shows from the temporary table
    search_result.delete()
    TemporarySearchResult.objects.all().delete()

    return redirect('series_detail')


@login_required
def saved_shows(request):
    saved_shows = TVShow.objects.all()
    return render(request, 'shows/series_details.html', {'saved_shows': saved_shows})


def increase_counter(request, pk):
    tv_show = get_object_or_404(TVShow, pk=pk)
    tv_show.episodes_watched += 1
    tv_show.save()

    return redirect(reverse('series_detail'))


def show_details(request, pk):
    tv_show = get_object_or_404(TVShow, pk=pk)
    return render(request, 'shows/show_details.html', {'tv_show': tv_show})

