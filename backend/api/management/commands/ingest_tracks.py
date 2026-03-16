import pandas as pd
import time
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Track, AudioFeatures

class Command(BaseCommand):
    help = 'Ingests Spotify track data from a CSV file into the database'

    # Mappings from CSV columns to Model fields
    TRACK_MAP = {
        'track_id': 'spotify_id',
        'track_name': 'title',
        'track_artist': 'artist_name',
        'track_album_name': 'album_name',
    }

    FEATURES_MAP = {
        'danceability': 'danceability',
        'energy': 'energy',
        'valence': 'valence',
        'tempo': 'tempo',
        'acousticness': 'acousticness',
        'instrumentalness': 'instrumentalness',
        'loudness': 'loudness',
        'speechiness': 'speechiness',
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='backend/data/spotify_songs_dataset.csv',
            help='Path to the CSV file'
        )
        parser.add_argument(
            '--chunksize',
            type=int,
            default=1000,
            help='Number of rows to process per chunk'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        chunk_size = options['chunksize']
        start_time_dt = timezone.localtime(timezone.now())
        
        start_msg = f"Starting Ingestion from {file_path} at {start_time_dt.strftime('%Y-%m-%d %H:%M:%S')}"
        self.stdout.write(self.style.SUCCESS(start_msg))
        self.log_to_file(start_msg)

        stats = {'created': 0, 'updated': 0, 'errors': 0}

        try:
            # Read CSV in chunks for memory efficiency
            chunk_idx = 1
            for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                chunk_start_time = time.time()
                self.process_chunk(chunk, stats)
                chunk_duration = time.time() - chunk_start_time
                
                chunk_msg = (
                    f"Processed chunk {chunk_idx}. Duration: {chunk_duration:.2f}s. "
                    f"Total: Created={stats['created']}, Updated={stats['updated']}, Errors={stats['errors']}"
                )
                self.stdout.write(chunk_msg)
                self.log_to_file(chunk_msg)
                chunk_idx += 1

            end_msg = f"Ingestion completed! Created: {stats['created']}, Updated: {stats['updated']}, Errors: {stats['errors']}"
            self.stdout.write(self.style.SUCCESS(end_msg))
            self.log_to_file(end_msg)

        except FileNotFoundError:
            err_msg = f'File not found: {file_path}'
            self.stdout.write(self.style.ERROR(err_msg))
            self.log_to_file(err_msg)
        except Exception as e:
            err_msg = f'An error occurred: {str(e)}'
            self.stdout.write(self.style.ERROR(err_msg))
            self.log_to_file(err_msg)

    def log_to_file(self, message):
        """Appends a message to the ingestion_log.txt file."""
        now = timezone.localtime(timezone.now())
        with open('ingestion_log.txt', 'a') as f:
            f.write(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

    def process_chunk(self, chunk, stats):
        """Processes a single chunk of the CSV data."""
        for _, row in chunk.iterrows():
            try:
                with transaction.atomic():
                    # Prepare Track data
                    track_data = {model_field: row[csv_col] for csv_col, model_field in self.TRACK_MAP.items()}
                    spotify_id = track_data.pop('spotify_id')

                    # Upsert 'Track' using Django ORM
                    track, created = Track.objects.update_or_create(
                        spotify_id=spotify_id,
                        defaults=track_data
                    )

                    if created:
                        stats['created'] += 1
                    else:
                        stats['updated'] += 1

                    # Prepare & Validate AudioFeatures data
                    features_data = {}
                    for csv_col, model_field in self.FEATURES_MAP.items():
                        val = row[csv_col]
                        # Clamp values between 0.0 and 1.0 for specific features
                        if model_field in ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'speechiness']:
                            val = max(0.0, min(1.0, float(val)))
                        features_data[model_field] = val

                    # Upsert 'AudioFeatures' using Django ORM (1:1 relationship)
                    AudioFeatures.objects.update_or_create(
                        track=track,
                        defaults=features_data
                    )

            except Exception as e:
                stats['errors'] += 1
                self.stdout.write(self.style.WARNING(f"Error processing track {row.get('track_id', 'unknown')}: {str(e)}"))
