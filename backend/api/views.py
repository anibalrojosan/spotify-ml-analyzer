import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import UserProfile, UserArchetype
from api.serializers import UserSerializer

class MockLoginView(APIView):
    """
    Endpoint to simulate user authentication and assign a UserArchetype.
    """
    def post(self, request):
        archetype_id = request.data.get('archetype_id')
        
        # 1. Get or assign an archetype
        if archetype_id:
            try:
                archetype = UserArchetype.objects.get(name=archetype_id)
            except UserArchetype.DoesNotExist:
                return Response(
                    {"error": f"Archetype '{archetype_id}' not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Pick a random archetype if none provided
            archetypes = UserArchetype.objects.all()
            if not archetypes.exists():
                return Response(
                    {"error": "No archetypes found in database. Run seed_archetypes first."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            archetype = random.choice(archetypes)

        # 2. Create or retrieve a mock user profile for this session
        mock_spotify_id = "mock_user_session"
        user, created = UserProfile.objects.update_or_create(
            spotify_id=mock_spotify_id,
            defaults={
                'display_name': 'Spotify Explorer',
                'archetype': archetype
            }
        )

        # 3. Store in session for persistence
        request.session['user_id'] = user.spotify_id
        request.session['archetype_id'] = archetype.name
        
        # Explicitly save session to ensure cookie is sent
        request.session.modified = True

        # 4. Return serialized user data
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
