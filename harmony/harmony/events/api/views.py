from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from harmony.events.api.serializers import EventListSerializer, EventCreateSerializer, EventDetailSerializer
from harmony.users.models import Member, Community
from harmony.events.models import Event
from harmony.utils.response import response_payload

User = get_user_model()


class EventListAPIView(ListAPIView):
    """
    This class represents the list view for events.
    Authentication is required for this view.
    """

    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    permission_classes = [
        AllowAny,
    ]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = [
        "title",
        "description",
        "location",
        "tags__name"
    ]
    ordering_fields = [
        "title",
        "date"
    ]
    filterset_fields = [
        "title",
        "date",
        "location",
        "tags__name"

    ]
    ordering = ["-date"]

    def get(self, request, *args, **kwargs):
        """
        This function returns a list of events.
        """
        try:
            request = self.request
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = EventListSerializer(page, many=True, context={"request": request})
                response =  self.get_paginated_response(serializer.data)
                response.data = response_payload(
                    success=True,
                    message="Events list fetched",
                    data=response.data
                )
                response.status_code = status.HTTP_200_OK

                return response
            serializer = EventListSerializer(queryset, many=True, context={"request": request})
            response = response_payload(
                success=True,
                message="Events list fetched",
                data=serializer.data
            )
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = response_payload(
                success=False,
                message="Failed to fetch events list",
                data=str(e)
            )
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



class EventDetailAPIView(RetrieveAPIView):
    """
    This class represents the detail view for events.
    Authentication is required for this view.
    """

    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    lookup_field = "id"
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        """
        This function returns a single event.
        """
        try:
            event = self.get_object()
            serializer = EventDetailSerializer(event, context={"request": request})
            response = response_payload(
                success=True,
                message="Event fetched",
                data=serializer.data
            )
            return Response(response, status=status.HTTP_200_OK)
        except Http404:
            response = response_payload(
                success=False,
                message="Event not found",
                data=None
            )
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class EventCreateAPIView(CreateAPIView):
    """
    This class represents the create view for events.
    Authentication is required for this view.

    """

    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def create(self, request, *args, **kwargs):
        """
        This function creates an event.
        """
        serializer = EventCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            response = response_payload(
                success=True,
                message="Event created",
                data=serializer.data
            )
            return Response(response, status=status.HTTP_201_CREATED)
        response = response_payload(
            success=False,
            message="Failed to create event",
            data=serializer.errors
        )
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
