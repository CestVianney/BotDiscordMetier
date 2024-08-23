import discord
import db.usersmetiersDb as db
from discord.ui import View, Button, Modal, TextInput, Select

class MetierNiveauModal(Modal):
    def __init__(self, metier, callback, user, button):
        super().__init__(title=f"Niveau pour {metier}")
        self.metier = metier
        self.callback = callback
        self.user = user
        self.button = button
        self.niveau = TextInput(label="Niveau", placeholder="Entrez un niveau entre 1 et 200", min_length=1, max_length=3)
        self.add_item(self.niveau)

    async def on_submit(self, interaction: discord.Interaction):
        niveau = self.niveau.value
        if not niveau.isdigit() or not (1 <= int(niveau) <= 200):
            await interaction.response.send_message("Veuillez entrer un niveau valide entre 1 et 200.", ephemeral=True)
            return
        # Mettre à jour le label et le style du bouton
        self.button.label = f"{self.metier} : {niveau}"
        self.button.style = discord.ButtonStyle.success if int(niveau) == 200 else discord.ButtonStyle.primary
        await interaction.response.edit_message(view=self.button.view)  # Rafraîchir l'affichage du bouton
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
            if niveau == 0:
                button_style = discord.ButtonStyle.danger  
            elif niveau == 200:
                button_style = discord.ButtonStyle.success
            else:
                button_style = discord.ButtonStyle.primary  
            button = Button(label=f"{metier} : {niveau}", style=button_style)
            button.callback = self.create_callback(metier, button)
            self.add_item(button)

    def create_callback(self, metier, button):
        async def callback(interaction: discord.Interaction):
            modal = MetierNiveauModal(metier, self.callback, self.user, button)
            await interaction.response.send_modal(modal)
        return callback

async def save_niveau(interaction: discord.Interaction, metier, niveau, user):
    db.insert_data(user.guild.id, user.name, metier, niveau)
    await interaction.response.defer()  # Déférer la réponse pour éviter les erreurs de délai
