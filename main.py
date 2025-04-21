import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

class Client(discord.Client):
    async def on_ready(self):
        try:
            token = os.getenv('TOKEN')
            print(f'TOKEN: {token}')
        except Exception as e:
            print(f'Error locating token: {e}')

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

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)
tree = discord.app_commands.CommandTree(client)
load_dotenv()

GUILD_ID = discord.Object(id=1359269280151240746)

## When making slash-commands, you cannot use upper-case letters for the name parameter
@tree.command(name="hello_world", description="Says hello world back", guild=GUILD_ID)
async def sayHelloWorld(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World")

@tree.command(name="repeat", description="Repeats whatever the user says", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

TOKEN = os.getenv('TOKEN')
client.run(TOKEN)