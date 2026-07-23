from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.db.models import Q

from office.models import Appointment
from office.notifications import send_appointment_reminder


class Command(BaseCommand):
    help = 'send appointment reminders'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='do not actually send appointment reminders')

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        now = timezone.now()
        offsets = getattr(settings, 'APPOINTMENT_REMINDER_OFFSETS', [168, 24])

        sent_count = 0
        for offset in offsets:
            
            qs = Appointment.objects.filter(
                date_time__lte=now + timedelta(hours=offset),
                status='confirmed',
                #last_reminder_sent_at__lt=now - timedelta(hours=offset)   
                # OR last reminder is null
                Q(last_reminder_sent_at__lt=now = timedelta(hours=offset)) | Q(last_reminder_sent_at__isnull=True)
            )
            
            for appointment in qs:
                if send_appointment_reminder(appointment, offset, dry_run=dry_run):
                    sent_count += 1
                    if not dry_run:
                        appointment.last_reminder_sent_at = now
                        appointment.save(update_fields=['last_reminder_sent_at'])
            
        self.stdout.write(self.style.SUCCESS("sent {sent_count} notifications"))