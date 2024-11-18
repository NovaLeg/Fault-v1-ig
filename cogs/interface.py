import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import time

class VoiceMasterControlPanel(View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog
        self.last_interaction = {}

    async def user_owns_temp_channel(self, user):
        return user.id in self.cog.temp_channels

    async def send_error_message(self, interaction, message):
        await interaction.response.send_message(message, ephemeral=True)

    async def is_cooldown(self, user_id):
        current_time = time.time()
        last_time = self.last_interaction.get(user_id, 0)
        cooldown_period = 3
        if current_time - last_time < cooldown_period:
            return True
        self.last_interaction[user_id] = current_time
        return False

    async def get_user_channel(self, user):
        channel_id = self.cog.temp_channels.get(user.id)
        if channel_id:
            return self.cog.bot.get_channel(channel_id)
        return None

    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, custom_id="voicemaster:lock", emoji="<:lock:1285222682878804019>")
    async def lock_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.is_cooldown(interaction.user.id):
            await self.send_error_message(interaction, "Please wait 3 seconds before using this button again.")
            return

        if not await self.user_owns_temp_channel(interaction.user):
            await self.send_error_message(interaction, "You do not own a temporary voice channel.")
            return

        channel = await self.get_user_channel(interaction.user)
        if channel:
            await channel.set_permissions(interaction.guild.default_role, connect=False)
            await interaction.response.send_message(f"Channel {channel.name} is locked.", ephemeral=True)

    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, custom_id="voicemaster:unlock", emoji="<:unlock:1285222452426702908>")
    async def unlock_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.is_cooldown(interaction.user.id):
            await self.send_error_message(interaction, "Please wait 3 seconds before using this button again.")
            return

        if not await self.user_owns_temp_channel(interaction.user):
            await self.send_error_message(interaction, "You do not own a temporary voice channel.")
            return

        channel = await self.get_user_channel(interaction.user)
        if channel:
            await channel.set_permissions(interaction.guild.default_role, connect=True)
            await interaction.response.send_message(f"Channel {channel.name} is unlocked.", ephemeral=True)

    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, custom_id="voicemaster:hide", emoji="<:hide:1285222917268963379>")
    async def hide_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.is_cooldown(interaction.user.id):
            await self.send_error_message(interaction, "Please wait 3 seconds before using this button again.")
            return

        if not await self.user_owns_temp_channel(interaction.user):
            await self.send_error_message(interaction, "You do not own a temporary voice channel.")
            return

        channel = await self.get_user_channel(interaction.user)
        if channel:
            await channel.set_permissions(interaction.guild.default_role, view_channel=False)
            await interaction.response.send_message(f"Channel {channel.name} is hidden.", ephemeral=True)

    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, custom_id="voicemaster:unhide", emoji="<:unhide:1285222758627934301>")
    async def unhide_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.is_cooldown(interaction.user.id):
            await self.send_error_message(interaction, "Please wait 3 seconds before using this button again.")
            return

        if not await self.user_owns_temp_channel(interaction.user):
            await self.send_error_message(interaction, "You do not own a temporary voice channel.")
            return

        channel = await self.get_user_channel(interaction.user)
        if channel:
            await channel.set_permissions(interaction.guild.default_role, view_channel=True)
            await interaction.response.send_message(f"Channel {channel.name} is unhidden.", ephemeral=True)

    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, custom_id="voicemaster:rename", emoji="<:rename:1285223098437730364>")
    async def rename_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.is_cooldown(interaction.user.id):
            await self.send_error_message(interaction, "Please wait 3 seconds before using this button again.")
            return

        if not await self.user_owns_temp_channel(interaction.user):
            await self.send_error_message(interaction, "You do not own a temporary voice channel.")
            return

        await interaction.response.send_modal(RenameChannelModal(self))

    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, custom_id="voicemaster:set_limit", emoji="<:limit:1285223757643911269>")
    async def set_limit_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.is_cooldown(interaction.user.id):
            await self.send_error_message(interaction, "Please wait 3 seconds before using this button again.")
            return

        if not await self.user_owns_temp_channel(interaction.user):
            await self.send_error_message(interaction, "You do not own a temporary voice channel.")
            return

        await interaction.response.send_modal(SetLimitModal(self))

    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, custom_id="voicemaster:set_bitrate", emoji="<:bitrate:1285223987835568158>")
    async def set_bitrate_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.is_cooldown(interaction.user.id):
            await self.send_error_message(interaction, "Please wait 3 seconds before using this button again.")
            return

        if not await self.user_owns_temp_channel(interaction.user):
            await self.send_error_message(interaction, "You do not own a temporary voice channel.")
            return

        await interaction.response.send_modal(SetBitrateModal(self))

    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, custom_id="voicemaster:transfer_ownership", emoji="<:crown:1285224509485486080>")
    async def transfer_ownership(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.is_cooldown(interaction.user.id):
            await self.send_error_message(interaction, "Please wait 3 seconds before using this button again.")
            return

        if not await self.user_owns_temp_channel(interaction.user):
            await self.send_error_message(interaction, "You do not own a temporary voice channel.")
            return

        await interaction.response.send_modal(TransferOwnershipModal(self, interaction))

    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, custom_id="voicemaster:kick", emoji="<:kick:1285224560475770988>")
    async def kick_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.is_cooldown(interaction.user.id):
            await self.send_error_message(interaction, "Please wait 3 seconds before using this button again.")
            return

        if not await self.user_owns_temp_channel(interaction.user):
            await self.send_error_message(interaction, "You do not own a temporary voice channel.")
            return

        await interaction.response.send_modal(KickUserModal(self))

class RenameChannelModal(Modal, title="Rename Channel"):
    new_name = TextInput(label="New Channel Name", required=True)

    def __init__(self, control_panel):
        super().__init__()
        self.control_panel = control_panel

    async def on_submit(self, interaction: discord.Interaction):
        channel = await self.control_panel.get_user_channel(interaction.user)
        if channel:
            try:
                await channel.edit(name=self.new_name.value)
                await interaction.response.send_message(f"Channel renamed to {self.new_name.value}.", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("I don't have permission to rename this channel.", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"An unexpected error occurred: {e}", ephemeral=True)

class SetLimitModal(Modal, title="Set User Limit"):
    limit = TextInput(label="User Limit", required=True, placeholder="e.g., 10")

    def __init__(self, control_panel):
        super().__init__()
        self.control_panel = control_panel

    async def on_submit(self, interaction: discord.Interaction):
        channel = await self.control_panel.get_user_channel(interaction.user)
        if channel:
            try:
                limit = int(self.limit.value)
                await channel.edit(user_limit=limit)
                await interaction.response.send_message(f"User limit set to {limit}.", ephemeral=True)
            except ValueError:
                await interaction.response.send_message("Invalid limit value.", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("I don't have permission to set the limit.", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"An unexpected error occurred: {e}", ephemeral=True)

class SetBitrateModal(Modal, title="Set Bitrate"):
    bitrate = TextInput(label="Bitrate (kbps)", required=True, placeholder="e.g., 64")

    def __init__(self, control_panel):
        super().__init__()
        self.control_panel = control_panel

    async def on_submit(self, interaction: discord.Interaction):
        channel = await self.control_panel.get_user_channel(interaction.user)
        if channel:
            try:
                bitrate = int(self.bitrate.value) * 1000
                await channel.edit(bitrate=bitrate)
                await interaction.response.send_message(f"Bitrate set to {self.bitrate.value} kbps.", ephemeral=True)
            except ValueError:
                await interaction.response.send_message("Invalid bitrate value.", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("I don't have permission to set the bitrate.", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"An unexpected error occurred: {e}", ephemeral=True)

class TransferOwnershipModal(Modal, title="Transfer Ownership"):
    user_id = TextInput(label="User ID", required=True)

    def __init__(self, control_panel, interaction):
        super().__init__()
        self.control_panel = control_panel
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_id = int(self.user_id.value)
            new_owner = self.interaction.guild.get_member(user_id)
            if not new_owner:
                await interaction.response.send_message("User not found.", ephemeral=True)
                return

            old_channel = await self.control_panel.get_user_channel(self.interaction.user)
            if old_channel:
                self.control_panel.cog.temp_channels.pop(self.interaction.user.id, None)
                self.control_panel.cog.temp_channels[new_owner.id] = old_channel.id
                await interaction.response.send_message(f"Ownership transferred to {new_owner.mention}.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Invalid user ID.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An unexpected error occurred: {e}", ephemeral=True)

class KickUserModal(Modal, title="Kick User"):
    user_id = TextInput(label="User ID", required=True)

    def __init__(self, control_panel):
        super().__init__()
        self.control_panel = control_panel

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_id = int(self.user_id.value)
            member = interaction.guild.get_member(user_id)
            if not member:
                await interaction.response.send_message("User not found.", ephemeral=True)
                return

            channel = await self.control_panel.get_user_channel(interaction.user)
            if channel:
                await channel.set_permissions(member, connect=False)
                await interaction.response.send_message(f"{member.mention} has been kicked from the channel.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Invalid user ID.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An unexpected error occurred: {e}", ephemeral=True)

class VoiceMasterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_channels = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord.')

    async def start_control_panel(self, interaction: discord.Interaction):
        view = VoiceMasterControlPanel(self)
        await interaction.response.send_message("Voice Master Control Panel", view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(VoiceMasterCog(bot))
