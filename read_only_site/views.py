from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Player, Match

# Create your views here.
def index(request):
    return render(request, 'read_only_site/index.html')

def player(request, player_name):
    player = get_object_or_404(Player, discord_handle=player_name)
    context = {'player': player}
    return render(request, 'read_only_site/player.html', context)

def match(request, match_pk):
    match = get_object_or_404(Match, pk=match_pk)
    context = {'match': match}
    return render(request, 'read_only_site/match.html', context)

def leaderboard(request):
    players = Player.objects.order_by('-trueskill_mu')
    context = {'players': players}
    return render(request, 'read_only_site/leaderboard.html', context)

def latest_matches(request):
    matches = Match.objects.order_by('-played_on')
    context = {'matches': matches}
    return render(request, 'read_only_site/latest_matches.html', context)
