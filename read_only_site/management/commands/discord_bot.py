"""Manages the discord_bot command"""

import os

from django.core.management.base import BaseCommand

from discord.ext import commands
from read_only_site.models import Match, Player

BOT = commands.Bot(command_prefix='!')
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_discord_token'), 'r') as file:
    TOKEN = file.read().replace('\n', '')

@BOT.command()
async def register(context, jstris_handle: str):
    """Registers a new player"""
    player = str(context.message.author)
    nickname = context.message.author.display_name
    mention = context.message.author.mention
    # check if player already exists
    _, created = Player.objects.get_or_create(discord_handle=player,
                                              discord_nickname=nickname,
                                              jstris_handle=jstris_handle)
    if created:
        await context.send(mention + ' is now registered!')
    else:
        await context.send(mention + ', you already were registered you cheeky m8')

@BOT.command()
async def winner(context):
    """Register a match, mentionning the winner by the loser"""
    loser_handle = str(context.message.author)
    loser_mention = context.message.author.mention
    if not context.message.mentions:
        await context.send('You must mention the winner!')
        return
    winner_handle = str(context.message.mentions[0])
    winner_mention = context.message.mentions[0].mention
    try:
        player_loser = Player.objects.get(discord_handle=loser_handle)
    except Player.DoesNotExist:
        await context.send(loser_mention + ', you are not registered in the'
                                           'league! Type !register to register'
                                           'in the league.')
        return
    try:
        player_winner = Player.objects.get(discord_handle=winner_handle)
    except Player.DoesNotExist:
        await context.send(winner_mention + ' is not (yet) registered in the league!')
        return
    match = Match(player_1=player_loser, player_2=player_winner, winner=player_winner)
    match.save()
    await context.send('Match saved!')

class Command(BaseCommand):
    """Command class to manage the discord_bot command"""
    help = 'Launches the discord bot'

    def handle(self, *args, **options):
        BOT.run(TOKEN)
