# Dependencies

import discord
import os
import random
import time
from discord.ext.commands import *
from discord.ext import *
from time import *


client = commands.Bot(command_prefix="-") # Init the client
client.remove_command('help') # Remove the existing help command with a better one.

# Start

@client.event
async def on_connect():
    print("Connecting")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
    activity=discord.Game(f'Installing Arch'))
    print('Connected.')

@client.event
async def on_disconnect():
    print("Disconnected!")

# Stop

# Standard & common commands

@client.command() # Ping command
async def ping(ctx):
    await ctx.send(f':ping_pong: Client latency is **{round(client.latency * 1000)}ms.**')

@commands.command(aliases=['server-info','guild-info','server'])
async def serverinfo(self,ctx):
    nbr_member=len(ctx.guild.members)
    nbr_text=len(ctx.guild.text_channels)
    nbr_vc=len(ctx.guild.voice_channels)
    created = ctx.guild.created_at
    embed=discord.Embed(title=f"{ctx.guild.name}",color=discord.Colour.red)
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    embed.add_field(name="Server created on", value=f"{created.strftime('%Y-%m-%d')}", inline=True)
    embed.add_field(name="Text Channels", value=f"{nbr_text}", inline=True)
    embed.add_field(name="Identity", value=f"{ctx.guild.id}", inline=True)
    embed.add_field(name="Voice Channels", value=f'{nbr_vc}', inline=True)
    embed.add_field(name="Owner",value=f'{ctx.guild.owner}', inline=True)
    embed.add_field(name="Members",value=f'{nbr_member}', inline=True)
    embed.add_field(name=f'System Channel',value=f'{ctx.guild.system_channel}',inline=True)
    await ctx.send(embed=embed)

@client.command(aliases=["whois"]) # User-info
async def userinfo(ctx, member: discord.Member = None):
    if not member:  
        member = ctx.message.author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.red(), timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="Discord ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Number of roles:", value="".join([role.mention for role in roles]))
    print(member.top_role.mention)
    await ctx.send(embed=embed)

@client.command(aliases=["profilepic"])
async def avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    embed = discord.Embed(colour=discord.Colour.red(), timestamp=ctx.message.created_at,
                          title=f"Avatar of {member}")
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

@client.command()
async def kill(ctx, *, person):
    await ctx.send(f"**{person} gets yeeted off of a cliff by God.**")

@client.command()
async def invite(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=778576098195013662&permissions=8&scope=bot")

@client.command()
async def source(ctx):
    await ctx.send("The source code is at GitHub: https://github.com/AaronTechnic/ermine")

@client.command() # "Say" command
async def say(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send(msg)

@say.error # Error handling for say
async def say_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("You are missing the required arguments.")

# Moderation

@client.command() #Kick command
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"{member} has been kicked.")
    except:
        await ctx.send("This user is a moderator and cannot be kicked.")

@kick.error # Error handling for kick
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You do not have permission to kick users.")
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("You must mention a user to kick.")


@client.command() # Ban command
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member} has been banned from this server.")
    except:
        await ctx.send("This user is a moderator and cannot be banned.")


@ban.error # Error handling for ban
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You do not have permission to ban users.")
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("You must mention a user to ban.")

@client.command() # Unban command
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@unban.error # Error handling for unban
async def unban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You do not have permission to unban users.")
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("You must mention a user to revoke a ban!")

@client.command()
@has_permissions(manage_roles = True)
async def mute(ctx, member: discord.Member):
    guild = ctx.guild
    try:
        mutedrole = discord.utils.get(guild.roles, name='Muted')
        await member.add_roles(mutedrole, reason=None, atomic=True)
        await ctx.send("{member} has been muted!")
    except:
        await ctx.send("**TIP:** As that user has been muted, you can unmute them my executing `e!unmute`.")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to mute people.")
    if isinstance(error, MissingRequiredArgument):
            await ctx.send("You must mention a user to mute!")


@client.command() # Unmute command
@has_permissions(manage_roles = True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedrole = discord.utils.get(guild.roles, name='Muted')
    await member.remove_roles(mutedrole, reason=None, atomic=True)
    await ctx.send("{member} has been unmuted!")

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You do not have permission to revoke mutes.")
    if isinstance(error, MissingRequiredArgument):
            await ctx.send("You must mention a user to revoke mutes!")

@client.command(aliases=["rm"])
@has_permissions(manage_messages=True)
async def purge(ctx, amount : int):
    await ctx.channel.purge(limit=amount+1)
    sent = await ctx.send(F"Deleted **{amount}** messages!")
    sleep(1)
    await sent.delete()

# End of moderation

@client.command()
async def help(ctx):
    embed=discord.Embed(title="Help menu in development.",color=0xe74c3c)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="Server created on", value=ctx.guild.created_at.strftime('%Y-%m-%d'), inline=True)
    embed.add_field(name="Identity", value=ctx.guild.id, inline=True)
    embed.add_field(name="Voice Channels", value=len(ctx.guild.voice_channels), inline=True)
    embed.add_field(name="Owner",value=ctx.guild.owner, inline=True)
    embed.add_field(name="Members",value=len(ctx.guild.members), inline=True)
    embed.add_field(name=f'System Channel',value=ctx.guild.system_channel,inline=True)
    await ctx.send(embed=embed)

# Bot token

client.run(os.environ['DISCORD_TOKEN'])
