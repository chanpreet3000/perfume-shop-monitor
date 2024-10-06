# Perfume Shop Discord Bot

This Discord bot scrapes the Perfume Shop API to monitor new products and price drops. It provides real-time updates to
designated Discord channels about new arrivals and discounts on perfumes and related products.

## Features

- Scrapes the Perfume Shop API at regular intervals
- Detects new products and price drops
- Sends notifications to designated Discord channels
- Allows management of banned brands, scrape links, and notification channels
- Configurable scrape cycle interval

## Setup

1. Clone this repository to your local machine.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your Discord bot token:
   ```
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   ```
4. Run the bot:
   ```
   python discord_bot.py
   ```

## Discord Commands

The bot supports the following commands:

- `/ps-add-brand <brand>`: Add a brand to the banned list
- `/ps-remove-brand <brand>`: Remove a brand from the banned list
- `/ps-get-brands`: Get all banned brands
- `/ps-set-interval <seconds>`: Set the scrape cycle interval in seconds
- `/ps-get-interval`: Get the current scrape cycle interval
- `/ps-add-link <link>`: Add a link to scrape
- `/ps-remove-link <link>`: Remove a link from the scrape list
- `/ps-get-links`: Get all links to scrape
- `/ps-add-channel <channel>`: Add a notification channel
- `/ps-remove-channel <channel>`: Remove a notification channel
- `/ps-get-channels`: Get all notification channels

## Important Notes

- The bot uses a `app_database.json` file to store configuration data such as banned brands, scrape links, and
  notification channels.
- Product price history is stored in `latest_price_db.json`.
- The scraper respects rate limits and uses a delay between requests to avoid overwhelming the Perfume Shop API.
- Make sure to keep your `.env` file secure and never share your Discord bot token publicly.

## Files

- `discord_bot.py`: Main bot file containing Discord client and command handling
- `ApplicationDataManager.py`: Manages application data storage and retrieval
- `LatestPriceDataManager.py`: Handles storage and retrieval of latest product prices
- `scraper.py`: Contains the logic for scraping the Perfume Shop API
- `Logger.py`: Provides logging functionality for the application

## Customization

You can customize the bot's behavior by modifying the following:

- Scrape interval: Use the `/ps-set-interval` command to change how often the bot checks for updates
- Banned brands: Manage brands you don't want to track using the brand-related commands
- Scrape links: Add or remove category links to scrape using the link-related commands
- Notification channels: Control where the bot sends updates using the channel-related commands

## License

This project is licensed under the MIT License - see the LICENSE file for details.