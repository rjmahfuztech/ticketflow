from django.conf import settings
from django.db import models

from core.models import TimeStampedModel
from tickets.models import Comment, Ticket

MAX_ATTACHMENT_BYTES = 5 * 1024 * 1024  # 5 mb


class Attachment(TimeStampedModel):
    # resource_type choices
    IMAGE = "image"
    RAW = "raw"

    RESOURCE_TYPE_CHOICES = [(IMAGE, "Image"), (RAW, "Raw")]

    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="attachments"
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attachments",
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="attachments"
    )
    public_id = models.CharField(max_length=255, unique=True)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE_CHOICES)
    file_format = models.CharField(max_length=10)
    file_size = models.PositiveIntegerField()
    original_filename = models.CharField(max_length=255)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(
                fields=["ticket", "created_at"], name="attachment_ticket_created_idx"
            )
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(file_size__lte=MAX_ATTACHMENT_BYTES),
                name="attachment_bytes_max_5mb",
            )
        ]

    def __str__(self):
        return self.original_filename
