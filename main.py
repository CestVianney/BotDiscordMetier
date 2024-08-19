import discord
import db.usersmetiersDb as db
import commands.ajoutermetier as ajoutermetier 
import commands.recherchermetier as recherchermetier
import commands.ajouterpassagedonjon as ajouterpassagedonjon
import commands.supprimerpassagedonjon as supprimerpassagedonjon
import commands.rechercherpassagedonjon as rechercherpassagedonjon
import commands.ajouterpassagequete as ajouterpassagequete
import commands.supprimerpassagequete as supprimerpassagequete
import commands.rechercherpassagequete as rechercherpassagequete
import commands.supprimerqueteexistante as supprimerqueteexistante
from discord.ext import commands
from utils.donjons import options
from functools import wraps

import os

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')
EK_ID = os.getenv('EK_ID')
TLB_ID = os.getenv('TLB_ID')
AUTHORIZED_GUILD_IDS = [EK_ID, TLB_ID]

def guild_only(*guild_ids):
    def decorator(func):
        @wraps(func)
        async def wrapper(interaction: discord.Interaction, *args, **kwargs):
            if interaction.guild_id not in guild_ids:
                await interaction.response.send_message("Cette commande n'est pas disponible dans cette guilde.", ephemeral=True)
                return
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {synced} commands")
    except Exception as e:
        print(f"An error occurred: {e}")

@bot.tree.command(name="ajouter-metiers", description="Ajoute les niveaux pour chaque métier")
@guild_only(*AUTHORIZED_GUILD_IDS)
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
@guild_only(*AUTHORIZED_GUILD_IDS)
async def rechercherMetier(interaction: discord.Interaction):
    view = recherchermetier.MetierSelectView()
    await interaction.response.send_message("Vous recherchez le métier :", view=view, ephemeral=True)

@bot.tree.command(name="ajouter-passage-donjon", description="Ajoute un donjon pour l'utilisateur")
@guild_only(*AUTHORIZED_GUILD_IDS)
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
@guild_only(*AUTHORIZED_GUILD_IDS)
async def supprimerPassageDonjon(interaction: discord.Interaction):
    donjons = db.get_donjons_from_user(interaction.user.name)
    if not donjons:
        await interaction.response.send_message("Vous n'avez renseigné aucun passage de donjon.", ephemeral=True)
        return
    view = supprimerpassagedonjon.DonjonSuppressionView(donjons)
    await interaction.response.send_message("Choisissez les donjons à supprimer :", view=view, ephemeral=True)

@bot.tree.command(name="rechercher-passage-donjon", description="Recherche les utilisateurs qui peuvent passer un donjon")
@guild_only(*AUTHORIZED_GUILD_IDS)
async def rechercherPassageDonjon(interaction: discord.Interaction):
    donjons = options 
    view = rechercherpassagedonjon.DonjonSelectView(donjons)
    await interaction.response.send_message("Vous recherchez le donjon :", view=view, ephemeral=True)

@bot.tree.command(name="creer-quete", description="Crée une quête")
@guild_only(*AUTHORIZED_GUILD_IDS)
async def creerQuete(interaction: discord.Interaction, nom_quete: str):
    db.insert_quete(nom_quete)
    await interaction.response.send_message(f"Création de la quête : {nom_quete}", ephemeral=True)

@bot.tree.command(name="quetes-existantes", description="Renvoie les quêtes existantes")
async def quetesExistantes(interaction: discord.Interaction):
    quetes = db.get_quetes_existantes()
    quetes.sort()
    if not quetes:
        await interaction.response.send_message("Il n'y a pas de quête existante.", ephemeral=True)
        return
    quetes_text = "\n".join(quetes)
    await interaction.response.send_message(quetes_text, ephemeral=True)

@bot.tree.command(name="supprimer-quete-existante", description="Supprime une quête existante")
@guild_only(*AUTHORIZED_GUILD_IDS)
async def supprimerQueteExistante(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Vous n'êtes pas autorisé à supprimer une quête.", ephemeral=True)
        return
    quetes = db.get_quetes_existantes()
    if not quetes:
        await interaction.response.send_message("Il n'y a pas de quête existante.", ephemeral=True)
        return
    view = supprimerqueteexistante.SupprimerQueteExistanteView(quetes)
    await interaction.response.send_message("Choisissez la quête à supprimer :", view=view, ephemeral=True)

@bot.tree.command(name="ajouter-passage-quete", description="Ajoute un passage de quête pour l'utilisateur")
@guild_only(*AUTHORIZED_GUILD_IDS)
async def ajouterPassageQuete(interaction: discord.Interaction):
    quetes = db.get_quetes_existantes()
    if not quetes:
        await interaction.response.send_message("Aucune quête n'a été créée ! Utilisez /creer-quete", ephemeral=True)
        return
    view = ajouterpassagequete.QueteSelectView(quetes)
    await interaction.response.send_message("Choisissez la quête pour laquelle vous avez un passage à proposer :", view=view, ephemeral=True)

@bot.tree.command(name="mes-passages-quetes", description="Renvoie les quêtes pour lesquelles l'utilisateur a un passage")
async def mesPassagesQuetes(interaction: discord.Interaction):
    quetes = db.get_quetes_from_user(interaction.user.name)
    if not quetes:
        await interaction.response.send_message("Vous n'avez renseigné aucun passage de quête.", ephemeral=True)
        return
    quetes_text = "\n".join(quetes)
    await interaction.response.send_message(quetes_text, ephemeral=True)


@bot.tree.command(name="supprimer-passage-quete", description="Supprime un passage de quête pour l'utilisateur")
@guild_only(*AUTHORIZED_GUILD_IDS)
async def supprimerPassageQuete(interaction: discord.Interaction):
    quetes = db.get_quetes_from_user(interaction.user.name)
    if not quetes:
        await interaction.response.send_message("Vous n'avez renseigné aucun passage de quête.", ephemeral=True)
        return
    view = supprimerpassagequete.QueteSuppressionView(quetes)
    await interaction.response.send_message("Choisissez la quête à supprimer :", view=view, ephemeral=True)

@bot.tree.command(name="rechercher-passage-quete", description="Recherche les utilisateurs qui peuvent passer une quête")
@guild_only(*AUTHORIZED_GUILD_IDS)
async def rechercherPassageQuete(interaction: discord.Interaction):
    quetes = db.get_quetes_existantes()
    if not quetes:
        await interaction.response.send_message("Aucune quête n'a été créée ! Utilisez /creer-quete", ephemeral=True)
        return
    view = rechercherpassagequete.RechercherPassageQueteView(quetes)
    await interaction.response.send_message("Vous recherchez la quête :", view=view, ephemeral=True)


db.instantiate_db()
bot.run(TOKEN)