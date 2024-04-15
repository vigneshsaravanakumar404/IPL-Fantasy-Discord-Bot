from typing import Callable, Optional
from discord import ui, Interaction, Embed, ButtonStyle, Button


class Pagination(ui.View):
    """
    A class to represent a pagination view for a discord message.
    """

    def __init__(self, interaction: Interaction, get_page: Callable):
        """
        Initializes a Pagination object.

        Args:
            interaction (Interaction): The interaction object representing the user's interaction with the bot.
            get_page (Callable): A callable object that returns the content of a specific page.

        Attributes:
            interaction (Interaction): The interaction object representing the user's interaction with the bot.
            get_page (Callable): A callable object that returns the content of a specific page.
            total_pages (Optional[int]): The total number of pages. Defaults to None.
            index (int): The current page index. Defaults to 1.
        """
        self.interaction = interaction
        self.get_page = get_page
        self.total_pages: Optional[int] = None
        self.index = 1
        super().__init__(timeout=100)

    async def interaction_check(self, interaction: Interaction) -> bool:
        """
        Checks if the interaction user is the author of the command.

        Parameters:
        - interaction (Interaction): The interaction object representing the user's interaction with the bot.

        Returns:
        - bool: True if the interaction user is the author of the command, False otherwise.
        """
        if interaction.user == self.interaction.user:
            return True
        else:
            emb = Embed(
                description=f"Only the author of the command can perform this action.",
                color=16711680,
            )
            await interaction.response.send_message(embed=emb, ephemeral=True)
            return False

    async def navegate(self):
        """
        Navigates through the pages and sends the appropriate message with the embed.

        This method retrieves the embed and total number of pages using the `get_page` method.
        If there is only one page, it sends the message with the embed.
        If there are multiple pages, it updates the buttons and sends the message with the embed and view.

        Parameters:
        - None

        Returns:
        - None
        """
        emb, self.total_pages = await self.get_page(self.index)
        if self.total_pages == 1:
            await self.interaction.response.send_message(embed=emb)
        elif self.total_pages > 1:
            self.update_buttons()
            await self.interaction.response.send_message(embed=emb, view=self)

    async def edit_page(self, interaction: Interaction):
        """
        Edits the current page of the pagination.

        Parameters:
        - interaction (Interaction): The interaction object representing the user's interaction with the pagination.

        Returns:
        - None

        This method retrieves the embed and total number of pages for the current index,
        updates the buttons, and then edits the message with the new embed and view.
        """
        emb, self.total_pages = await self.get_page(self.index)
        self.update_buttons()
        await interaction.response.edit_message(embed=emb, view=self)

    def update_buttons(self):
        """
        Updates the buttons based on the current index and total pages.

        If the index is greater than half of the total pages, the emoji of the middle button is set to "⏮️".
        Otherwise, the emoji of the middle button is set to "⏭️".

        The first button is disabled if the index is 1, and the last button is disabled if the index is equal to the total pages.
        """
        if self.index > self.total_pages // 2:
            self.children[2].emoji = "⏮️"
        else:
            self.children[2].emoji = "⏭️"
        self.children[0].disabled = self.index == 1
        self.children[1].disabled = self.index == self.total_pages

    @ui.button(emoji="◀️", style=ButtonStyle.success)
    async def previous(self, interaction: Interaction, button: Button):
        """
        Decreases the index by 1 and edits the page.

        Parameters:
        - interaction (Interaction): The interaction object representing the user's interaction with the button.
        - button (Button): The button object representing the button that was clicked.

        Returns:
        None
        """
        self.index -= 1
        await self.edit_page(interaction)

    @ui.button(emoji="▶️", style=ButtonStyle.success)
    async def next(self, interaction: Interaction, button: Button):
        """
        Increments the index by 1 and edits the page.

        Parameters:
        - interaction (Interaction): The interaction object representing the user's interaction with the button.
        - button (Button): The button object representing the button that was clicked.

        Returns:
        None
        """
        self.index += 1
        await self.edit_page(interaction)

    @ui.button(emoji="⏭️", style=ButtonStyle.blurple)
    async def end(self, interaction: Interaction, button: Button):
        """
        Moves the pagination to the last page if the current index is less than or equal to half of the total pages,
        otherwise moves the pagination to the first page.

        Parameters:
        - interaction (Interaction): The interaction object representing the user's interaction with the button.
        - button (Button): The button object representing the button that was clicked.
        """
        if self.index <= self.total_pages // 2:
            self.index = self.total_pages
        else:
            self.index = 1
        await self.edit_page(interaction)

    async def on_timeout(self):
        """
        Handles the timeout event for the pagination.

        This method is called when the pagination times out. It retrieves the original response message
        and removes the pagination view from it.

        Returns:
            None
        """
        message = await self.interaction.original_response()
        await message.edit(view=None)

    @staticmethod
    def compute_total_pages(total_results: int, results_per_page: int) -> int:
        """
        Computes the total number of pages based on the total number of results and the number of results per page.

        Args:
            total_results (int): The total number of results.
            results_per_page (int): The number of results to display per page.

        Returns:
            int: The total number of pages.

        """
        return ((total_results - 1) // results_per_page) + 1
