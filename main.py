import nextcord
from nextcord.ext import commands
import os
from keep_alive import keep_alive
from nextcord import SlashOption, TextChannel
from typing import Optional
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
 
@bot.event 
async def on_message(message):
    if bot.user.mention in message.content:
        await message.reply("Hello Pookie")
    await bot.process_commands(message)

class buttons(nextcord.ui.View):

    def __init__(self):
        super().__init__()
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
        super().__init__()
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
    webhook_url=webhook.url
    if ctx.user.guild_permissions.administrator and ctx.user != None:


        embed=nextcord.Embed(description=f"Press the button below to create a Ticket!")
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
        await ctx.send(embed=embed)
    else:
        embed = nextcord.Embed(title=f"You don't have the permissions for this!")
        await ctx.send(embed=embed, ephemeral=True)

@bot.slash_command(name="sendwebhook", description="Send an embed message using webhook")
async def sendwebhook(
    ctx: nextcord.Interaction,
    id: str = SlashOption(required=True),
    title: str = SlashOption(required=True),
    description: str = SlashOption(required=True),
    color: str = SlashOption(required=True),
    username: str = SlashOption(required=False),
    avatarurl: str = SlashOption(required=False),
    icon: str = SlashOption(required=False),
    thumbnail_icon: str = SlashOption(required=False),
    image: str = SlashOption(required=False),
    footer_text: str = SlashOption(required=False)
):
    if ctx.user.guild_permissions.administrator and ctx.user != None:
        webhook = await bot.fetch_webhook(id)
        
        # Create the initial embed with username, avatar_url, and specified color
        embed = nextcord.Embed(
            title=title,
            description=description,
            color=nextcord.Colour(int(color, 16))  # Convert hex color to integer
        )
        embed.set_thumbnail(url=thumbnail_icon)
        embed.set_image(url=image)
        embed.set_footer(text=footer_text, icon_url=icon)
        await webhook.send(embed=embed, username=username, avatar_url=avatarurl)

        # Create subsequent embeds without specifying username, avatar_url, and color
        for _ in range(5):  # You can adjust the range as needed
            embed = nextcord.Embed(
                title=title,
                description=description,
                color=nextcord.Colour(int(color, 16))  # Convert hex color to integer
            )
            embed.set_thumbnail(url=thumbnail_icon)
            embed.set_image(url=image)
            embed.set_footer(text=footer_text, icon_url=icon)
            await webhook.send(embed=embed)

        await ctx.send("Embeds created with webhook.")
    else:
        await ctx.send("You don't have the required permissions.")




bot.run(token)
