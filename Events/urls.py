from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('events', EventViewSet, base_name='events')

urlpatterns = [

    path("events/<int:pk>/images/", ImageList.as_view(), name="event_list"),
    path("events/<int:pk>/images/<int:image_pk>/vote/",
         CreateVote.as_view(), name="event_list"),
    path("events/<int:pk>/attendees/", AttendeeList.as_view(), name="event_list"),
    path("events/<int:pk>/attendee/", AttendeeUpdate.as_view(), name="event_list"),

]

urlpatterns += router.urls
