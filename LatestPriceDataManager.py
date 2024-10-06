import json
from typing import Dict, List, Tuple
from Logger import Logger


class LatestPriceDataManager:
    def __init__(self):
        self.filename = 'latest_price_db.json'
        self.data: Dict[str, float] = self.init()

    def init(self) -> Dict[str, float]:
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
        except Exception as error:
            Logger.error('Error in LatestPriceDataManager:', error)
            raise

    def __save(self) -> None:
        Logger.info(f"Saving data to {self.filename}")
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.data, file, indent=2)
            Logger.info(f"Successfully saved {len(self.data)} price entries to {self.filename}")
        except IOError as error:
            Logger.error('Error saving data in LatestPriceDataManager:', error)
            raise

    def get_value(self, key: str) -> float:
        value = self.data.get(key)
        if value is None:
            Logger.warn(f"No price found for key {key}")
        return value

    def set_multiple_values(self, key_value_pairs: List[Tuple[str, float]]) -> None:
        Logger.info(f"Setting {len(key_value_pairs)} price entries")
        updated_count = 0
        for key, value in key_value_pairs:
            try:
                float_value = float(value)  # Validate float
                self.data[key] = float_value
                updated_count += 1
            except ValueError:
                Logger.error(f"Invalid price value: Key {key}, Price {value}")

        self.__save()
