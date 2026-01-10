import os
import pandas as pd
from django.conf import settings
import logging

# Set a logger to check in console
logger = logging.getLogger(__name__)

class SpotifyDataLoader:
    """
    Singleton class to load the Spotify CSV dataset into memory efficiently.
    This prevents reading from the disk on every API request.
    """
    _instance = None
    _dataframe = None

    def __new__(cls): # Singleton Pattern
        if cls._instance is None:
            cls._instance = super(SpotifyDataLoader, cls).__new__(cls)
        return cls._instance

    def load_data(self): 
        """
        Loads the CSV file specified in settings if not already loaded.
        Returns the Pandas DataFrame.
        """
        if self._dataframe is not None:  # Lazy Loading
            return self._dataframe       # This variable acts as cache

        csv_path = os.path.join(settings.BASE_DIR, 'data', 'cleaned_dataset.csv')

        if not os.path.exists(csv_path):
            logger.error(f"Dataset not found at: {csv_path}")
            raise FileNotFoundError(f"CSV Dataset not found at {csv_path}. Check the correct route.")

        try:
            logger.info(f"Loading Spotify Dataset from: {csv_path}...")
            
            df = pd.read_csv(csv_path)
            
            # Here an optimization can be done (e.g. convert numeric columns if necessary, delete columns not used to save RAM)
            # For now all is loaded.
            
            self._dataframe = df
            logger.info(f"Dataset loaded successfully! Shape: {df.shape}")
            return self._dataframe

        except Exception as e:
            logger.error(f"Error loading CSV: {str(e)}")
            raise e

    def get_random_sample(self, n=5):
        """
        Helper method to get random tracks for simulation.
        """
        if self._dataframe is None:
            self.load_data()

        # make the df to look like a JSON using orient='records'
        # necessary for communication with APIs
        return self._dataframe.sample(n).to_dict(orient='records')


data_loader = SpotifyDataLoader()