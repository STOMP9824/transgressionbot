import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

class Client(discord.Client):
    async def on_ready(self):
        try:
            ## Syncs our guild object to discord
            ## Not doing so risks our slash command not showing.
            guild = discord.Object(id=1359269280151240746)
            synced = await tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('your turn'):
            await message.channel.send(f'Hello {message.author}! :D')
    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send('Oh! thanks for the reaction!\n{reaction.}')

class SubmitIncidentReport(discord.ui.Modal, title="Incident Report"):
    incident_title = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Title",
        required=True,
        placeholder="Provide incident report title"
    )
    incident_text = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label="report",
        required=True,
        max_length="500",
        placeholder="Describe the incident here"
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"{self.incident_title.value}",
                              description=f"{self.incident_text.value}",
                              color=discord.Color.green()
                              )
        embed.set_author(name=self.user.nick)
        await interaction.response.send_message(embed=embed, ephemeral=True)

## Stuff for initializing the bot

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)
tree = discord.app_commands.CommandTree(client)
load_dotenv()

GUILD_ID = discord.Object(id=1359269280151240746)

## Slash commands below

## When making slash-commands, you cannot use upper-case letters for the name parameter
@tree.command(name="hello_world", description="Says hello world back", guild=GUILD_ID)
async def sayHelloWorld(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello world, hello {interaction.user.name}")

@tree.command(name="repeat", description="Repeats whatever the user says", guild=GUILD_ID)
async def repeat(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

@tree.command(name="embed", description="Test embed", guild=GUILD_ID)
async def testEmbed(interaction: discord.Interaction):
    embed = discord.Embed(title="Test Title", description="Test Description")
    await interaction.response.send_message(embed=embed)

@tree.command(name="incident_report", description="submit an incident report to the Transgression Map project", guild=GUILD_ID)
async def incident(interaction: discord.Interaction):
    incident_modal = SubmitIncidentReport()
    incident_modal.user = interaction.user
    await interaction.response.send_modal(incident_modal)


try:
    TOKEN = os.getenv('TOKEN')
except Exception as e:
    print(f'Error locating token: {e}. Please make sure the .env file is located at the root of your project')
    quit()

client.run(TOKEN)