import nextcord
from nextcord.ext import commands
from nextcord.ext import application_checks
import os
from keep_alive import keep_alive
from nextcord import SlashOption, TextChannel
from typing import Optional
import colour
import datetime
from nextcord.ui import button
keep_alive()
bot = commands.Bot(command_prefix=".", intents=nextcord.Intents.all())
bot.remove_command("help")

token = os.environ['TOKEN']
cogs = ["cogs.basic","cogs.Snipe","cogs.help","cogs.moderation","cogs.WelcomeCog"]  # Modify the cogs list to include the correct path to the basic.commands file

@bot.event
async def on_ready():
    print("The bot is ready!")
    print("Loading cogs . . .")
    for cog in cogs:
        try:
            bot.load_extension(cog)
            print(cog + " was loaded.")
        except Exception as e:
            print(e)

    bot.add_view(butts())
    bot.add_view(buttons())
 
@bot.event 
async def on_message(message):
    if bot.user.mention in message.content:
        await message.reply("Hello Pookie")
    await bot.process_commands(message)

class buttons(nextcord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Ticket Support", style=nextcord.ButtonStyle.green, emoji="📧")
    async def teste3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True),
            interaction.user: nextcord.PermissionOverwrite(read_messages=True)
        }
        channek = await interaction.guild.create_text_channel(f"Ticket-", overwrites=overwrites)
        id = channek.id
        embed = nextcord.Embed(title="Ticket Support", description=f"Thank you for requesting help.\nState your problems or questions here and await a response.")
        await channek.send(embed=embed, view=butts())
        await interaction.send(f"Ticket created <#{id}>..", ephemeral=True)

class butts(nextcord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Close Ticket", style=nextcord.ButtonStyle.red, emoji="📧")
    async def teste(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.channel.delete()

    @nextcord.ui.button(label="Claim Ticket", style=nextcord.ButtonStyle.green, emoji="📧")
    async def teste2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.guild_permissions.administrator and interaction.user != None:
            embed = nextcord.Embed(title=f"Claimed Ticket", description=f"Your ticket will be handled by {interaction.user.mention}.")
            await interaction.send(embed=embed)
            interaction = await bot.wait_for("button_click", check=lambda inter: inter.custom_id == "teste2")

            async def button_callback(button_inter: nextcord.Interaction):
                butts.disabled = True
            butts.callback = button_callback
        else:
            embed = nextcord.Embed(title=f"You don't have the permissions for this!")
            await interaction.send(embed=embed, ephemeral=True)

@bot.slash_command(name="ticket", description="Setup the ticket system!")
async def ticket(ctx: nextcord.Interaction):
    if ctx.user.guild_permissions.administrator and ctx.user != None:


        embed=nextcord.Embed(description=f"Press the button below to create a Ticket!")
        await ctx.response.send_message("Ticket System Created", ephemeral=True)
        await ctx.send(embed=embed, view=buttons())
    else:
        embed = nextcord.Embed(title=f"You don't have the permissions for this!")
        await ctx.send(embed=embed, ephemeral=True)
@bot.slash_command(name="webhook", description="Create a webhook")
async def webhook(ctx: nextcord.Interaction, channel: nextcord.TextChannel, name: str):
    if ctx.user.guild_permissions.administrator and ctx.user is not None:
        if name is None:
            webhook = await channel.create_webhook(name="Webhook")
            embed = nextcord.Embed(title="Webhook created", description="A webhook has been created", color=nextcord.Colour.random())

            # Send a message using the webhook with the embed
            await webhook.send(embed=embed, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url)

            await ctx.send(f"Webhook created in {channel.mention} id=```{webhook.id}```")

            # Send a message using the webhook with the embed
            await webhook.send(embed=embed, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url)

            await ctx.send(f"Webhook created in {channel.mention} id=```{webhook.url}```")
        elif channel is None:
            webhook = await channel.create_webhook(name="Webhook")
            embed = nextcord.Embed(title="Webhook created", description="A webhook has been created", color=nextcord.Colour.random())

            # Send a message using the webhook with the embed
            await webhook.send(embed=embed, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url)

            await ctx.send(f"Webhook created in {channel.mention}., id=```{webhook.id}```")

            # Send a message using the webhook with the embed
            await webhook.send(embed=embed, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url)

            await ctx.send(f"Webhook created in {channel.mention} id=```{webhook.id}```.")
        else:
            webhook = await channel.create_webhook(name=name)
            embed = nextcord.Embed(title="Webhook created", description=f"A webhook has been created in {channel.mention}", color=nextcord.Colour.random())

            # Send a message using the webhook with the embed
            await webhook.send(embed=embed, username=ctx.user.display_name, avatar_url=ctx.user.avatar.url)

            await ctx.send(f"Webhook created in {channel.mention}. id=```{webhook.id}```")


@bot.slash_command(name="embed", description="Create An embed")
async def embed(ctx: nextcord.Interaction,title:str=SlashOption(required=True), description:str=SlashOption(required=True), color:str=SlashOption(required=True)):
    if ctx.user.guild_permissions.administrator and ctx.user != None:
        embed = nextcord.Embed(title=title, description=description, color=nextcord.Colour.random())
        await ctx.send("Embed Created", ephemeral=True)
        await ctx.send(embed=embed)
    else:
        embed = nextcord.Embed(title=f"You don't have the permissions for this!")
        await ctx.send(embed=embed, ephemeral=True)

@bot.slash_command(name="sendwebhook", description="Send an embed message using webhook")
async def sendwebhook(
    ctx: nextcord.Interaction,
    id: str = SlashOption(required=True),
    color: str = SlashOption(required=True),
    description: str = SlashOption(required=False),
    title: str = SlashOption(required=False),
    username: str = SlashOption(required=False),
    avatarurl: str = SlashOption(required=False),
    icon: str = SlashOption(required=False),
    thumbnail_icon: str = SlashOption(required=False),
    image: str = SlashOption(required=False),
    footer_text: str = SlashOption(required=False),
    send_subsequent: bool = SlashOption(required=False, default=False)
):
    if ctx.user.guild_permissions.administrator and ctx.user != None:
        webhook = await bot.fetch_webhook(id)

        try:
            # Try to convert color to RGB using the colour library
            color_rgb = colour.Color(color).rgb
            color_value = int(color_rgb[0] * 255) << 16 | int(color_rgb[1] * 255) << 8 | int(color_rgb[2] * 255)
        except ValueError:
            # Handle invalid color input, set a default color, or raise an error
            color_value = 0x7289DA  # Discord blue as a default color

        if username and avatarurl:
            # Create the initial embed with username, avatar_url, and specified color
            embed = nextcord.Embed(
                title=title,
                description=description,
                color=nextcord.Colour(color_value)
            )
            embed.set_thumbnail(url=thumbnail_icon)
            embed.set_image(url=image)
            embed.set_footer(text=footer_text, icon_url=icon)

            # Send the initial embed with username and avatar_url
            await webhook.send(embed=embed, username=username, avatar_url=avatarurl)

        # Optionally send subsequent embeds without specifying username and avatar_url
        elif send_subsequent:
            for _ in range(1):  # Adjust the range as needed
                embed = nextcord.Embed(
                    title=title,
                    description=description,
                    color=nextcord.Colour(color_value)
                )
                embed.set_thumbnail(url=thumbnail_icon)
                embed.set_image(url=image)
                embed.set_footer(text=footer_text, icon_url=icon)
                await webhook.send(embed=embed)

            await ctx.send("Embeds created with webhook.")
        else:
            await ctx.send("Initial embed created with webhook.")
    else:
        await ctx.send("You don't have the required permissions.")

@bot.slash_command(name='timeout', description='timeouts a user for a specific time')
@application_checks.has_permissions(moderate_members=True)
async def timeout(ctx: nextcord.Interaction, member: nextcord.Member, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0, reason: str = None):
    duration = datetime.timedelta(seconds=seconds, minutes=minutes, hours= hours, days=days)
    await member.timeout(duration, reason=reason)

    await ctx.response.send_message(f'{member.mention} was timeouted until for {duration}')
@bot.slash_command(name='untimeout', description='Untimeouts a user')
@application_checks.has_permissions(moderate_members=True)
async def untimeout(ctx: nextcord.Interaction, member: nextcord.Member):
    await member.timeout(None)
    await ctx.send(f"{member.mention} was untimed out")
@bot.command()
async def verify(ctx):
    # Create a view with the "Verify" button
    view = VerifyButton()
    
    # Send a message with the button
    await ctx.send("Click the button below to verify:", view=view)

# Custom button to handle verification
class VerifyButton(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Verify", style=nextcord.ButtonStyle.green)
    async def verify_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        member = interaction.user
        guild = interaction.guild

        # Get the "Member" and "Quarantine" roles
        member_role = nextcord.utils.get(guild.roles, name="୧・M E M B E R S・୨")
        quarantine_role = nextcord.utils.get(guild.roles, name="Quarantine")

        if member_role and quarantine_role:
            # Add the "Member" role and remove the "Quarantine" role
            await member.add_roles(member_role)
            await member.remove_roles(quarantine_role)
            await interaction.response.send_message("You have been verified!", ephemeral=True)
        else:
            await interaction.response.send_message("Roles not found. Please contact an administrator.")

bot.run(token)
