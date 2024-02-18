from datetime import timedelta

from django.contrib import admin
from harmony.events.models import Event, Tags


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "get_date", "get_time", "location", "type", "organizer")
    search_fields = ("title", "get_date", "get_time", "location", "type", "organizer")

    # date and time fields do not exist, so we need to add them using methods
    def get_date(self, obj):
        date_time = obj.date
        # add 5.5 hours to get the correct time
        date_time = date_time.replace(tzinfo=None)
        date_time = date_time + timedelta(hours=5, minutes=30)
        return date_time.strftime("%Y-%m-%d")
    get_date.short_description = "Date"

    def get_time(self, obj):
        date_time = obj.date
        # add 5.5 hours to get the correct time
        date_time = date_time.replace(tzinfo=None)
        date_time = date_time + timedelta(hours=5, minutes=30)
        return date_time.strftime("%H:%M")
    get_time.short_description = "Time"


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    search_fields = ("name",)
