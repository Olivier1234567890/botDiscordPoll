import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()


@bot.event
async def on_ready():
    print("coucou")
    await bot.tree.sync()


@bot.command(name='del')
async def dele(ctx, number_of_messages: int):
    messages = [message async for message in ctx.channel.history(limit=number_of_messages + 1)]
    for m in messages:
        await m.delete()


@bot.tree.command(name='sondage', description='sondageAPE')
async def slash(interaction: discord.Interaction, question: str, reponse1: str, reponse2: str, reponse3: str | None = '', reponse4: str | None = '', reponse5: str | None=''):
    # Initialisation des liste de réactions et de réponses
    reactions = ['🇦', '🇧', '🇨', '🇩', '🇪']
    reponses = [reponse1, reponse2]
    if reponse3 != '': reponses.append(reponse3)
    if reponse4 != '': reponses.append(reponse4)
    if reponse5 != '': reponses.append(reponse5)

    # Association de chaque réaction avec sa réponse
    propositions = []
    for i in range(len(reponses)):
        propositions.append(reactions[i] + ' ' + reponses[i])

    # creation du sondage dans un embed
    embed = discord.Embed(colour=0xEB459F,title=question, description='@everyone\n'+'\n'.join(propositions))
    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()

    # ajout des récations sous le message
    for reaction in reactions[:len(reponses)]:
        await msg.add_reaction(reaction)

bot.run(os.getenv("TOKEN"))
