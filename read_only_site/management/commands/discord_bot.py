"""Manages the discord_bot command"""

import os
import sys

from django.core.management.base import BaseCommand

from discord.ext import commands
from discord import utils
from read_only_site.models import Match, Player

BOT = commands.Bot(command_prefix='!')
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_discord_token'), 'r') as file:
    TOKEN = file.read().replace('\n', '')

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
                           'register to register in the league.')
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
