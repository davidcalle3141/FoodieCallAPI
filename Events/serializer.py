from rest_framework import serializers

from .models import *


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = (
            "image",
            "event",
            "voted_by",
        )


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = (
            "event",
            "user",
            "is_going",
            "date_joined",

        )


class ImageSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True,read_only=True, required=False)

    class Meta:
        model = Image
        fields = (
            "id",
            "event",
            "image",
            "votes",
        )


class EventSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True, required=False)
    attendees = AttendeeSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Event
        fields = (
            "id",
            "is_active",
            "has_happened",
            "date_of_event",
            "date_created",
            "event_name",
            "created_by",
            "images",
            "attendees",

        )
