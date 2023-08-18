from rest_framework import serializers


class SeriesSerializer(serializers.Serializer):
    Title = serializers.CharField()
    Year = serializers.CharField()
    imdbID = serializers.CharField()
    Poster = serializers.URLField()
    Season = serializers.CharField()
    Genre = serializers.CharField()
    class Meta:
        fields = ('Title', 'Year', 'imdbID', 'Poster', 'season', 'genre')  # List the fields you want to include in the response