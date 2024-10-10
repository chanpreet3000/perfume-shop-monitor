import json
from typing import Set
from Logger import Logger


class ApplicationDataManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApplicationDataManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        Logger.info("Initializing ApplicationDataManager")
        self.filename = 'app_database.json'
        self.banned_brands: Set[str] = set()
        self.cycle_interval: int = 60
        self.links_to_scrape: Set[str] = set()
        self.notification_channels: Set[str] = set()
        self._load_data()

    def _load_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.banned_brands = set(data.get('banned_brands', []))
                self.cycle_interval = data.get('cycle_interval', 60)
                self.links_to_scrape = set(data.get('links_to_scrape', []))
                self.notification_channels = set(data.get('notification_channels', []))

            Logger.info("ApplicationDataManager initialized successfully", {
                'banned_brands': list(self.banned_brands),
                'cycle_interval': self.cycle_interval,
                'links_to_scrape': list(self.links_to_scrape),
                'notification_channels': list(self.notification_channels)
            })
        except FileNotFoundError:
            Logger.warn(f"Database file {self.filename} not found. Initializing with default values.")
        except json.JSONDecodeError as error:
            Logger.error('Error loading data:', error)
            raise

    def save(self):
        Logger.info("Saving data to file")
        try:
            with open(self.filename, 'w') as file:
                json.dump({
                    'banned_brands': list(self.banned_brands),
                    'cycle_interval': self.cycle_interval,
                    'links_to_scrape': list(self.links_to_scrape),
                    'notification_channels': list(self.notification_channels)
                }, file, indent=2)
        except IOError as error:
            Logger.error('Error saving data:', error)
            raise

    # Banned brands methods
    def add_banned_brand(self, brand: str):
        Logger.info(f"Adding banned brand: {brand}")
        self.banned_brands.add(brand)
        self.save()

    def remove_banned_brand(self, brand: str):
        Logger.info(f"Removing banned brand: {brand}")
        self.banned_brands.discard(brand)
        self.save()

    def get_all_banned_brands(self) -> Set[str]:
        return self.banned_brands

    # Links to scrape methods
    def add_link_to_scrape(self, link: str):
        Logger.info(f"Adding link to scrape: {link}")
        self.links_to_scrape.add(link)
        self.save()

    def remove_link_to_scrape(self, link: str):
        Logger.info(f"Removing link to scrape: {link}")
        self.links_to_scrape.discard(link)
        self.save()

    def get_all_links_to_scrape(self) -> Set[str]:
        return self.links_to_scrape

    # Notification channels methods
    def add_notification_channel(self, channel: str):
        Logger.info(f"Adding notification channel: {channel}")
        self.notification_channels.add(channel)
        self.save()

    def remove_notification_channel(self, channel: str):
        Logger.info(f"Removing notification channel: {channel}")
        self.notification_channels.discard(channel)
        self.save()

    def get_all_notification_channels(self) -> Set[str]:
        return self.notification_channels
