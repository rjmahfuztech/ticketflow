from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Ticket(TimeStampedModel):
    # category choices
    BILLING = "B"
    TECHNICAL = "T"
    ACCOUNT = "A"
    OTHER = "O"

    CATEGORY_CHOICES = [
        (BILLING, "Billing"),
        (TECHNICAL, "Technical"),
        (ACCOUNT, "Account"),
        (OTHER, "Other"),
    ]

    # priority choices
    LOW = "L"
    MEDIUM = "M"
    HIGH = "H"
    URGENT = "U"

    PRIORITY_CHOICES = [
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
        (URGENT, "Urgent"),
    ]

    # status choices
    OPEN = ("O",)
    IN_PROGRESS = "P"
    RESOLVED = "R"
    CLOSED = "C"

    STATUS_CHOICES = [
        (OPEN, "Open"),
        (IN_PROGRESS, "In Progress"),
        (RESOLVED, "Resolved"),
        (CLOSED, "Closed"),
    ]

    reference = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default=OTHER)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default=MEDIUM)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=OPEN)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="tickets_created",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets_assigned",
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
