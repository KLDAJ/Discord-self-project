import discord
from discord import app_commands
from discord.ext import commands
import json
import os

DEFAULT_SETTINGS = {
    "welcome_channel_id": None,
    "goodbye_channel_id": None,
    "welcome_message": "Welcome, {mention}! 🎉",
    "goodbye_message": "Goodbye, {name}. We'll miss you! 👋",
    "welcome_image_url": "https://example.com/welcome_image.png",
    "goodbye_image_url": "https://example.com/goodbye_image.png",
    "welcome_color": "00FF00",
    "goodbye_color": "FF0000"
}

if os.path.exists("config.json"):
    with open("config.json", "r") as f:
        config = json.load(f)
else:
    config = {}

def save_config():
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

def get_server_config(guild_id):
    if str(guild_id) not in config:
        config[str(guild_id)] = DEFAULT_SETTINGS.copy()
        save_config()
    return config[str(guild_id)]

def hex_to_int(hex_code):
    return int(hex_code.lstrip("#"), 16)

TOKEN = ""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.event
async def on_guild_join(guild):
    get_server_config(guild.id)
    print(f"Joined new server: {guild.name}. Default settings initialized.")

@bot.event
async def on_member_join(member):
    guild_id = member.guild.id
    server_config = get_server_config(guild_id)
    welcome_channel_id = server_config.get("welcome_channel_id")
    if welcome_channel_id:
        channel = bot.get_channel(welcome_channel_id)
        if channel:
            welcome_message = server_config.get("welcome_message", "Welcome, {mention}! 🎉")
            welcome_image_url = server_config.get("welcome_image_url", "https://example.com/welcome_image.png")
            welcome_color = hex_to_int(server_config.get("welcome_color", "00FF00"))
            embed = discord.Embed(
                title="Welcome!",
                description=welcome_message.format(mention=member.mention),
                color=welcome_color
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_image(url=welcome_image_url)
            await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    guild_id = member.guild.id
    server_config = get_server_config(guild_id)
    goodbye_channel_id = server_config.get("goodbye_channel_id")
    if goodbye_channel_id:
        channel = bot.get_channel(goodbye_channel_id)
        if channel:
            goodbye_message = server_config.get("goodbye_message", "Goodbye, {name}. We'll miss you! 👋")
            goodbye_image_url = server_config.get("goodbye_image_url", "https://example.com/goodbye_image.png")
            goodbye_color = hex_to_int(server_config.get("goodbye_color", "FF0000"))
            embed = discord.Embed(
                title="Goodbye!",
                description=goodbye_message.format(name=member.name),
                color=goodbye_color
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_image(url=goodbye_image_url)
            await channel.send(embed=embed)

@bot.tree.command(name="set_welcome_channel", description="Set the channel for welcome messages.")
@app_commands.checks.has_permissions(administrator=True)
async def set_welcome_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    guild_id = interaction.guild.id
    server_config = get_server_config(guild_id)
    server_config["welcome_channel_id"] = channel.id
    save_config()
    await interaction.response.send_message(f"Welcome messages will now be sent in {channel.mention}.")

@bot.tree.command(name="set_goodbye_channel", description="Set the channel for goodbye messages.")
@app_commands.checks.has_permissions(administrator=True)
async def set_goodbye_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    guild_id = interaction.guild.id
    server_config = get_server_config(guild_id)
    server_config["goodbye_channel_id"] = channel.id
    save_config()
    await interaction.response.send_message(f"Goodbye messages will now be sent in {channel.mention}.")

@bot.tree.command(name="set_welcome_message", description="Set the custom welcome message.")
@app_commands.checks.has_permissions(administrator=True)
async def set_welcome_message(interaction: discord.Interaction, message: str):
    guild_id = interaction.guild.id
    server_config = get_server_config(guild_id)
    server_config["welcome_message"] = message
    save_config()
    await interaction.response.send_message(f"Welcome message set to: `{message}`")

@bot.tree.command(name="set_goodbye_message", description="Set the custom goodbye message.")
@app_commands.checks.has_permissions(administrator=True)
async def set_goodbye_message(interaction: discord.Interaction, message: str):
    guild_id = interaction.guild.id
    server_config = get_server_config(guild_id)
    server_config["goodbye_message"] = message
    save_config()
    await interaction.response.send_message(f"Goodbye message set to: `{message}`")

@bot.tree.command(name="set_welcome_image", description="Set the custom welcome image URL.")
@app_commands.checks.has_permissions(administrator=True)
async def set_welcome_image(interaction: discord.Interaction, image_url: str):
    guild_id = interaction.guild.id
    server_config = get_server_config(guild_id)
    server_config["welcome_image_url"] = image_url
    save_config()
    await interaction.response.send_message(f"Welcome image URL set to: `{image_url}`")

@bot.tree.command(name="set_goodbye_image", description="Set the custom goodbye image URL.")
@app_commands.checks.has_permissions(administrator=True)
async def set_goodbye_image(interaction: discord.Interaction, image_url: str):
    guild_id = interaction.guild.id
    server_config = get_server_config(guild_id)
    server_config["goodbye_image_url"] = image_url
    save_config()
    await interaction.response.send_message(f"Goodbye image URL set to: `{image_url}`")

@bot.tree.command(name="set_welcome_color", description="Set the custom welcome embed color (hex code).")
@app_commands.checks.has_permissions(administrator=True)
async def set_welcome_color(interaction: discord.Interaction, hex_code: str):
    if not hex_code.startswith("#"):
        hex_code = f"#{hex_code}"
    try:
        int(hex_code.lstrip("#"), 16)
        guild_id = interaction.guild.id
        server_config = get_server_config(guild_id)
        server_config["welcome_color"] = hex_code.lstrip("#")
        save_config()
        await interaction.response.send_message(f"Welcome embed color set to: `{hex_code}`")
    except ValueError:
        await interaction.response.send_message("Invalid hex code! Please provide a valid hex color code (e.g., `#00FF00`).", ephemeral=True)

@bot.tree.command(name="set_goodbye_color", description="Set the custom goodbye embed color (hex code).")
@app_commands.checks.has_permissions(administrator=True)
async def set_goodbye_color(interaction: discord.Interaction, hex_code: str):
    if not hex_code.startswith("#"):
        hex_code = f"#{hex_code}"
    try:
        int(hex_code.lstrip("#"), 16)
        guild_id = interaction.guild.id
        server_config = get_server_config(guild_id)
        server_config["goodbye_color"] = hex_code.lstrip("#")
        save_config()
        await interaction.response.send_message(f"Goodbye embed color set to: `{hex_code}`")
    except ValueError:
        await interaction.response.send_message("Invalid hex code! Please provide a valid hex color code (e.g., `#FF0000`).", ephemeral=True)

@bot.tree.command(name="test_greet", description="Preview the welcome message.")
@app_commands.checks.has_permissions(administrator=True)
async def test_greet(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    server_config = get_server_config(guild_id)
    welcome_channel_id = server_config.get("welcome_channel_id")
    if welcome_channel_id:
        channel = bot.get_channel(welcome_channel_id)
        if channel:
            welcome_message = server_config.get("welcome_message", "Welcome, {mention}! 🎉")
            welcome_image_url = server_config.get("welcome_image_url", "https://example.com/welcome_image.png")
            welcome_color = hex_to_int(server_config.get("welcome_color", "00FF00"))
            embed = discord.Embed(
                title="Welcome!",
                description=welcome_message.format(mention=interaction.user.mention),
                color=welcome_color
            )
            embed.set_thumbnail(url=interaction.user.avatar.url)
            embed.set_image(url=welcome_image_url)
            await channel.send(embed=embed)
            await interaction.response.send_message("Welcome message preview sent!", ephemeral=True)
        else:
            await interaction.response.send_message("Welcome channel not found!", ephemeral=True)
    else:
        await interaction.response.send_message("Welcome channel not set!", ephemeral=True)

@bot.tree.command(name="test_goodbye", description="Preview the goodbye message.")
@app_commands.checks.has_permissions(administrator=True)
async def test_goodbye(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    server_config = get_server_config(guild_id)
    goodbye_channel_id = server_config.get("goodbye_channel_id")
    if goodbye_channel_id:
        channel = bot.get_channel(goodbye_channel_id)
        if channel:
            goodbye_message = server_config.get("goodbye_message", "Goodbye, {name}. We'll miss you! 👋")
            goodbye_image_url = server_config.get("goodbye_image_url", "https://example.com/goodbye_image.png")
            goodbye_color = hex_to_int(server_config.get("goodbye_color", "FF0000"))
            embed = discord.Embed(
                title="Goodbye!",
                description=goodbye_message.format(name=interaction.user.name),
                color=goodbye_color
            )
            embed.set_thumbnail(url=interaction.user.avatar.url)
            embed.set_image(url=goodbye_image_url)
            await channel.send(embed=embed)
            await interaction.response.send_message("Goodbye message preview sent!", ephemeral=True)
        else:
            await interaction.response.send_message("Goodbye channel not found!", ephemeral=True)
    else:
        await interaction.response.send_message("Goodbye channel not set!", ephemeral=True)

bot.run(TOKEN)
