from rest_framework import serializers
from harmony.events.models import Event, Tags
from harmony.users.models import User


class TagsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tags model.
    """

    class Meta:
        model = Tags
        fields = [
            "id",
            "name",
        ]


class EventListSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model.
    """
    title = serializers.CharField(required=True)

    # name of organizer if community or first_name and last_name if member
    organizer = serializers.SerializerMethodField()

    # count of users applied for the event
    attendees_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "organizer",
            "attendees_count",
        ]

    def get_organizer(self, obj):
        if obj.organizer.type == "COM":
            return obj.organizer.community.name
        else:
            return f"{obj.organizer.member.first_name} {obj.organizer.member.last_name}"

    def get_attendees_count(self, obj):
        return obj.attendees.count()


class EventDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model.
    """
    organizer = serializers.SerializerMethodField()
    attendees_count = serializers.SerializerMethodField()
    attendees = serializers.SerializerMethodField()
    # tags = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "date",
            "time",
            "location",
            "type",
            "organizer",
            "attendees_count",
            "attendees",
            # "tags",
            "duration"
        ]

    def get_organizer(self, obj):
        if obj.organizer.type == "COM":
            return obj.organizer.community.name
        else:
            return f"{obj.organizer.member.first_name} {obj.organizer.member.last_name}"

    def get_attendees_count(self, obj):
        return obj.attendees.count()

    def get_attendees(self, obj):
        """
        return user ids of attendees
        """
        return [attendee.id for attendee in obj.attendees.all()]

    # def get_tags(self, obj):
    #     """
    #     return tags of the event
    #     """
    #     return [tag.name for tag in obj.tags.all()]

    def get_date(self, obj):
        return obj.date.strftime("%Y-%m-%d")

    def get_time(self, obj):
        return obj.date.strftime("%H:%M")


class EventCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model.
    """
    # set organizer as logged in user
    organizer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    # tags should be selectable from existing tags, or can be added as well if not present.
    # This is handled by a serializer method field
    date = serializers.DateField(write_only=True)
    time = serializers.TimeField(write_only=True)
    # tags = TagsSerializer(many=True, required=False)


    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "date",
            "time",
            "location",
            "type",
            "organizer",
            # "tags",
            "duration"
        ]

    def get_time(self, obj):
        return obj.date.strftime("%H:%M")

    def get_date(self, obj):
        return obj.date.strftime("%Y-%m-%d")

    # we need to take time and date separately and then combine them to create a datetime object
    # def create(self, validated_data):
    #     time = validated_data.pop("time")
    #     date = validated_data.pop("date")
    #     tags_data = validated_data.pop("tags", [])
    #     # create a datetime object
    #     validated_data["date"] = f"{date} {time}"
    #     event = Event.objects.create(**validated_data)
    #     # add the tags using set method
    #     for tag in tags_data:
    #         tag, created = Tags.objects.get_or_create(name=tag)
    #         print(tag)
    #         event.tags.add(tag)
    #
    #     return event

    #skipping tags for now
    def create(self, validated_data):
        time = validated_data.pop("time")
        date = validated_data.pop("date")
        validated_data["date"] = f"{date} {time}"
        event = Event.objects.create(**validated_data)
        return event
