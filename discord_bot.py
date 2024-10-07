import asyncio
import os
import discord
from discord import app_commands
from ApplicationDataManager import ApplicationDataManager
from LatestPriceDataManager import LatestPriceDataManager
from Logger import Logger
from dotenv import load_dotenv

from fetcher import scrape_products, ScrapedProduct
from scraper import fetch_products_parallel
from utils import get_current_time, sleep_randomly

load_dotenv()


class ProductScraperBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.data_manager = ApplicationDataManager()
        self.price_manager = LatestPriceDataManager()
        self.scraper_task = None

    async def setup_hook(self):
        await self.tree.sync()
        Logger.info("Command tree synced")
        self.scraper_task = self.loop.create_task(self.run_scraper_cycle())

    async def close(self):
        if self.scraper_task:
            self.scraper_task.cancel()
        await super().close()

    async def run_scraper_cycle(self):
        while True:
            try:
                Logger.info("Starting scraper cycle")

                links_to_scrape = self.data_manager.get_all_links_to_scrape()

                if not links_to_scrape:
                    Logger.warn("No links to scrape. Skipping this cycle.")
                else:
                    products = await self.loop.run_in_executor(None, scrape_products, links_to_scrape)

                    banned_brands = self.data_manager.get_all_banned_brands()
                    filtered_products = [
                        product for product in products
                        if
                        product.brand.lower() not in (brand.lower() for brand in banned_brands) and product.is_in_stock
                    ]

                    Logger.info(
                        f"Scraped {len(products)} products, {len(filtered_products)} after filtering banned brands")

                    filtered_products = await self.loop.run_in_executor(None, fetch_products_parallel,
                                                                        filtered_products)

                    new_products = []
                    price_drops = []

                    # Check for new products and price drops
                    for product in filtered_products:
                        latest_price = self.price_manager.get_value(product.uid)
                        if latest_price is None:
                            new_products.append(product)
                        elif product.price < latest_price:
                            price_drops.append(product)

                    # Update latest prices
                    self.price_manager.set_multiple_values(
                        [(product.uid, product.price) for product in filtered_products])

                    Logger.info(f"Found {len(new_products)} new products and {len(price_drops)} price drops")

                    if new_products:
                        content = f"🎉 @here Exciting news! {len(new_products)} New products have just arrived. Be the first to check them out!"
                        await self.send_products_info_to_discord(new_products, 0x00FF00, content)

                    if price_drops:
                        content = f"💰 @here Alert! {len(price_drops)} Price drops detected. Don't miss out on these amazing deals!"
                        await self.send_products_info_to_discord(price_drops, 0xffff00, content)

                cycle_interval = self.data_manager.get_cycle_interval()
                Logger.info(f"Scraper cycle completed. Sleeping for {cycle_interval} seconds.")

                await asyncio.sleep(cycle_interval)

            except asyncio.CancelledError:
                Logger.info("Scraper cycle task cancelled")
                break
            except Exception as e:
                Logger.error("Error in scraper cycle", e)
                await asyncio.sleep(10 * 60)

    async def send_products_info_to_discord(self, products: list[ScrapedProduct], embed_color: int, content: str):
        Logger.info(f'Sending {len(products)} products to Discord')

        chunk_size = 10
        channels = self.data_manager.get_all_notification_channels()

        for i in range(0, len(products), chunk_size):
            chunk = products[i:i + chunk_size]

            embeds = [self.create_embed(product, embed_color) for product in
                      chunk]

            for channel_id in channels:
                channel = self.get_channel(int(channel_id))
                if channel:
                    try:
                        await channel.send(content=content if i == 0 else '', embeds=embeds)
                        Logger.info(
                            f"Message sent successfully to channel {channel_id} (Products {i + 1} to {i + len(chunk)})")
                    except Exception as error:
                        Logger.error(
                            f"Error sending message to channel {channel_id} (Products {i + 1} to {i + len(chunk)})",
                            error)
                else:
                    Logger.warn(f"Channel {channel_id} not found")

            await sleep_randomly(5, 0, 'Sleeping after sending products to Discord')

    def create_embed(self, product: ScrapedProduct, embed_color: int):
        previous_price = product.latest_price if product.latest_price is not None else product.price
        if previous_price is None:
            discount_from_previous_scan = 100
        else:
            discount_from_previous_scan = ((previous_price - product.price) / previous_price) * 100

        embed = discord.Embed(
            title=f"{product.name} - {product.variant_info}",
            url=product.url,
            color=embed_color
        )
        embed.add_field(name="Current Price", value=product.price, inline=True)
        embed.add_field(name="Previous Scan Price", value=previous_price, inline=True)
        embed.add_field(name="SKU", value=product.default_sku, inline=True)
        embed.add_field(name="Discount From Previous Scan", value=f"{discount_from_previous_scan:.2f}% Off!",
                        inline=True)
        embed.add_field(name="Brand", value=product.brand, inline=True)

        promotions = {promo["reward"]["rewardType"] for promo in product.promotions}
        if product.promotions:
            embed.add_field(name="Promotions", value="\n".join(f"• {promo}" for promo in promotions), inline=False)

        embed.set_footer(text=f"🕒 Time: {get_current_time()} (UK)")
        return embed


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
