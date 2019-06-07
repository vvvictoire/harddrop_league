"""Admin panel settings"""

from django.contrib import admin

# Register your models here.
from .models import Player, Match

admin.site.register(Player)
admin.site.register(Match)
