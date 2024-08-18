import discord
import db.usersmetiersDb as db
from discord.ui import View, Select

class SupprimerQueteExistanteView(View):
    def __init__(self, quetes):
        super().__init__()
        options = [discord.SelectOption(label=quete, value=quete) for quete in quetes]
        option_groups = [options[i:i + 25] for i in range(0, len(options), 25)]
        for i, group in enumerate(option_groups):
            select = Select(
                placeholder=f"Choisissez une quête à supprimer (groupe {i + 1})",
                min_values=1,
                max_values=1,
                options=group,
                custom_id=f"quete_select_{i}"
            )
            select.callback = self.select_callback
            self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        selected_quetes = [option for option in interaction.data['values']]
        quete = selected_quetes[0]
        db.delete_quete_existante(quete)
        await interaction.response.edit_message(
            content=f"La quête {quete} a été supprimée.",
            view=None
        )
        self.stop()