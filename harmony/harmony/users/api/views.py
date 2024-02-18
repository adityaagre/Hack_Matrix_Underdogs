from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from harmony.users.api.serializers import UserSerializer, MemberSerializer, CommunitySerializer
from harmony.users.models import Member, Community
from harmony.utils.response import response_payload

User = get_user_model()


class UserListView(ListAPIView):
    """
    This class represents the list view for users.
    Authentication is not required for this view.
    We can list members or communities using filters
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        AllowAny,
    ]
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        "type",
    ]
    search_fields = [
        "username",
        "email",
    ]
    ordering = ["-user__date_joined"]


    def get(self, request, *args, **kwargs):
        """
        This function returns a list of members.
        """
        try:
            request = self.request
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = UserSerializer(page, many=True, context={"request": request})
                response = self.get_paginated_response(serializer.data)
                # use response_payload to add success and message keys to the response
                response.data = response_payload(
                    success=True, data=response.data, message="Users fetched successfully"
                )
                # WARN: Explicit HTTP response code missing
                return response
            serializer = UserSerializer(queryset, many=True, context={"request": request})
            response = response_payload(success=True, data=serializer.data, message="Users fetched successfully")
            return Response(response, status=status.HTTP_200_OK)
        except Http404:
            return Response(
                response_payload(success=False, message="Users not found"),
                status=status.HTTP_404_NOT_FOUND,
            )


class MemberUpdateAPIView(UpdateAPIView):
    """
    This class represents the update view for members.
    Authentication is required for this view.
    Members can update their own details only.
    """

    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        user_id = self.request.user.id
        return Member.objects.get(user_id=user_id)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = MemberSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                response_payload(success=True, data=serializer.data, message="Member details updated successfully"),
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                response_payload(success=False, message="Member not found"),
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                response_payload(success=False, message=str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )


class CommunityUpdateView(UpdateAPIView):
    """
    This class represents the update view for communities.
    Authentication is required for this view.
    Communities can update their own details only.
    """

    queryset = Community.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        user_id = self.request.user.id
        return Community.objects.get(user_id=user_id)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = CommunitySerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                response_payload(success=True, data=serializer.data, message="Community details updated successfully"),
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                response_payload(success=False, message="Community not found"),
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                response_payload(success=False, message=str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )



# delete views pending
