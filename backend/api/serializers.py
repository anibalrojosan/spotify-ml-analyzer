from rest_framework import serializers
from api.models import UserProfile, UserArchetype

class ArchetypeSerializer(serializers.ModelSerializer):
    """
    Serializer for UserArchetype model to expose basic details.
    """
    class Meta:
        model = UserArchetype
        fields = ['name', 'display_name', 'description']

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model with a mock avatar and nested archetype.
    """
    avatar_url = serializers.SerializerMethodField()
    archetype = ArchetypeSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['spotify_id', 'display_name', 'avatar_url', 'archetype']

    def get_avatar_url(self, obj):
        """
        Generates a mock avatar URL using DiceBear API with spotify_id as seed.
        """
        return f"https://api.dicebear.com/7.x/avataaars/svg?seed={obj.spotify_id}"
