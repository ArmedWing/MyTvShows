from django import forms

from MyTvShows.tvshows.models import FavouriteTVShow


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


class SeriesDetailsForm(FavouriteTVShow):
    model = FavouriteTVShow
    fields = '__all__'
