from datetime import UTC, datetime
from django.utils.timezone import localtime
from django.db import models


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_duration(self):
        entered_at = localtime(self.entered_at)
        if self.leaved_at == None:
            leaved_at = localtime(datetime.now(UTC))
        else:
            leaved_at = localtime(self.leaved_at)
        duration = leaved_at - entered_at
        total_seconds = duration.total_seconds()
        return total_seconds

    def format_duration(self, duration):
        seconds = int(duration % 60)
        minutes = int((duration % 3600) // 60)
        hours = int((duration % 86400) // 3600)
        days = int(duration // 86400)

        time_parts = [
            (days, 'дней'),
            (hours, 'ч'),
            (minutes, 'мин'),
            (seconds, 'сек')
        ]

        time_str = ' '.join(f'{value}{unit}' for value, unit in time_parts if value > 0)
        return time_str


    def is_strange(self):
        return self.get_duration() > 3600
