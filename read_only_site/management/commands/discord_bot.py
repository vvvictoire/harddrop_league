"""Manages the discord_bot command"""

import math
import os
import sys

from django.core.management.base import BaseCommand

from discord.ext import commands
from discord import utils
from read_only_site.models import Match, Player
from trueskill import Rating, backends, quality_1vs1, setup

# More details about the constants on https://trueskill.org
# the initial mean of ratings
TRUESKILL_MU = 300.0
# the initial standard deviation of ratings. The recommended value is a third of mu.
TRUESKILL_SIGMA = 100.0
# the distance which guarantees about 76% chance of winning.
# The recommended value is a half of sigma.
TRUESKILL_BETA = 50.0
# the dynamic factor which restrains a fixation of rating.
# The recommended value is sigma per cent.
TRUESKILL_TAU = 3.0


BOT = commands.Bot(command_prefix='!')
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_discord_token'), 'r') as file:
    TOKEN = file.read().replace('\n', '')

@BOT.command()
async def matchmaking(context):
    """Finds a player to play against"""
    discord_id = context.message.author.id
    mention = context.message.author.mention
    try:
        player = Player.objects.get(discord_id=discord_id)
    except Player.DoesNotExist:
        await context.send(mention + ' you are not registered in the league!'
                           'type ' + BOT.command_prefix +
                           'register <jstris nickname> to register in the league')
        return
    # TrueSkill setup
    setup(mu=TRUESKILL_MU, sigma=TRUESKILL_SIGMA, beta=TRUESKILL_BETA, tau=TRUESKILL_TAU)
    if 'scipy' in backends.available_backends():
        # scipy can be used in the current environment
        backends.choose_backend(backend='scipy')
    # Setup the Rating for the asking player
    rating_asking = Rating(mu=player.trueskill_mu, sigma=player.trueskill_sigma)
    players = Player.objects.exclude(discord_id=discord_id)
    best_match = None
    best_quality = 0.0
    for player_match in players:
        player_rating = Rating(mu=player_match.trueskill_mu, sigma=player_match.trueskill_sigma)
        quality = quality_1vs1(rating_asking, player_rating)
        if quality > best_quality:
            best_quality = quality
            best_match = player_match
    await context.send(player.discord_nickname +
                       ' should play against ' +
                       best_match.discord_nickname)

@BOT.command()
async def register(context, jstris_handle: str):
    """Registers a new player (format: !register jstris_handle)"""
    discord_id = context.message.author.id
    player = str(context.message.author)
    nickname = context.message.author.display_name
    mention = context.message.author.mention
    # check if player already exists
    _, created = Player.objects.get_or_create(discord_id=discord_id,
                                              defaults={'discord_handle': player,
                                                        'discord_nickname': nickname,
                                                        'jstris_handle': jstris_handle})
    if created:
        await context.send(mention + ' is now registered!')
    else:
        await context.send(mention + ', you already were registered you cheeky m8')

@BOT.command()
async def rating(context, *discord_name):
    """Gives the current rating of the author of the message or of the player passed in argument"""
    if not discord_name:
        player_id = context.message.author.id
        mention = context.message.author.mention
        try:
            player = Player.objects.get(discord_id=player_id)
        except Player.DoesNotExist:
            await context.send(mention + ' you are not registered in the league!'
                               'type ' + BOT.command_prefix +
                               'register <jstris nickname> to register in the league')
        await context.send(player.discord_nickname +
                           ' rating: ' +
                           str(math.floor(player.trueskill_mu)))
    else:
        player_name = ' '.join(discord_name)
        try:
            player = Player.objects.get(discord_nickname=player_name)
        except Player.DoesNotExist:
            await context.send(player_name + ' is not registered in the league!')
        await context.send(player.discord_nickname +
                           ' rating: ' +
                           str(math.floor(player.trueskill_mu)))


@BOT.command()
async def update_name(context):
    """Updates the discord name in the database"""
    player_id = context.message.author.id
    mention = context.message.author.mention
    handle = str(context.message.author)
    display_name = context.message.author.display_name
    try:
        player = Player.objects.get(discord_id=player_id)
    except Player.DoesNotExist:
        await context.send(mention + ' you are not registered in the league!'
                           'type ' + BOT.command_prefix +
                           'register <jstris nickname> to register in the league')
        return
    player.discord_handle = handle
    player.discord_nickname = display_name
    player.save()
    await context.send('Your Discord name have been updated!')


@BOT.command()
async def winner(context):
    """Register a match, mentionning the winner by the loser"""
    loser_id = context.message.author.id
    loser_mention = context.message.author.mention
    if not context.message.mentions:
        await context.send('You must mention the winner!')
        return
    winner_mention = context.message.mentions[0].mention
    winner_id = context.message.mentions[0].id
    if winner_id == loser_id:
        await context.send('You can\'t win against yourself smh')
        return
    try:
        player_loser = Player.objects.get(discord_id=loser_id)
    except Player.DoesNotExist:
        await context.send(loser_mention +
                           ', you are not registered in the'
                           'league! Type ' +
                           BOT.command_prefix +
                           'register <jstris nickname> to register in the league.')
        return
    try:
        player_winner = Player.objects.get(discord_id=winner_id)
    except Player.DoesNotExist:
        await context.send(winner_mention + ' is not (yet) registered in the league!')
        return
    match = Match(player_1=player_loser, player_2=player_winner, winner=player_winner)
    try:
        match.save()
    except Exception as exception:
        await context.send(exception)
        return
    await context.send('Match saved!')

@BOT.command()
async def github(context):
    """Displays the link to the github repository"""
    await context.send('https://github.com/vvvictoire/harddrop_league')

@BOT.command()
async def update_id(context):
    """(Trucy only) Updates the Discord ids in the database"""
    if context.message.author.id != 156908510049861632:
        pass
    players = Player.objects.all()
    members = context.message.guild.members
    for player in players:
        member = utils.find(lambda m: m.display_name == player.discord_nickname, members)
        if member:
            player.discord_id = member.id
            player.save()

@BOT.command()
async def update_rankings(context):
    """(Trucy only) Recompute the rankings"""
    if context.message.author.id != 156908510049861632:
        pass
    players = Player.objects.all()
    for player in players:
        player.trueskill_sigma = 100.0
        player.trueskill_mu = 300.0
        player.save()
    matches = Match.objects.all()
    for match in matches:
        match.rate_match()
        match.save()

@BOT.command()
async def nini(context):
    """(Trucy only) Shuts down the bot"""
    if context.message.author.id != 156908510049861632:
        pass
    else:
        sys.exit(0)

class Command(BaseCommand):
    """Command class to manage the discord_bot command"""
    help = 'Launches the discord bot'

    def handle(self, *args, **options):
        BOT.run(TOKEN)
