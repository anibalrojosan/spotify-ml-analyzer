from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
import uuid
# from .utils.data_loader import data_loader

class MockAuthView(APIView):
    """
    Simulates Spotify OAuth.
    Allows passing an 'archetype_id' in the body to force a specific profile.
    """

    def post(self, request):
        # Define the 5 Archetypes (PRD Business Logic)
        ARCHETYPES = [
            {"id": 0, "name": "The Rhythmic Flow", "description": "Steady 120-128 BPM, House/Pop"},
            {"id": 1, "name": "The High Intensity", "description": "Fast, Aggressive, Metal/Gym"},
            {"id": 2, "name": "The Mainstream Groove", "description": "Radio-friendly, Danceable"},
            {"id": 3, "name": "The Organic / Relaxed", "description": "Acoustic, Low Energy"},
            {"id": 4, "name": "The Euphoric / Social", "description": "Happy, Party, High Valence"},
        ]

        # 2. LOGIC UPGRADE: Check parameters in 'request'
        # Buscamos si el frontend envió un ID específico, ej: { "archetype_id": 1 }
        requested_id = request.data.get('archetype_id')

        # Simulation: Every time we "Login", the system will pick a different profile
        # so we can test how the Frontend reacts to different data.        
        selected_archetype = None

        if requested_id is not None:
            # Search the requested ID
            selected_archetype = next((a for a in ARCHETYPES if a["id"] == int(requested_id)), None)
        
        # If the ID doesn't exist, we make a random choice
        if selected_archetype is None:
            selected_archetype = random.choice(ARCHETYPES)

        # Build the Mock User (mock of the Spotify API Structure)
        mock_user_profile = {
            "id": f"mock_user_{uuid.uuid4().hex[:8]}",
            "display_name": f"Test User ({selected_archetype['name']})",
            "email": "simulator@spotify-analyzer.local",
            "images": [{"url": "https://i.scdn.co/image/ab67616d0000b2736a", "height": 300, "width": 300}],
            
            # CRITICAL METADATA: Data Science results here            
            "app_metadata": {
                "archetype_id": selected_archetype['id'],
                "archetype_name": selected_archetype['name'],
                "role": "simulation_user"
            }
        }

        # Build the Mock Token
        mock_token = {
            "access_token": f"mock_token_{uuid.uuid4().hex}",
            "token_type": "Bearer",
            "expires_in": 3600,
        }

        # Final response
        return Response({
            "user": mock_user_profile,
            "auth": mock_token,
            "message": f"Login Successful. Loaded profile: {selected_archetype['name']}"
        }, status=status.HTTP_200_OK)