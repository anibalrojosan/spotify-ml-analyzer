from rest_framework import authentication
from api.models import UserProfile

class MockSessionAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class for DRF that uses the Django session
    to identify a mock user and populate request.user.
    """
    def authenticate(self, request):
        user_id = request.session.get('user_id')
        
        if not user_id:
            return None

        try:
            user = UserProfile.objects.get(spotify_id=user_id)
        except UserProfile.DoesNotExist:
            # If the session has a user_id that doesn't exist in the DB,
            # treat it as unauthenticated.
            return None

        # Return a tuple of (user, auth)
        # auth is usually None for session-based authentication
        return (user, None)
