import os

import discord
from dotenv import load_dotenv

import base64

data_uri = base64.b64encode(open("test.png", "rb").read()).decode("utf-8")
img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_voice_state_update(member, before, after):
    if member:
        print()

        if member.voice.deaf:
            async for entry in member.guild.audit_logs(limit=1):
                if entry.user == member:
                    return
                else:
                    for channel in member.guild.channels:
                        if channel.name == "general":
                            await channel.send(
                                f"{member.name} was deafened by {entry.user.name}"
                            )


client.run(TOKEN)
