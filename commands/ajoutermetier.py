import discord
import db.usersmetiersDb as db
from discord.ui import View, Button, Modal, TextInput, Select

class MetierNiveauModal(Modal):
    def __init__(self, metier, callback, user):
        super().__init__(title=f"Niveau pour {metier}")
        self.metier = metier
        self.callback = callback
        self.user = user
        self.niveau = TextInput(label="Niveau", placeholder="Entrez un niveau entre 1 et 200", min_length=1, max_length=3)
        self.add_item(self.niveau)

    async def on_submit(self, interaction: discord.Interaction):
        niveau = self.niveau.value
        if not niveau.isdigit() or not (1 <= int(niveau) <= 200):
            await interaction.response.send_message("Veuillez entrer un niveau valide entre 1 et 200.", ephemeral=True)
            return
        await self.callback(interaction, self.metier, int(niveau), self.user)

class MetierNiveauView(View):
    def __init__(self, metiers, callback, user):
        super().__init__()
        self.metiers = metiers
        self.callback = callback
        self.user = user
        self.add_buttons()

    def add_buttons(self):
        for metier, niveau in self.metiers:
            button = Button(label=metier + " : " + str(niveau), style=discord.ButtonStyle.primary)
            button.callback = self.create_callback(metier)
            self.add_item(button)

    def create_callback(self, metier):
        async def callback(interaction: discord.Interaction):
            modal = MetierNiveauModal(metier, self.callback, self.user)
            await interaction.response.send_modal(modal)
        return callback

async def save_niveau(interaction: discord.Interaction, metier, niveau, user):
    user_mention = user.mention
    db.insert_data(user.name, metier, niveau)
    await interaction.response.send_message(f"Niveau pour {metier} enregistré: {niveau} par {user_mention}", ephemeral=True)
