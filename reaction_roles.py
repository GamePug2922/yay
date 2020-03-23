import discord
import psutil
import os
import chalk
import asyncio

from datetime import datetime
from discord.ext import commands
from discord.ext.commands import errors
from utils import default
import asyncpg
from discord.utils import get


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Channel ID = "channel_id_content.content"
    # Message ID = "message_id_content.content"
    # Emoji = "emoji_content.content"
    # Role = "role_content.content"


    @commands.command()
    @commands.guild_only()
    async def add_reaction_role(self, ctx):
        guild_id = str(ctx.guild.id)
        setup = await self.bot.pg_con.fetch("SELECT * FROM setup WHERE guild_id = $1", guild_id)
        if not setup:
            await ctx.send("This server is unconfigured, please get the server owner to run `-setup`.")
        else:
            # Purging the authors message (command)
            await ctx.message.delete()

            # Getting Embed Color
            guild_id = str(ctx.guild.id)
            color_find = await self.bot.pg_con.fetch("SELECT color FROM config WHERE guild_id = $1", guild_id)
            color_found = int(color_find[0]['color'], 16)
            guild_id = str(ctx.guild.id)

            # Welcome / Channel ID (ask)
            message_id_embed = discord.Embed(title="✈️ Reaction Role", description="Hello, lets get started with reaction roles all you need to do is specify the message ID.", color=color_found)
            message_id = await ctx.send(embed=message_id_embed)

            # Channel ID Check (ask)
            channel_embed = embed=discord.Embed(title="✈️ Reaction Role", description="Finally, tag the channel.", color=color_found)

            # Emoji ID Check (ask)
            emoji_embed = embed=discord.Embed(title="✈️ Reaction Role", description="Tell me the emoji.", color=color_found)

            # Role (ask)
            role_embed = embed=discord.Embed(title="✈️ Reaction Role", description="Tell me the role name.", color=color_found)

            io_embed = embed=discord.Embed(title="✈️ Reaction Role", description="Would you like to log this reaction role?", color=color_found)

            # Success
            done_embed = embed=discord.Embed(title="✈️ Reaction Role", description="I have successfully created the reaction role in my database.", color=color_found)


            def message_id_check(m):
                return m.content and m.author == ctx.author
            message_id_content = await self.bot.wait_for('message', check=message_id_check, timeout=60.0)
            try:
                await message_id.edit(embed=emoji_embed) # Deleting the channel_id_embed message
                await message_id_content.delete()
            except:
                return

            def emoji_check(m):
                return m.content and m.author == ctx.author
            emoji_content = await self.bot.wait_for('message', check=emoji_check, timeout=60.0)
            try:
                await emoji_content.delete()
                await message_id.edit(embed=role_embed)
            except:
                return

            def role_check(m):
                return m.content and m.author == ctx.author
            role_content = await self.bot.wait_for('message', check=role_check, timeout=60.0)
            try:
                await role_content.delete()
                await message_id.edit(embed=channel_embed)
            except:
                return

            def channel_check(m):
                return m.content and m.author == ctx.author
            msg = await self.bot.wait_for('message', check=channel_check, timeout=60.0)
            try:
                await msg.delete()
                await message_id.edit(embed=io_embed)
                msg = msg.content
                msg = msg.replace("<","")
                msg = msg.replace(">","")
                msg = msg.replace("#","")
                a = int(msg)
            except:
                return

            await message_id.add_reaction("❎")
            await message_id.add_reaction("✅")
            def acv(reaction, user):
                if reaction.emoji == '❎':
                    return user == ctx.author and str(reaction.emoji) == '❎'
                elif reaction.emoji == '✅':
                    return user == ctx.author and str(reaction.emoji) == '✅'


            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=acv)
            except asyncio.TimeoutError as e:
                e_error=discord.Embed(title="**<a:crossmark:676105813064155169> Error**", description=f"```You took too long. Please try again. ```", color=0xDD2E44)
                await ctx.send(embed=e_error)
            else:
                await message_id.clear_reactions()
                if reaction.emoji == '❎':
                    await message_id.edit(embed=done_embed)
                    message_id_db = str(message_id_content.content)
                    messageid = str(message_id_content.content)

                    guild_id_db = str(ctx.guild.id)

                    emoji_db = str(emoji_content.content)
                    emoji = str(emoji_content.content)

                    role_db = str(role_content.content)

                    await self.bot.pg_con.execute("INSERT INTO reaction (message_id, guild_id, emoji, role, log) VALUES ($1, $2, $3, $4, FALSE)", message_id_db, guild_id_db, emoji_db, role_db)

                    try:
                        channel = self.bot.get_channel(a)
                        message = await channel.fetch_message(messageid)
                        await message.add_reaction(emoji)
                    except:
                        return


                elif reaction.emoji == '✅':
                    await message_id.edit(embed=done_embed)
                    message_id_db = str(message_id_content.content)
                    messageid = str(message_id_content.content)

                    guild_id_db = str(ctx.guild.id)

                    emoji_db = str(emoji_content.content)
                    emoji = str(emoji_content.content)

                    role_db = str(role_content.content)

                    await self.bot.pg_con.execute("INSERT INTO reaction (message_id, guild_id, emoji, role, log) VALUES ($1, $2, $3, $4, TRUE)", message_id_db, guild_id_db, emoji_db, role_db)

                    try:
                        channel = self.bot.get_channel(a)
                        message = await channel.fetch_message(messageid)
                        await message.add_reaction(emoji)
                    except:
                        return


    @commands.command()
    @commands.guild_only()
    async def remove_reaction_role(self, ctx):
        guild_id = str(ctx.guild.id)
        setup = await self.bot.pg_con.fetch("SELECT * FROM setup WHERE guild_id = $1", guild_id)
        if not setup:
            await ctx.send("This server is unconfigured, please get the server owner to run `-setup`.")
        else:
            # Purging the authors message (command)
            await ctx.message.delete()

            # Getting Embed Color
            guild_id = str(ctx.guild.id)
            color_find = await self.bot.pg_con.fetch("SELECT color FROM config WHERE guild_id = $1", guild_id)
            color_found = int(color_find[0]['color'], 16)
            guild_id = str(ctx.guild.id)

            # Welcome / Channel ID (ask)
            message_id_embed = discord.Embed(title="✈️ Reaction Role", description="Hello, lets get started with removing reaction roles all you need to do is specify the message ID.", color=color_found)
            message_id = await ctx.send(embed=message_id_embed)

            # Channel ID Check (ask)
            channel_embed = embed=discord.Embed(title="✈️ Reaction Role", description="Finally, tag the channel.", color=color_found)

            # Emoji ID Check (ask)
            emoji_embed = embed=discord.Embed(title="✈️ Reaction Role", description="Tell me the emoji.", color=color_found)

            # Success
            done_embed = embed=discord.Embed(title="✈️ Reaction Role", description="I have successfully removed the reaction role in my database.", color=color_found)


            def message_id_check(m):
                return m.content and m.author == ctx.author
            message_id_content = await self.bot.wait_for('message', check=message_id_check, timeout=60.0)
            try:
                await message_id.edit(embed=emoji_embed) # Deleting the channel_id_embed message
                await message_id_content.delete()
            except:
                return

            def emoji_check(m):
                return m.content and m.author == ctx.author
            emoji_content = await self.bot.wait_for('message', check=emoji_check, timeout=60.0)
            try:
                await emoji_content.delete()
                await message_id.edit(embed=channel_embed)
            except:
                return

            def channel_check(m):
                return m.content and m.author == ctx.author
            msg = await self.bot.wait_for('message', check=channel_check, timeout=60.0)
            try:
                await msg.delete()
                await message_id.edit(embed=done_embed)
                msg = msg.content
                msg = msg.replace("<","")
                msg = msg.replace(">","")
                msg = msg.replace("#","")
                a = int(msg)
            except:
                return

            message_id_db = str(message_id_content.content)
            messageid = str(message_id_content.content)

            guild_id_db = str(ctx.guild.id)

            emoji_db = str(emoji_content.content)
            emoji = str(emoji_content.content)

            await self.bot.pg_con.execute("DELETE FROM reaction WHERE guild_id = $1 AND message_id = $2 AND emoji = $3", guild_id_db, message_id_db, emoji_db)

            try:
                channel = self.bot.get_channel(a)
                message = await channel.fetch_message(messageid)
                await message.clear_reaction(emoji)
            except:
                return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Getting the guild
        guild_id = str(payload.guild_id) # Fetching Guild ID

        guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds) # Fetching Guild

        emoji = str(payload.emoji) # Fetching Emoji

        message_id = str(payload.message_id) # fetching message id

        db_msgid = await self.bot.pg_con.fetchrow("SELECT message_id FROM reaction WHERE guild_id = $1 AND message_id = $2 AND emoji = $3", guild_id, message_id, emoji)

        db_emoji = await self.bot.pg_con.fetchrow("SELECT emoji FROM reaction WHERE guild_id = $1 AND message_id = $2 AND emoji = $3", guild_id, message_id, emoji)

        db_role = await self.bot.pg_con.fetchrow("SELECT role FROM reaction WHERE guild_id = $1 AND message_id = $2 AND emoji = $3", guild_id, message_id, emoji)

        db_log = await self.bot.pg_con.fetchrow("SELECT log FROM reaction WHERE guild_id = $1 AND message_id = $2 AND emoji = $3 AND log = TRUE", guild_id, message_id, emoji)

        try:

            if message_id in db_msgid[0]:
                user = payload.member
                guild_role = self.bot.get_guild(payload.guild_id)
                role = discord.utils.get(guild_role.roles, name=db_role[0])
                await user.add_roles(role)


                if db_log:
                    # Logging
                    guild_id = str(payload.guild_id)
                    log_channel = await self.bot.pg_con.fetch("SELECT log_channel FROM config WHERE guild_id = $1", guild_id)
                    log = int(log_channel[0]['log_channel'])
                    channel = self.bot.get_channel(log)
                    embed=discord.Embed(title="⚠️ **Warning!**", description=f"**{user.name}#{user.discriminator}** has reacted to a reaction role.", color=0xffff00)
                    embed.add_field(name="Message ID", value=db_msgid[0], inline=True)
                    embed.add_field(name="Emoji", value=db_emoji[0], inline=True)
                    embed.add_field(name="Role", value=db_role[0], inline=True)
                    await channel.send(embed=embed)

        except:
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # Getting the guild_id
        guild_id = str(payload.guild_id) # Fetching Guild ID

        guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds) # Fetching Guild

        emoji = str(payload.emoji) # Fetching Emoji

        message_id = str(payload.message_id) # fetching message id

        db_msgid = await self.bot.pg_con.fetchrow("SELECT message_id FROM reaction WHERE guild_id = $1 AND message_id = $2 AND emoji = $3", guild_id, message_id, emoji)

        db_emoji = await self.bot.pg_con.fetchrow("SELECT emoji FROM reaction WHERE guild_id = $1 AND message_id = $2 AND emoji = $3", guild_id, message_id, emoji)

        db_role = await self.bot.pg_con.fetchrow("SELECT role FROM reaction WHERE guild_id = $1 AND message_id = $2 AND emoji = $3", guild_id, message_id, emoji)

        db_log = await self.bot.pg_con.fetchrow("SELECT log FROM reaction WHERE guild_id = $1 AND message_id = $2 AND emoji = $3 AND log = TRUE", guild_id, message_id, emoji)

        get_member = self.bot.get_guild(payload.guild_id)
        user = get_member.get_member(payload.user_id)

        try:

            if message_id in db_msgid[0]:
                guild_role = self.bot.get_guild(payload.guild_id)
                role = discord.utils.get(guild_role.roles, name=db_role[0])
                await user.remove_roles(role)

                if db_log:
                    # Logging
                    guild_id = str(payload.guild_id)
                    log_channel = await self.bot.pg_con.fetch("SELECT log_channel FROM config WHERE guild_id = $1", guild_id)
                    log = int(log_channel[0]['log_channel'])
                    channel = self.bot.get_channel(log)
                    embed=discord.Embed(title="⚠️ **Warning!**", description=f"**{user.name}#{user.discriminator}** has unreacted to a reaction role.", color=0xffff00)
                    embed.add_field(name="Message ID", value=db_msgid[0], inline=True)
                    embed.add_field(name="Emoji", value=db_emoji[0], inline=True)
                    embed.add_field(name="Role", value=db_role[0], inline=True)
                    await channel.send(embed=embed)

        except:
            return







def setup(bot):
    bot.add_cog(ReactionRoles(bot))
