import datetime

from rest_framework import generics, status, permissions
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from Authentication import models
from Authentication.models import Account
from .serializer import *


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        date_created = datetime.datetime.now()
        event_name = request.data.get("event_name")
        is_active = "True"
        has_happened = "False"
        date_of_event = request.data.get("date_of_event")
        created_by = Account.objects.get(pk=request.user.pk).pk

        data = {
            "date_created": date_created,
            "event_name": event_name,
            "is_active": is_active,
            "has_happened": has_happened,
            "date_of_event": date_of_event,
            "created_by": created_by
        }
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            event = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendeeList(generics.ListCreateAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Attendee.objects.filter(event_id=self.kwargs["pk"])
        return queryset

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs["pk"])

        if request.user == event.created_by:
            event = event
            user = request.data.get("user")
            is_going = request.data.get("is_going", "False")
            date_joined = datetime.datetime.now()
        elif request.user == Attendee.objects.get(pk=self.kwargs["pk"]).user:
            attendee = Attendee.objects.get(pk=self.kwargs["pk"]).user
            event = attendee.event
            user = attendee.user
            is_going = request.data.get("is_going")
            date_joined = datetime.datetime.now()
        else:
            raise PermissionDenied("you cannot add or modify attendees to this event")

        data = {
            "event": event.pk,
            "user": user,
            "is_going": is_going,
            "date_joined": date_joined

        }
        serializer = AttendeeSerializer(data=data)
        if serializer.is_valid():
            attendee = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendeeUpdate(generics.UpdateAPIView):
    serializer_class = AttendeeSerializer
    queryset = Attendee.objects.all()

    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        partial=True
        instance = self.get_object()
        event = Event.objects.get(pk=self.kwargs["pk"])

        user = Account.objects.get(pk=request.user.pk)
        is_going = request.data.get("is_going")
        date_joined = datetime.datetime.now()
        attendee = Attendee.objects.get(user=user.pk, event=event.pk)
        data = {
            "id": attendee.pk,
            "is_going": is_going,
            "date_joined": date_joined

        }
        serializer = self.get_serializer(instance, data=data, partial=partial)
        if serializer.is_valid():
            attendee = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageList(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Image.objects.filter(event_id=self.kwargs["pk"])
        return queryset

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs["pk"])

        if not request.user == event.created_by:
            raise PermissionDenied("you cannot add images to this event")
        image = request.data.get("image")
        image_event = event.pk
        data = {'image': image, 'event': image_event}
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            image = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateVote(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk, image_pk):
        voted_by = request.user.mobile
        data = {'image': image_pk, 'event': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        # attendees = Attendee.objects.get(pk=self.kwargs["pk"])
        # access = False
        # for attendee in attendees:
        # if request.user == attendee:
        # access = True
        # if not access:
        # raise PermissionError("you cannot vote here")
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
