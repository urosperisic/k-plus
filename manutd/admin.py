from django.contrib import admin
from .models import Player, Match

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('shirt_number', 'first_name', 'last_name', 'position', 'goals')
    search_fields = ('first_name', 'last_name')
    list_filter = ('position',)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('opponent', 'is_home', 'result', 'match_date')
    search_fields = ('opponent',)
    list_filter = ('is_home', 'match_date')