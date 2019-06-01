from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Player, Match

admin.site.register(Player)
admin.site.register(Match)
