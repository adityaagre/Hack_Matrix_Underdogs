from django.urls import path
from harmony.events.api.views import EventListAPIView, EventDetailAPIView, EventCreateAPIView

app_name = "events"
urlpatterns = [
    path("", EventListAPIView.as_view(), name="event-list"),
    path("<int:id>/", EventDetailAPIView.as_view(), name="event-detail"),
    path("create/", EventCreateAPIView.as_view(), name="event-create"),

]
