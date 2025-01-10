import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    await bot.tree.sync()

@bot.tree.command(name="detect", description="Find members who haven't reacted to a specific message.")
async def detect(interaction: discord.Interaction, message_id: str):
    await interaction.response.defer()  # Acknowledge the command

    try:
        channel = interaction.channel
        message = await channel.fetch_message(int(message_id))
    except Exception as e:
        await interaction.followup.send(f"Could not find the message: {e}")
        return

    if not message.reactions:
        await interaction.followup.send("This message has no reactions.")
        return

    # Get all members in the server
    guild_members = set(interaction.guild.members)

    # Get all members who reacted
    reacted_members = set()
    for reaction in message.reactions:
        async for user in reaction.users():
            reacted_members.add(user)

    # Find members who haven't reacted
    non_reacted_members = guild_members - reacted_members
    non_reacted_names = [member.display_name for member in non_reacted_members]

    # Build and send the result
    if non_reacted_names:
        await interaction.followup.send(
            "Members who haven't reacted:\n" + "\n".join(non_reacted_names)
        )
    else:
        await interaction.followup.send("Everyone has reacted to the message!")

bot.run("YOUR_BOT_TOKEN")
