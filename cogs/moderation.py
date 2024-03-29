import nextcord
from nextcord.ext import commands
# Custom check function
def has_ban_permissions(ctx):
    return ctx.author.guild_permissions.ban_members

class MemberConverter(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            return await commands.MemberConverter().convert(ctx, argument)
        except commands.MemberNotFound:
            raise commands.BadArgument("Please specify a valid member to ban.")

class Moderation(commands.Cog, name="Moderation"):
    def __init__(self, bot):
        self.bot = bot

    async def send_error_embed(self, ctx, error_message):
        embed = nextcord.Embed(
            title="Error",
            description=error_message,
            color=nextcord.Colour.random()
        )
        await ctx.send(embed=embed)

    @commands.command(name="ban", description="Ban a member from the server.", usage=".ban [member] [reason]")
    @commands.check(has_ban_permissions)
    async def ban(self, ctx, member: MemberConverter = None, *, reason: str = "No reason provided"):
        # Check if the user has not specified any member
        if member is None:
            return await self.send_error_embed(ctx, "Please specify a valid member to ban.")

        # Check if the target is the command author
        if member == ctx.author:
            return await self.send_error_embed(ctx, "You cannot ban yourself.")

        # Check if the target is an administrator
        if member.guild_permissions.administrator:
            return await self.send_error_embed(ctx, "You cannot ban an administrator.")

        # Check if the bot's role is lower than the target's role
        if ctx.guild.me.top_role <= member.top_role:
            return await self.send_error_embed(ctx, "The bot's role must be higher than the target's role.")

        try:
            await member.ban(reason=reason)
            embed = nextcord.Embed(
                title="Member Banned",
                description=f"{member.mention} has been banned. Reason: {reason}",
                color=nextcord.Colour.random()
            )
            await ctx.send(embed=embed)
        except commands.BadArgument as e:
            # Catch the custom exception and send the error in an embed
            await self.send_error_embed(ctx, str(e))
        except nextcord.Forbidden:
            # This will be executed if the bot does not have permission to ban the member
            await self.send_error_embed(ctx, "The bot does not have permission to ban the member.")
        except nextcord.HTTPException:
            # This will be executed if an error occurs during the ban
            await self.send_error_embed(ctx, "An error occurred while banning the member.")


    @commands.command(name='unban', description="Unban a user from the server.", usage="unban [username/userid]")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, username):
        try:
            banned_users = ctx.guild.bans()
            

            async for ban_entry in banned_users:
                user = ban_entry.user
                if user.name.lower() == username.lower():
                    await ctx.guild.unban(user)
                    embed = nextcord.Embed(
                        title='Unban Successful',
                        description=f'Unbanned {user.name}',
                        color=nextcord.Colour.random()  # Set color to a random color
                    )
                    await ctx.send(embed=embed)
                    return

            embed = nextcord.Embed(
                title='Unban Error',
                description='User not found in ban list.',
                color=nextcord.Colour.random()  # Set color to a random color
            )
            await ctx.send(embed=embed)

        except nextcord.Forbidden:
            embed = nextcord.Embed(
                title='Unban Error',
                description='Bot does not have permission to unban members.',
                color=nextcord.Colour.random()  # Set color to a random color
            )
            await ctx.send(embed=embed)
        except nextcord.HTTPException:
            embed = nextcord.Embed(
                title='Unban Error',
                description='An error occurred while processing the unban request.',
                color=nextcord.Colour.random()  # Set color to a random color
            )
            await ctx.send(embed=embed)
      
    @commands.command(name='kick', description="Kick a member from the server.", usage="kick [member] [reason]")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: MemberConverter = None, *, reason: str = "No reason provided"):
        # Check if the user has not specified any member
        if member is None:
            return await self.send_error_embed(ctx, "Please specify a member to kick.")
        # Check if the target is the command author
        if member == ctx.author:
            return await self.send_error_embed(ctx, "You cannot kick yourself.")
        # Check if the target is an administrator
        if member.guild_permissions.administrator:
            return await self.send_error_embed(ctx, "You cannot kick an administrator.")
        # Check if the bot's role is lower than the target's role
        if ctx.guild.me.top_role <= member.top_role:
            return await self.send_error_embed(ctx, "The bot's role must be higher than the target's role.")
        try:
            await member.kick(reason=reason)
            embed = nextcord.Embed(
                title="Member Kicked",
                description=f"{member.mention} has been kicked. Reason: {reason}",
                color=nextcord.Colour.random()
            )
            await ctx.send(embed=embed)
        except commands.BadArgument as e:
            # Catch the custom exception and send the error in an embed
            await self.send_error_embed(ctx, str(e))
        except nextcord.Forbidden:
            # This will be executed if the bot does not have permission to kick the member
            await self.send_error_embed(ctx, "The bot does not have permission to kick the member.")
        except nextcord.HTTPException:
            # This will be executed if an error occurs during the kick
            await self.send_error_embed(ctx, "An error occurred while kicking the member.")

    @commands.command(name='lock', description="Lock a channel.", usage="lock [channel]")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: nextcord.TextChannel = None):
        channel = channel or ctx.channel
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            embed = nextcord.Embed(
                title="Channel Locked",
                description=f"{channel.mention} has been locked.",
                color=nextcord.Colour.random()
            )
            await ctx.send(embed=embed)
        except nextcord.Forbidden:
            await self.send_error_embed(ctx, "The bot does not have permission to lock the channel.")
        except nextcord.HTTPException:
            await self.send_error_embed(ctx, "An error occurred while locking the channel.")

    @commands.command(name='unlock', description="Unlock a channel.", usage="unlock [channel]")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: nextcord.TextChannel = None):
        channel = channel or ctx.channel
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            embed = nextcord.Embed(
                title="Channel Unlocked",
                description=f"{channel.mention} has been unlocked.",
                color=nextcord.Colour.random())
            await ctx.send(embed=embed)
        except nextcord.Forbidden:
            await self.send_error_embed(ctx, "The bot does not have permission to unlock the channel.")
        except nextcord.HTTPException:
            await self.send_error_embed(ctx, "An error occurred while unlocking the channel.")

    @commands.command(name='purge', description="Purge a specified number of messages.", usage="purge [amount]")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        try:
            await ctx.channel.purge(limit=amount + 1)
            embed = nextcord.Embed(
                title="Messages Purged",
                description=f"{amount} messages have been purged.",
                color=nextcord.Colour.random()
            )
            await ctx.send(embed=embed, delete_after=5)
        except nextcord.Forbidden:
            await self.send_error_embed(ctx, "The bot does not have permission to purge messages.")
        except nextcord.HTTPException:
            await self.send_error_embed(ctx, "An error occurred while purging the messages")
    @commands.command(name ="avatarurl", description="Get the avatar url for a member", usage="avatar url <member>")
    async def avatarurl(self, ctx, member: nextcord.Member = None):
        member = member or ctx.author
        embed = nextcord.Embed(
            title=f"{member.name}'s AvatarUrl",description=f"[Click here to download]({member.avatar.url})", color=nextcord.Colour.random())
            
        await ctx.send(embed=embed)  
    @commands.command(name="vote",description="Vote for the server on top.gg", usage=".vote")
    async def vote(self, ctx):
        embed = nextcord.Embed(
            title="Vote for the server",
            description="Vote for the server on top.gg",
            color=nextcord.Colour.random()
        )
        embed.add_field(name="Link", value="[Click here to vote](https://top.gg/servers/1196104116703866991)", inline=False)
        await ctx.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 1200154683721928805:
            if not message.attachments:  # Check if the message has no attachments
                await message.delete()
            else:
                # Assuming correct emoji IDs, replace them with the actual IDs
                await message.add_reaction("<:emoji_47:1200357003567042590>")
                await message.add_reaction("<:emoji_47:1200357030205067354>")           
            
def setup(bot):
    bot.add_cog(Moderation(bot))
