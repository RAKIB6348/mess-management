from django.core.exceptions import ValidationError
from django.db import models

from members.models import Member


class Meal(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="meals"
    )
    date = models.DateField()
    count = models.PositiveIntegerField(default=1)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-date", "member__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["member", "date"], name="unique_meal_per_member_per_day"
            )
        ]

    def __str__(self):
        return f"{self.member} - {self.date} ({self.count})"

    def clean(self):
        if self.count < 1:
            raise ValidationError("Meal count must be at least 1.")
        if not self.member.is_active:
            raise ValidationError(
                "Cannot record meals for an inactive member."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
