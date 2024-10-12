import json
from typing import Dict, List, Tuple, Optional
from Logger import Logger


class LatestPriceDataManager:
    def __init__(self):
        self.filename = 'latest_price_db.json'
        self.data: Dict[str, float] = self._init()

    def _init(self) -> Dict[str, float]:
        Logger.info("Initializing LatestPriceDataManager")
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                validated_data = {
                    key: float(value)
                    for key, value in data.items()
                }
                Logger.info(f"Loaded {len(validated_data)} price entries from {self.filename}")
                return validated_data
        except FileNotFoundError:
            Logger.warn(f"Database file {self.filename} not found. Initializing with empty data.")
            return {}
        except json.JSONDecodeError as error:
            Logger.error(f'Error decoding JSON in {self.filename}:', error)
            raise
        except Exception as error:
            Logger.error('Unexpected error in LatestPriceDataManager:', error)
            raise

    def _save(self) -> None:
        Logger.info(f"Saving data to {self.filename}")
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.data, file, indent=2)
            Logger.info(f"Successfully saved {len(self.data)} price entries to {self.filename}")
        except IOError as error:
            Logger.error('Error saving data in LatestPriceDataManager:', error)
            raise

    def get_value(self, key: str) -> Optional[float]:
        value = self.data.get(str(key))
        if value is None:
            Logger.warn(f"No price found for key {key}")
        return value

    def set_multiple_values(self, key_value_pairs: List[Tuple[str, float]]) -> None:
        Logger.info(f"Setting {len(key_value_pairs)} price entries")
        updated_count = 0
        for key, value in key_value_pairs:
            Logger.info(f"Setting price for {key} to {value}")
            self.data[key] = value
            updated_count += 1
            Logger.info(f"Price for {key} to ", self.data[key])
        Logger.info(f"Successfully set {updated_count} price entries")
        self._save()
