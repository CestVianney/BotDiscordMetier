import discord
import db.usersmetiersDb as db
import commands.ajoutermetier as ajoutermetier 
import commands.recherchermetier as recherchermetier
import commands.ajouterpassagedonjon as ajouterpassagedonjon
import commands.supprimerpassagedonjon as supprimerpassagedonjon
import commands.rechercherpassagedonjon as rechercherpassagedonjon
from discord.ext import commands
from dotenv import load_dotenv
from utils.donjons import options

import os

load_dotenv()
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {synced} commands")
    except Exception as e:
        print(f"An error occurred: {e}")

@bot.tree.command(name="ajouter-metiers", description="Ajoute les niveaux pour chaque métier")
async def ajouterMetiers(interaction: discord.Interaction):
    metiersFromDb = db.get_data_from_user(interaction.user.name)
    metiers = [
        ('Alchimiste', 0), ('Bijoutier', 0), ('Bricoleur', 0), ('Bucheron', 0), ('Chasseur', 0), 
        ('Cordomage', 0), ('Cordonnier', 0), ('Costumage', 0), ('Facomage', 0), ('Faconneur', 0), 
        ('Forgeron', 0), ('Forgemage', 0), ('Joaillomage', 0), ('Mineur', 0), ('Paysan', 0), 
        ('Pecheur', 0), ('Sculpteur', 0), ('Sculptemage', 0), ('Tailleur', 0)
    ]
    for i, (metier, _) in enumerate(metiers):
        for metierFromDb, niveau in metiersFromDb:
            if metier == metierFromDb:
                metiers[i] = (metier, niveau)
                break
    user = interaction.user
    view = ajoutermetier.MetierNiveauView(metiers, ajoutermetier.save_niveau, user)
    await interaction.response.send_message('Veuillez choisir un métier pour renseigner son niveau', view=view, ephemeral=True)

@bot.tree.command(name="mes-metiers", description="Renvoie les métiers et niveaux de l'utilisateur")
async def mesMetiers(interaction: discord.Interaction):
    metiers = db.get_data_from_user(interaction.user.name)
    if not metiers:
        await interaction.response.send_message("Vous n'avez pas encore renseigné de métiers.", ephemeral=True)
        return
    metiers_text = "\n".join([f"{metier} : {niveau}" for metier, niveau in metiers])
    await interaction.response.send_message(metiers_text, ephemeral=True)

@bot.tree.command(name="rechercher-metier", description="Recherche un métier par niveau")
async def rechercherMetier(interaction: discord.Interaction):
    view = recherchermetier.MetierSelectView()
    await interaction.response.send_message("Vous recherchez le métier :", view=view, ephemeral=True)

@bot.tree.command(name="ajouter-passage-donjon", description="Ajoute un donjon pour l'utilisateur")
async def ajouterPassageDonjon(interaction: discord.Interaction):
    donjondFromDb = db.get_donjons_from_user(interaction.user.name)
    available_options = [option for option in options if option.label not in donjondFromDb]
    if not available_options:
        await interaction.response.send_message("Vous pouvez déjà passer tous les donjons !", ephemeral=True)
        return
    view = ajouterpassagedonjon.DonjonSelectView(available_options)
    await interaction.response.send_message("Choisissez les donjons que vous pouvez faire passer :", view=view, ephemeral=True)

@bot.tree.command(name="mes-passages-donjons", description="Renvoie les donjons que l'utilisateur peut passer")
async def mesPassagesDonjons(interaction: discord.Interaction):
    donjons = db.get_donjons_from_user(interaction.user.name)
    if not donjons:
        await interaction.response.send_message("Vous n'avez renseigné aucun passage de donjon.", ephemeral=True)
        return
    donjons_text = "\n".join(donjons)
    await interaction.response.send_message(donjons_text, ephemeral=True)

@bot.tree.command(name="supprimer-passage-donjon", description="Supprime une liste de donjons pour l'utilisateur")
async def supprimerPassageDonjon(interaction: discord.Interaction):
    donjons = db.get_donjons_from_user(interaction.user.name)
    if not donjons:
        await interaction.response.send_message("Vous n'avez renseigné aucun passage de donjon.", ephemeral=True)
        return
    view = supprimerpassagedonjon.DonjonSuppressionView(donjons)
    await interaction.response.send_message("Choisissez les donjons à supprimer :", view=view, ephemeral=True)

@bot.tree.command(name="rechercher-passage-donjon", description="Recherche les utilisateurs qui peuvent passer un donjon")
async def rechercherPassageDonjon(interaction: discord.Interaction):
    donjons = options 
    view = rechercherpassagedonjon.DonjonSelectView(donjons)
    await interaction.response.send_message("Vous recherchez le donjon :", view=view, ephemeral=True)

db.instantiate_db()
bot.run(TOKEN)