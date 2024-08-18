import discord
from discord.ui import View, Modal, TextInput, Select
import db.usersmetiersDb as db

class NiveauModal(Modal):
    def __init__(self, metier):
        super().__init__(title=f"Niveau pour {metier}")
        self.metier = metier
        self.niveau = TextInput(label="Niveau", placeholder="Entrez un niveau entre 1 et 200", min_length=1, max_length=3)
        self.add_item(self.niveau)

    async def on_submit(self, interaction: discord.Interaction):
        niveau = self.niveau.value
        if not niveau.isdigit() or not (1 <= int(niveau) <= 200):
            await interaction.response.send_message("Veuillez entrer un niveau valide entre 1 et 200.", ephemeral=True)
            return
        
        result = db.get_metier_par_niveau(self.metier, int(niveau))
        
        guild = interaction.guild
        members = []
        async for member in guild.fetch_members(limit=None):
            members.append(member)
        
        tagged_users = []
        for username in result:
            user = discord.utils.get(members, name=username)
            if user:
                tagged_users.append(user.mention)
        
        if tagged_users:
            message = f"Utilisateurs trouvés : {' '.join(tagged_users)}"
        else:
            message = "Aucun utilisateur trouvé."
        
        message += f"\nNiveau pour {self.metier} : {niveau}"
        await interaction.response.send_message(message, ephemeral=True)

class MetierSelectView(View):
    def __init__(self):
        super().__init__()
        select = Select(
            placeholder="Choisissez un métier",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label='Alchimiste', value='Alchimiste'),
                discord.SelectOption(label='Bijoutier', value='Bijoutier'),
                discord.SelectOption(label='Bricoleur', value='Bricoleur'),
                discord.SelectOption(label='Bucheron', value='Bucheron'),
                discord.SelectOption(label='Chasseur', value='Chasseur'),
                discord.SelectOption(label='Cordomage', value='Cordomage'),
                discord.SelectOption(label='Cordonnier', value='Cordonnier'),
                discord.SelectOption(label='Costumage', value='Costumage'),
                discord.SelectOption(label='Facomage', value='Facomage'),
                discord.SelectOption(label='Faconneur', value='Faconneur'),
                discord.SelectOption(label='Forgeron', value='Forgeron'),
                discord.SelectOption(label='Forgemage', value='Forgemage'),
                discord.SelectOption(label='Joaillomage', value='Joaillomage'),
                discord.SelectOption(label='Mineur', value='Mineur'),
                discord.SelectOption(label='Paysan', value='Paysan'),
                discord.SelectOption(label='Pecheur', value='Pecheur'),
                discord.SelectOption(label='Sculpteur', value='Sculpteur'),
                discord.SelectOption(label='Sculptemage', value='Sculptemage'),
                discord.SelectOption(label='Tailleur', value='Tailleur')
            ],
            custom_id="metier_select"
        )
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        metier = interaction.data['values'][0]
        modal = NiveauModal(metier)
        await interaction.response.send_modal(modal)
