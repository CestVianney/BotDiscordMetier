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
import io
import hashlib
from discord.ext import commands
from utils.donjons import options
from functools import wraps

import os

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = os.getenv('OWNER_ID')

def is_owner():
    def decorator(func):
        @wraps(func)
        async def wrapper(interaction: discord.Interaction, *args, **kwargs):
            if OWNER_ID != str(interaction.user.id):
                await interaction.response.send_message("Pas touche :)", ephemeral=True)
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
async def ajouterMetiers(interaction: discord.Interaction):
    user = interaction.user
    metiersFromDb = db.get_data_from_user(user.guild.id, user.name)
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
    user = interaction.user
    metiers = db.get_data_from_user(user.guild.id, user.name)
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
    user = interaction.user
    donjondFromDb = db.get_donjons_from_user(user.guild.id, user.name)
    available_options = [option for option in options if option.label not in donjondFromDb]
    if not available_options:
        await interaction.response.send_message("Vous pouvez déjà passer tous les donjons !", ephemeral=True)
        return
    view = ajouterpassagedonjon.DonjonSelectView(available_options)
    await interaction.response.send_message("Choisissez les donjons que vous pouvez faire passer :", view=view, ephemeral=True)

@bot.tree.command(name="mes-passages-donjons", description="Renvoie les donjons que l'utilisateur peut passer")
async def mesPassagesDonjons(interaction: discord.Interaction):
    user = interaction.user
    donjons = db.get_donjons_from_user(user.guild.id, user.name)
    if not donjons:
        await interaction.response.send_message("Vous n'avez renseigné aucun passage de donjon.", ephemeral=True)
        return
    donjons_text = "\n".join(donjons)
    await interaction.response.send_message(donjons_text, ephemeral=True)

@bot.tree.command(name="supprimer-passage-donjon", description="Supprime une liste de donjons pour l'utilisateur")
async def supprimerPassageDonjon(interaction: discord.Interaction):
    user = interaction.user
    donjons = db.get_donjons_from_user(user.guild.id, user.name)
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

@bot.tree.command(name="admin-creer-quete", description="Crée une quête")
@is_owner()
async def adminCreerQuete(interaction: discord.Interaction, nom_quete: str):
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

@bot.tree.command(name="admin-supprimer-quete-existante", description="Supprime une quête existante")
@is_owner()
async def adminSupprimerQueteExistante(interaction: discord.Interaction):
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
async def ajouterPassageQuete(interaction: discord.Interaction):
    quetes = db.get_quetes_existantes()
    if not quetes:
        await interaction.response.send_message("Aucune quête n'a été créée ! Utilisez /creer-quete", ephemeral=True)
        return
    view = ajouterpassagequete.QueteSelectView(quetes)
    await interaction.response.send_message("Choisissez la quête pour laquelle vous avez un passage à proposer :", view=view, ephemeral=True)

@bot.tree.command(name="mes-passages-quetes", description="Renvoie les quêtes pour lesquelles l'utilisateur a un passage")
async def mesPassagesQuetes(interaction: discord.Interaction):
    user = interaction.user
    quetes = db.get_quetes_from_user(user.guild.id, user.name)
    if not quetes:
        await interaction.response.send_message("Vous n'avez renseigné aucun passage de quête.", ephemeral=True)
        return
    quetes_text = "\n".join(quetes)
    await interaction.response.send_message(quetes_text, ephemeral=True)


@bot.tree.command(name="supprimer-passage-quete", description="Supprime un passage de quête pour l'utilisateur")
async def supprimerPassageQuete(interaction: discord.Interaction):
    user = interaction.user
    quetes = db.get_quetes_from_user(user.guild.id, user.name)
    if not quetes:
        await interaction.response.send_message("Vous n'avez renseigné aucun passage de quête.", ephemeral=True)
        return
    view = supprimerpassagequete.QueteSuppressionView(quetes)
    await interaction.response.send_message("Choisissez la quête à supprimer :", view=view, ephemeral=True)

@bot.tree.command(name="rechercher-passage-quete", description="Recherche les utilisateurs qui peuvent passer une quête")
async def rechercherPassageQuete(interaction: discord.Interaction):
    quetes = db.get_quetes_existantes()
    if not quetes:
        await interaction.response.send_message("Aucune quête n'a été créée ! Utilisez /creer-quete", ephemeral=True)
        return
    view = rechercherpassagequete.RechercherPassageQueteView(quetes)
    await interaction.response.send_message("Vous recherchez la quête :", view=view, ephemeral=True)

@bot.tree.command(name="admin-extract-db", description="Extraction de la base de données")
@is_owner()
async def adminExtractDb(interaction: discord.Interaction):
    await send_db_file(interaction.channel)

async def send_db_file(channel):
    try:
        with open('database.db', 'rb') as db_file:
            await channel.send("Voici votre base de données :", file=discord.File(db_file, 'database.db'))
    except Exception as e:
        await channel.send(f"Une erreur s'est produite lors de l'extraction de la base de données : {e}")

@bot.hybrid_command(name="admin-upload", description="Upload a file")
@is_owner()
async def adminUpload(ctx, attachment: discord.Attachment):
    await ctx.defer()
    message = await ctx.send("Uploading your file...")

    # Lire le fichier attaché
    file_data = await attachment.read()
    file_name = "database.db"
    print(f"Uploading file {file_name}")

    # Calculer le hash du fichier
    await message.edit(content="Calculating file hash")
    hash_value = hashlib.sha256(file_data).hexdigest()
    await message.edit(content=f"File hash: {hash_value}")

    # Calculer la taille du fichier en octets
    bytes_io = io.BytesIO(file_data)
    await message.edit(content="Calculating file bytes size")
    bytes_size = len(bytes_io.getbuffer())
    await message.edit(content=f"File bytes size: {bytes_size}")

    # Sauvegarder le fichier à la racine du projet
    file_path = os.path.join(os.getcwd(), file_name)
    try:
        with open(file_path, 'wb') as file:
            file.write(file_data)
        print(f"File saved as {file_path}")
        await message.edit(content="File uploaded and saved successfully.")
    except Exception as e:
        print(f"Error saving file: {e}")
        await message.edit(content=f"An error occurred while saving the file: {e}")

db.instantiate_db()
bot.run(TOKEN)