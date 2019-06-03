from django.core.management.base import BaseCommand, CommandError
from read_only_site.models import Player, Match
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def ping(context):
    await context.send('pong')

@bot.command()
async def register(context):
    player = str(context.message.author)
    mention = context.message.author.mention
    # check if player already exists
    new_player, created = Player.objects.get_or_create(discord_handle=player)
    if created:
        await context.send(mention + ' is registered!')
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
        bot.run('NTg0MDMzMDk4NjM1NjczNjA2.XPQ0kA.OjMMkZ8SIKQxt9c4U1Qflj3Am6I')
