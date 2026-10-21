from django.core.exceptions import ValidationError
from django.db import models

from members.models import Member


class Payment(models.Model):
    """An advance / partial payment a member makes towards the mess bill."""

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="payments"
    )
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.member} paid {self.amount} on {self.date}"

    def clean(self):
        if self.amount is not None and self.amount <= 0:
            raise ValidationError("Payment amount must be greater than zero.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
