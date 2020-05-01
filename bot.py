import discord
import datetime
#import youtube_dl
import os
#now_date = datetime.datetime.now()
from discord.ext import commands
from discord.utils import get

prefix = '.'
client = commands.Bot( command_prefix = prefix )
client.remove_command( 'help' )

@client.event
async def on_ready():
	#print( 'Bot connected: ' + client.user.name + '\n---------------' )
	await client.change_presence( status = discord.Status.online, activity = discord.Game( '.help' ))

# Clear
@client.command( pass_context = True )
async def clear( ctx, amount = 0 ):
	await ctx.channel.purge( limit = 1 + amount )
	#print( '[log]', datetime.datetime.now(), '| clear chat:', amount, '|', ctx.message.author)

# Hello
@client.command( pass_context = True )
async def hello( ctx, amount = 1 ):
	await ctx.channel.purge( limit = amount )
	author = ctx.message.author
	await ctx.send( f'Hello { author.mention }' )

# Help
@client.command( pass_context = True )
async def help( ctx ):
	await ctx.channel.purge( limit = 1 )
	emb = discord.Embed( title = 'Commands:' )
	emb.add_field( name = '{}hello'.format( prefix ), value = 'Приветствие' )
	emb.add_field( name = '{}clear'.format( prefix ), value = 'Очистить чат' )
	emb.add_field( name = '{}sendme'.format( prefix ), value = 'Отправить мое сообщение в личные' )
	await ctx.send( embed = emb )
"""
# Kick
@client.command( pass_context = True )
@commands.has_permissions( administrator = True)
async def kick( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )
	await member.kick( reason = reason )
	await ctx.send( f'kick user { member.mention }')

# Ban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True)
async def ban( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )
	await member.ban( reason = reason )
	await ctx.send( f'ban user { member.mention }')

# Unban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True)
async def unban( ctx, *, member ):
	await ctx.channel.purge( limit = 1 )
	banned_users = await ctx.guild.bans()
	for ban_entry in banned_users:
		user = ban_entry.user
		# Name#9999
		await ctx.guild.unban( user )
		await ctx.send( f'unbanned user { user.mention }')
		return
"""
# LS
@client.command()
async def sendme( ctx, message ):
	await ctx.channel.purge( limit = 1 )
	await ctx.author.send( message )
"""
# Connect Voice
@client.command()
async def join( ctx ):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)
	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
		await ctx.send( f'Bot connected to channel: {channel}')

# Leave Voice
@client.command()
async def leave( ctx ):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)
	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await channel.connect()
		await ctx.send( f'Bot disconnected to channel: {channel}')

@client.command()
async def play( ctx, url : str ):
	song_there = os.path.isfile('song.mp3')
	try:
		if song_there:
			os.remove('song.mp3')
			print('[log] Old mp3 delete')
	except PermissionError:
		print('[log] Do not delete file error')
	await ctx.send('Please wait..')
	voice = get(client.voice_clients, guild = ctx.guild)
	ydl_opts = {
		'format' : 'bestaudio/best',
		'postprocessors' : [{
			'key' : 'FFmpegExtractAudio',
			'preferredcodec' : 'mp3',
			'preferredquality' : '192'
		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print('[log] Loading music..')
		ydl.download([url])
	for file in os.listdir('./'):
		if file.endswith('.mp3'):
			name = file
			print('[log] Rename file: {file}')
			os.rename(file, 'song.mp3')
	voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print( f'{name}, music finished playing' ))
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.07
	song_name = name.rsplit('-', 2)
	await ctx.send( f'Now playing: {song_name[0]}') 
"""
# Connect
token = os.environ.get('Bot_Token')
client.run(str(token))
