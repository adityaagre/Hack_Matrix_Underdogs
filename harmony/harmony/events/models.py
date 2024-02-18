from django.db import models
from harmony.users.models import User


class Event(models.Model):
    """
    Class for Event model
    Events cover all activities that are conducted by the organization
    We use types for events (e.g. meetings, workshops, etc.)
    """

    class EventType(models.TextChoices):
        """
        Class for Event Types
        """
        MEETING = "MEETING", "Meeting"
        WORKSHOP = "WORKSHOP", "Workshop"
        CONFERENCE = "CONFERENCE", "Conference"
        SEMINAR = "SEMINAR", "Seminar"
        RECRUITMENT = "RECRUITMENT", "Recruitment"
        OTHER = "OTHER", "Other"

    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=15, choices=EventType.choices, default=EventType.OTHER)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    attendees = models.ManyToManyField(User, related_name="attendees", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField("Tags", related_name="events", blank=True)
    duration = models.DurationField(blank=True, null=True)

    def __str__(self):
        if self.organizer.type == "COMMUNITY":
            return f"{self.title} by {self.organizer.community.name}"
        else:
            return f"{self.title} by {self.organizer.member.first_name} {self.organizer.member.last_name}"

    class Meta:
        verbose_name_plural = "events"
        verbose_name = "event"
        ordering = ["-date"]

    # def get_absolute_url(self):
    #     """
    #     Get URL for event's detail view.
    #     :return:
    #     """
    #     return reverse("events:detail", kwargs={"pk": self.pk})


class Tags(models.Model):
    """
    Class for Tags model
    Tags are labels for events, communities as well as used when member selects interests
    Only to be used in many-to-many relationships
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "tags"
        verbose_name = "tag"
        ordering = ["name"]
