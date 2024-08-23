import discord
import db.usersmetiersDb as db
from discord.ui import View, Select

class DonjonSelectView(View):
    def __init__(self, options):
        super().__init__()
        option_groups = [options[i:i + 25] for i in range(0, len(options), 25)]
        for i, group in enumerate(option_groups):
            select = Select(
                placeholder=f"Choisissez les donjons (groupe {i + 1})",
                min_values=1,
                max_values=len(group),
                options=group,
                custom_id=f"donjon_select_{i}"
            )
            select.callback = self.select_callback
            self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        selected_donjons = [option for option in interaction.data['values']]
        user = interaction.user
        db.save_donjons_for_user(user.guild.id, user.name, selected_donjons)
        await interaction.response.edit_message(
            content=f"Donjons sélectionnés : {', '.join(selected_donjons)}",
            view=None  
        )
        self.stop()  
