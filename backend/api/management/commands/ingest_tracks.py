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
        """Processes a single chunk of the CSV data using bulk operations."""
        # Initialize data in memory
        tracks_to_create = []
        features_data_map = {} # spotify_id -> features_data
        seen_spotify_ids = set()

        # Prepare data in memory
        for _, row in chunk.iterrows():
            try:
                # Prepare Track data
                track_data = {model_field: row[csv_col] for csv_col, model_field in self.TRACK_MAP.items()}
                spotify_id = track_data.pop('spotify_id')

                # Deduplicate within the same chunk
                if spotify_id in seen_spotify_ids:
                    continue
                seen_spotify_ids.add(spotify_id)

                track = Track(spotify_id=spotify_id, **track_data)
                tracks_to_create.append(track)

                # Prepare & Validate AudioFeatures data
                features_data = {}
                for csv_col, model_field in self.FEATURES_MAP.items():
                    val = row[csv_col]
                    # Clamp values between 0.0 and 1.0 for specific features
                    if model_field in ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'speechiness']:
                        val = max(0.0, min(1.0, float(val)))
                    features_data[model_field] = val
                
                features_data_map[spotify_id] = features_data

            except Exception as e:
                stats['errors'] += 1
                self.stdout.write(self.style.WARNING(f"Error preparing track {row.get('track_id', 'unknown')}: {str(e)}"))

        if not tracks_to_create:
            return

        # Massive insertions (bulk upsert) are performed in a single transaction
        try:
            with transaction.atomic():
                # Bulk Upsert Tracks
                Track.objects.bulk_create(
                    tracks_to_create,
                    update_conflicts=True, # If a conflict is found, update the existing record
                    unique_fields=['spotify_id'],
                    update_fields=['title', 'artist_name', 'album_name']
                )
                
                # Update stats (We can't easily differentiate created vs updated with bulk_create)
                stats['created'] += len(tracks_to_create)

                # Retrieve Track IDs to be used for AudioFeatures bulk upsert
                spotify_ids = list(features_data_map.keys())
                tracks_db = Track.objects.filter(spotify_id__in=spotify_ids)
                
                # Bulk Upsert AudioFeatures
                features_to_create = []
                for track_db in tracks_db:
                    f_data = features_data_map[track_db.spotify_id]
                    features_to_create.append(AudioFeatures(track=track_db, **f_data))
                
                if features_to_create:
                    AudioFeatures.objects.bulk_create(
                        features_to_create,
                        update_conflicts=True,
                        unique_fields=['track'],
                        update_fields=list(self.FEATURES_MAP.values())
                    )
                    
        except Exception as e:
            stats['errors'] += len(tracks_to_create)
            self.stdout.write(self.style.ERROR(f"Error during bulk save: {str(e)}"))
