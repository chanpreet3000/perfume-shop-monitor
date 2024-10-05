import os
import discord
from discord import app_commands
from ApplicationDataManager import ApplicationDataManager
from Logger import Logger
from dotenv import load_dotenv

load_dotenv()

WATCH_PRODUCT_CRON_DELAY_SECONDS = int(os.getenv('WATCH_PRODUCT_CRON_DELAY_SECONDS', 60 * 60))


class ProductScraperBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.data_manager = ApplicationDataManager()

    async def setup_hook(self):
        await self.tree.sync()
        Logger.info("Command tree synced")


client = ProductScraperBot()


@client.tree.command(name="ps-add-brand", description="Add a brand to the banned list")
async def add_brand(interaction: discord.Interaction, brand: str):
    Logger.info(f"Received add brand request for: {brand}")
    await interaction.response.defer(thinking=True)

    client.data_manager.add_banned_brand(brand)
    Logger.info(f"Added brand to banned list: {brand}")
    embed = discord.Embed(
        title="✅ Brand Added",
        description=f"Added '{brand}' to the banned brands list.",
        color=0x00ff00
    )
    await interaction.followup.send(embed=embed)


@client.tree.command(name="ps-remove-brand", description="Remove a brand from the banned list")
async def remove_brand(interaction: discord.Interaction, brand: str):
    Logger.info(f"Received remove brand request for: {brand}")
    await interaction.response.defer(thinking=True)

    client.data_manager.remove_banned_brand(brand)
    Logger.info(f"Removed brand from banned list: {brand}")
    embed = discord.Embed(
        title="✅ Brand Removed",
        description=f"Removed '{brand}' from the banned brands list.",
        color=0x00ff00
    )
    await interaction.followup.send(embed=embed)


@client.tree.command(name="ps-get-brands", description="Get all banned brands")
async def get_brands(interaction: discord.Interaction):
    Logger.info("Fetching all banned brands")
    await interaction.response.defer(thinking=True)

    banned_brands = client.data_manager.get_all_banned_brands()
    Logger.debug(f"Banned brands retrieved: {banned_brands}")
    if banned_brands:
        response = "\n".join([f"{i + 1}. {brand}" for i, brand in enumerate(banned_brands)])
        embed = discord.Embed(
            title="📋 Banned Brands",
            description=response,
            color=0x00ccff
        )
    else:
        Logger.warn("No banned brands found")
        embed = discord.Embed(
            title="🚫 No Banned Brands",
            description="There are no banned brands in the list.",
            color=0xff0000
        )

    await interaction.followup.send(embed=embed)


@client.tree.command(name="ps-set-interval", description="Set the cycle interval in seconds")
async def set_interval(interaction: discord.Interaction, interval: int):
    Logger.info(f"Received set interval request: {interval} seconds")
    await interaction.response.defer(thinking=True)

    client.data_manager.update_cycle_interval(interval)
    Logger.info(f"Updated cycle interval to {interval} seconds")
    embed = discord.Embed(
        title="✅ Interval Updated",
        description=f"Set the cycle interval to {interval} seconds.",
        color=0x00ff00
    )
    await interaction.followup.send(embed=embed)


@client.tree.command(name="ps-get-interval", description="Get the current cycle interval")
async def get_interval(interaction: discord.Interaction):
    Logger.info("Fetching current cycle interval")
    await interaction.response.defer(thinking=True)

    interval = client.data_manager.get_cycle_interval()
    Logger.debug(f"Current cycle interval: {interval} seconds")
    embed = discord.Embed(
        title="⏱️ Current Cycle Interval",
        description=f"The current cycle interval is set to {interval} seconds.",
        color=0x00ccff
    )
    await interaction.followup.send(embed=embed)


@client.tree.command(name="ps-add-link", description="Add a link to scrape")
async def add_link(interaction: discord.Interaction, link: str):
    Logger.info(f"Received add link request for: {link}")
    await interaction.response.defer(thinking=True)

    client.data_manager.add_link_to_scrape(link)
    Logger.info(f"Added link to scrape: {link}")
    embed = discord.Embed(
        title="✅ Link Added",
        description=f"Added '{link}' to the list of links to scrape.",
        color=0x00ff00
    )
    await interaction.followup.send(embed=embed)


@client.tree.command(name="ps-remove-link", description="Remove a link from the scrape list")
async def remove_link(interaction: discord.Interaction, link: str):
    Logger.info(f"Received remove link request for: {link}")
    await interaction.response.defer(thinking=True)

    client.data_manager.remove_link_to_scrape(link)
    Logger.info(f"Removed link from scrape list: {link}")
    embed = discord.Embed(
        title="✅ Link Removed",
        description=f"Removed '{link}' from the list of links to scrape.",
        color=0x00ff00
    )
    await interaction.followup.send(embed=embed)


@client.tree.command(name="ps-get-links", description="Get all links to scrape")
async def get_links(interaction: discord.Interaction):
    Logger.info("Fetching all links to scrape")
    await interaction.response.defer(thinking=True)

    links = client.data_manager.get_all_links_to_scrape()
    Logger.debug(f"Links to scrape retrieved: {links}")
    if links:
        response = "\n".join([f"{i + 1}. {link}" for i, link in enumerate(links)])
        embed = discord.Embed(
            title="📋 Links to Scrape",
            description=response,
            color=0x00ccff
        )
    else:
        Logger.warn("No links to scrape found")
        embed = discord.Embed(
            title="🚫 No Links to Scrape",
            description="There are no links in the scrape list.",
            color=0xff0000
        )

    await interaction.followup.send(embed=embed)


@client.tree.command(name="ps-add-channel", description="Add a notification channel")
async def add_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    Logger.info(f"Received add channel request for: {channel.id}")
    await interaction.response.defer(thinking=True)

    client.data_manager.add_notification_channel(str(channel.id))
    Logger.info(f"Added notification channel: {channel.id}")
    embed = discord.Embed(
        title="✅ Channel Added",
        description=f"Added {channel.mention} to the notification channels.",
        color=0x00ff00
    )
    await interaction.followup.send(embed=embed)


@client.tree.command(name="ps-remove-channel", description="Remove a notification channel")
async def remove_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    Logger.info(f"Received remove channel request for: {channel.id}")
    await interaction.response.defer(thinking=True)

    client.data_manager.remove_notification_channel(str(channel.id))
    Logger.info(f"Removed notification channel: {channel.id}")
    embed = discord.Embed(
        title="✅ Channel Removed",
        description=f"Removed {channel.mention} from the notification channels.",
        color=0x00ff00
    )
    await interaction.followup.send(embed=embed)


@client.tree.command(name="ps-get-channels", description="Get all notification channels")
async def get_channels(interaction: discord.Interaction):
    Logger.info("Fetching all notification channels")
    await interaction.response.defer(thinking=True)

    channels = client.data_manager.get_all_notification_channels()
    Logger.debug(f"Notification channels retrieved: {channels}")
    if channels:
        response = "\n".join([f"{i + 1}. <#{channel}>" for i, channel in enumerate(channels)])
        embed = discord.Embed(
            title="📋 Notification Channels",
            description=response,
            color=0x00ccff
        )
    else:
        Logger.warn("No notification channels found")
        embed = discord.Embed(
            title="🚫 No Notification Channels",
            description="There are no notification channels set.",
            color=0xff0000
        )

    await interaction.followup.send(embed=embed)


@client.event
async def on_ready():
    Logger.info(f'Bot is now online and ready to use: {client.user}')


def run_bot():
    Logger.info("Initializing Discord bot")
    discord_token = os.getenv('DISCORD_BOT_TOKEN')
    client.run(discord_token)
