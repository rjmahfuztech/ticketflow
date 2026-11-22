from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Ticket(TimeStampedModel):
    # category choices
    BILLING = "billing"
    TECHNICAL = "technical"
    ACCOUNT = "account"
    OTHER = "other"

    CATEGORY_CHOICES = [
        (BILLING, "Billing"),
        (TECHNICAL, "Technical"),
        (ACCOUNT, "Account"),
        (OTHER, "Other"),
    ]

    # priority choices
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

    PRIORITY_CHOICES = [
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
        (URGENT, "Urgent"),
    ]

    # status choices
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

    STATUS_CHOICES = [
        (OPEN, "Open"),
        (IN_PROGRESS, "In Progress"),
        (RESOLVED, "Resolved"),
        (CLOSED, "Closed"),
    ]

    reference = models.CharField(
        max_length=20, unique=True, null=True, blank=True, editable=False
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES, default=OTHER)
    priority = models.CharField(max_length=12, choices=PRIORITY_CHOICES, default=MEDIUM)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=OPEN)
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

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["status", "priority"], name="ticket_status_priority_idx"
            ),
            models.Index(
                fields=["assigned_to", "status"], name="ticket_assignee_status_idx"
            ),
            models.Index(
                fields=["created_by", "status"], name="ticket_creator_status_idx"
            ),
        ]

    def __str__(self):
        return self.reference or self.title
