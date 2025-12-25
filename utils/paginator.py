import discord

class PaginatorView(discord.ui.View):
    def __init__(self, embeds: list[discord.Embed]):
        super().__init__(timeout=300)
        self.current_page = 0
        self.embeds = embeds

    @discord.ui.button(label='<')
    async def backward(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        if self.current_page == -1:
            self.current_page = len(self.embeds) - 1

        await interaction.response.edit_message(
            content=f'Page {self.current_page + 1}/{len(self.embeds)}',embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label='>')
    async def forward(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        if self.current_page == len(self.embeds):
            self.current_page = 0

        await interaction.response.edit_message(
            content=f'Page {self.current_page + 1}/{len(self.embeds)}', embed=self.embeds[self.current_page], view=self)