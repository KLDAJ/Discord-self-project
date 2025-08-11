import discord
from discord import app_commands
from discord.ext import commands
import json
import os

# Default settings for new servers
DEFAULT_SETTINGS = {
    "welcome_channel_id": None,
    "goodbye_channel_id": None,
    "welcome_message": "Welcome, {mention}! 🎉",  # Default welcome message
    "goodbye_message": "Goodbye, {name}. We'll miss you! 👋",  # Default goodbye message
    "welcome_image_url": "https://example.com/welcome_image.png",  # Default welcome image URL
    "goodbye_image_url": "https://example.com/goodbye_image.png",  # Default goodbye image URL
    "welcome_color": "00FF00",  # Default welcome color (green)
    "goodbye_color": "FF0000"  # Default goodbye color (red)
}

# Load or create the config file
if os.path.exists("config.json"):
    with open("config.json", "r") as f:
        config = json.load(f)
else:
    config = {}

# Save the config file
def save_config():
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

# Function to get server-specific settings
def get_server_config(guild_id):
    if str(guild_id) not in config:
        # Initialize default settings for new servers
        config[str(guild_id)] = DEFAULT_SETTINGS.copy()
        save_config()
    return config[str(guild_id)]

# Function to convert hex color code to integer
def hex_to_int(hex_code):
    return int(hex_code.lstrip("#"), 16)

# Replace with your bot's token
TOKEN = "MTM0NjE4ODE3ODIxMzU3MjY1OA.Gw9hqL.1kP9hOEUax4xftkkUEkD24fYUv128c4nvi0dQE"

# Set up the bot with intents
intents = discord.Intents.default()
intents.members = True  # Enable the members intent
intents.message_content = True  # Enable the message content intent
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")
    try:
        # Sync slash commands with Discord
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Event: When the bot joins a new server
@bot.event
async def on_guild_join(guild):
    # Initialize default settings for the new server
    get_server_config(guild.id)
    print(f"Joined new server: {guild.name}. Default settings initialized.")

# Event: When a new member joins
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
            # Create an embed for the welcome message
            embed = discord.Embed(
                title="Welcome!",
                description=welcome_message.format(mention=member.mention),
                color=welcome_color  # Custom welcome color
            )
            embed.set_thumbnail(url=member.avatar.url)  # Add the member's avatar
            embed.set_image(url=welcome_image_url)  # Add the welcome image
            await channel.send(embed=embed)

# Event: When a member leaves
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
            # Create an embed for the goodbye message
            embed = discord.Embed(
                title="Goodbye!",
                description=goodbye_message.format(name=member.name),
                color=goodbye_color  # Custom goodbye color
            )
            embed.set_thumbnail(url=member.avatar.url)  # Add the member's avatar
            embed.set_image(url=goodbye_image_url)  # Add the goodbye image
            await channel.send(embed=embed)

# Slash Command: Set the welcome channel
@bot.tree.command(name="set_welcome_channel", description="Set the channel for welcome messages.")
@app_commands.checks.has_permissions(administrator=True)
async def set_welcome_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    guild_id = interaction.guild.id
    server_config = get_server_config(guild_id)
    server_config["welcome_channel_id"] = channel.id
    save_config()
    await interaction.response.send_message(f"Welcome messages will now be sent in {channel.mention}.")

# Slash Command: Set the goodbye channel
@bot.tree.command(name="set_goodbye_channel", description="Set the channel for goodbye messages.")
@app_commands.checks.has_permissions(administrator=True)
async def set_goodbye_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    guild_id = interaction.guild.id
    server_config = get_server_config(guild_id)
    server_config["goodbye_channel_id"] = channel.id
    save_config()
    await interaction.response.send_message(f"Goodbye messages will now be sent in {channel.mention}.")

# Slash Command: Set the welcome message
@bot.tree.command(name="set_welcome_message", description="Set the custom welcome message.")
@app_commands.checks.has_permissions(administrator=True)
async def set_welcome_message(interaction: discord.Interaction, message: str):
    guild_id = interaction.guild.id
    server_config = get_server_config(guild_id)
    server_config["welcome_message"] = message
    save_config()
    await interaction.response.send_message(f"Welcome message set to: `{message}`")

# Slash Command: Set the goodbye message
@bot.tree.command(name="set_goodbye_message", description="Set the custom goodbye message.")
@app_commands.checks.has_permissions(administrator=True)
async def set_goodbye_message(interaction: discord.Interaction, message: str):
    guild_id = interaction.guild.id
    server_config = get_server_config(guild_id)
    server_config["goodbye_message"] = message
    save_config()
    await interaction.response.send_message(f"Goodbye message set to: `{message}`")

# Slash Command: Set the welcome image URL
@bot.tree.command(name="set_welcome_image", description="Set the custom welcome image URL.")
@app_commands.checks.has_permissions(administrator=True)
async def set_welcome_image(interaction: discord.Interaction, image_url: str):
    guild_id = interaction.guild.id
    server_config = get_server_config(guild_id)
    server_config["welcome_image_url"] = image_url
    save_config()
    await interaction.response.send_message(f"Welcome image URL set to: `{image_url}`")

# Slash Command: Set the goodbye image URL
@bot.tree.command(name="set_goodbye_image", description="Set the custom goodbye image URL.")
@app_commands.checks.has_permissions(administrator=True)
async def set_goodbye_image(interaction: discord.Interaction, image_url: str):
    guild_id = interaction.guild.id
    server_config = get_server_config(guild_id)
    server_config["goodbye_image_url"] = image_url
    save_config()
    await interaction.response.send_message(f"Goodbye image URL set to: `{image_url}`")

# Slash Command: Set the welcome embed color
@bot.tree.command(name="set_welcome_color", description="Set the custom welcome embed color (hex code).")
@app_commands.checks.has_permissions(administrator=True)
async def set_welcome_color(interaction: discord.Interaction, hex_code: str):
    if not hex_code.startswith("#"):
        hex_code = f"#{hex_code}"
    try:
        # Validate the hex code
        int(hex_code.lstrip("#"), 16)
        guild_id = interaction.guild.id
        server_config = get_server_config(guild_id)
        server_config["welcome_color"] = hex_code.lstrip("#")
        save_config()
        await interaction.response.send_message(f"Welcome embed color set to: `{hex_code}`")
    except ValueError:
        await interaction.response.send_message("Invalid hex code! Please provide a valid hex color code (e.g., `#00FF00`).", ephemeral=True)

# Slash Command: Set the goodbye embed color
@bot.tree.command(name="set_goodbye_color", description="Set the custom goodbye embed color (hex code).")
@app_commands.checks.has_permissions(administrator=True)
async def set_goodbye_color(interaction: discord.Interaction, hex_code: str):
    if not hex_code.startswith("#"):
        hex_code = f"#{hex_code}"
    try:
        # Validate the hex code
        int(hex_code.lstrip("#"), 16)
        guild_id = interaction.guild.id
        server_config = get_server_config(guild_id)
        server_config["goodbye_color"] = hex_code.lstrip("#")
        save_config()
        await interaction.response.send_message(f"Goodbye embed color set to: `{hex_code}`")
    except ValueError:
        await interaction.response.send_message("Invalid hex code! Please provide a valid hex color code (e.g., `#FF0000`).", ephemeral=True)

# Slash Command: Preview the welcome message
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
            # Create an embed for the welcome message preview
            embed = discord.Embed(
                title="Welcome!",
                description=welcome_message.format(mention=interaction.user.mention),
                color=welcome_color  # Custom welcome color
            )
            embed.set_thumbnail(url=interaction.user.avatar.url)  # Add the user's avatar
            embed.set_image(url=welcome_image_url)  # Add the welcome image
            await channel.send(embed=embed)
            await interaction.response.send_message("Welcome message preview sent!", ephemeral=True)
        else:
            await interaction.response.send_message("Welcome channel not found!", ephemeral=True)
    else:
        await interaction.response.send_message("Welcome channel not set!", ephemeral=True)

# Slash Command: Preview the goodbye message
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
            # Create an embed for the goodbye message preview
            embed = discord.Embed(
                title="Goodbye!",
                description=goodbye_message.format(name=interaction.user.name),
                color=goodbye_color  # Custom goodbye color
            )
            embed.set_thumbnail(url=interaction.user.avatar.url)  # Add the user's avatar
            embed.set_image(url=goodbye_image_url)  # Add the goodbye image
            await channel.send(embed=embed)
            await interaction.response.send_message("Goodbye message preview sent!", ephemeral=True)
        else:
            await interaction.response.send_message("Goodbye channel not found!", ephemeral=True)
    else:
        await interaction.response.send_message("Goodbye channel not set!", ephemeral=True)

# Run the bot
bot.run(TOKEN)
    
