from django.contrib import admin
from .models import Track, AudioFeatures, UserArchetype, UserProfile, UserInsight

# custom config for Track to make it more readable
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist_name', 'album_name', 'spotify_id')
    search_fields = ('title', 'artist_name', 'spotify_id')

# config for AudioFeatures
@admin.register(AudioFeatures)
class AudioFeaturesAdmin(admin.ModelAdmin):
    list_display = ('track', 'energy', 'valence', 'danceability', 'tempo')
    list_filter = ('energy', 'valence')

# Registro simple para los demás modelos
admin.site.register(UserArchetype)
admin.site.register(UserProfile)
admin.site.register(UserInsight)