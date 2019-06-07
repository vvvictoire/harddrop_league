from django.core.management.base import BaseCommand, CommandError
from read_only_site.models import Player, Match
import discord
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_discord_token'), 'r') as file:
    token = file.read().replace('\n', '')

@bot.command()
async def register(context, jstris_handle: str):
    player = str(context.message.author)
    nickname = context.message.author.display_name
    mention = context.message.author.mention
    # check if player already exists
    new_player, created = Player.objects.get_or_create(discord_handle=player,
                                                       discord_nickname=nickname,
                                                       jstris_handle=jstris_handle)
    if created:
        await context.send(mention + ' is now registered!')
    else:
        await context.send(mention + ', you already were registered you cheeky m8')

@bot.command()
async def winner(context):
    loser = str(context.message.author)
    loser_mention = context.message.author.mention
    if len(context.message.mentions < 1):
        await context.send('You must mention the winner!')
    winner = str(context.message.mentions[0])
    winner_mention = context.message.mentions[0].mention
    try:
        player_loser = Player.objects.get(discord_handle=loser)
    except Player.DoesNotExist:
        await context.send(loser_mention + ', you are not registered in the league! Type !register to register in the league.')
        return
    try:
        player_winner = Player.objects.get(discord_handle=winner)
    except Player.DoesNotExist:
        await context.send(winner_mention + ' is not (yet) registered in the league!')
        return
    match = Match(player_1=player_loser, player_2=player_winner, winner=player_winner)
    match.save()
    await context.send('Match saved!')

class Command(BaseCommand):
    help = 'Launches the discord bot'

    def handle(self, *args, **options):
        bot.run(token)
