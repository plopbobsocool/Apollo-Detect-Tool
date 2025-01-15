import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

# Create an instance of the bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}! Bot is ready.")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="detect", description="Compare server members to a list of names in a message.")
async def detect(interaction: discord.Interaction, message_link: str):
    try:
        # Parse the message link
        link_parts = message_link.split('/')
        if len(link_parts) < 3:
            await interaction.response.send_message("Invalid message link format.", ephemeral=True)
            return

        guild_id = int(link_parts[-3])
        channel_id = int(link_parts[-2])
        message_id = int(link_parts[-1])

        # Fetch the message
        guild = bot.get_guild(guild_id)
        if not guild:
            await interaction.response.send_message("Bot is not in the specified guild.", ephemeral=True)
            return

        channel = guild.get_channel(channel_id)
        if not channel:
            await interaction.response.send_message("Channel not found.", ephemeral=True)
            return

        message = await channel.fetch_message(message_id)
        name_list = message.content.splitlines()

        # Normalize names from the list
        normalized_names = [name.strip().lower() for name in name_list]

        # Get server members
        all_members = guild.members

        # Find members not in the name list
        missing_members = [
            member.display_name
            for member in all_members
            if member.display_name.lower() not in normalized_names
        ]

        # Respond with the results
        if missing_members:
            response = "The following members are not in the provided list:\n" + "\n".join(missing_members)
        else:
            response = "All server members are accounted for in the list!"

        await interaction.response.send_message(response)

    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

# Run the bot
TOKEN = "YOUR_BOT_TOKEN"
bot.run(TOKEN)
