from django.core.management.base import BaseCommand
from api.models import UserArchetype

class Command(BaseCommand):
    help = 'Seeds the database with the 5 K-Means User Archetypes'

    def handle(self, *args, **options):
        archetypes = [
            {
                "name": "the-organic-relaxed",
                "display_name": "The Organic / Relaxed",
                "description": "User seeks calmness, disconnection, or focus. Prefers natural sounds over synthesized production.",
                "min_values": {"acousticness": 0.5, "energy": 0.0},
                "max_values": {"acousticness": 1.0, "energy": 0.5}
            },
            {
                "name": "the-euphoric-social",
                "display_name": "The Euphoric / Social",
                "description": "User seeks dopamine and social connection. Prefers music that is explicitly happy and danceable.",
                "min_values": {"valence": 0.65, "danceability": 0.65},
                "max_values": {"valence": 1.0, "danceability": 1.0}
            },
            {
                "name": "the-high-intensity",
                "display_name": "The High Intensity",
                "description": "User seeks adrenaline and power. Prefers fast, aggressive, or heavy music.",
                "min_values": {"tempo": 130.0, "energy": 0.75},
                "max_values": {"tempo": 250.0, "energy": 1.0}
            },
            {
                "name": "the-rhythmic-flow",
                "display_name": "The Rhythmic Flow",
                "description": "User seeks momentum and consistency. Prefers the steady 120-128 BPM range that maintains a Flow State.",
                "min_values": {"tempo": 115.0, "energy": 0.6},
                "max_values": {"tempo": 130.0, "energy": 0.8}
            },
            {
                "name": "the-mainstream-groove",
                "display_name": "The Mainstream Groove",
                "description": "User seeks accessibility and balance. Prefers polished, radio-friendly structures with a good groove.",
                "min_values": {"danceability": 0.6, "energy": 0.5},
                "max_values": {"danceability": 0.8, "energy": 0.75}
            }
        ]

        for arch_data in archetypes:
            # obj: saved archetype object
            # created: boolean indicating if the archetype was created or updated
            obj, created = UserArchetype.objects.update_or_create(
                name=arch_data["name"],
                defaults=arch_data
            )
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f'{action} archetype: {obj.display_name}'))
