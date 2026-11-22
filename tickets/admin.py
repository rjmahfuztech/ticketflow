from django.contrib import admin

from tickets.models import Comment, Ticket, TicketEvent

admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(TicketEvent)
