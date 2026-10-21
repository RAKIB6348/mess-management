"""Monthly mess bill calculation.

meal_rate = total_bazaar_expense / total_meals
member_share = member_meals * meal_rate
"""

from calendar import monthrange
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Sum

from bazaar.models import Expense
from meals.models import Meal
from members.models import Member
from billing.models import Payment


@dataclass
class MemberBill:
    member: Member
    meals: int = 0
    share: Decimal = Decimal("0.00")
    paid: Decimal = Decimal("0.00")

    @property
    def due(self) -> Decimal:
        return (self.share - self.paid).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )


@dataclass
class BillSummary:
    year: int
    month: int
    members: list = field(default_factory=list)
    total_meals: int = 0
    total_expense: Decimal = Decimal("0.00")
    total_paid: Decimal = Decimal("0.00")
    meal_rate: Decimal = Decimal("0.00")

    @property
    def total_share(self) -> Decimal:
        return sum((m.share for m in self.members), Decimal("0.00"))

    @property
    def total_due(self) -> Decimal:
        return sum((m.due for m in self.members), Decimal("0.00"))


def month_bounds(year: int, month: int) -> tuple[date, date]:
    last_day = monthrange(year, month)[1]
    return date(year, month, 1), date(year, month, last_day)


def calculate_bill(year: int, month: int) -> BillSummary:
    start, end = month_bounds(year, month)

    members = list(Member.objects.filter(status=Member.Status.ACTIVE))
    summary = BillSummary(year=year, month=month)

    # Expenses in the period.
    expense_total = (
        Expense.objects.filter(date__range=(start, end)).aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0.00")
    )
    summary.total_expense = expense_total

    # Payments in the period.
    paid_total = (
        Payment.objects.filter(date__range=(start, end)).aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0.00")
    )
    summary.total_paid = paid_total

    # Meals per member in the period.
    meal_rows = (
        Meal.objects.filter(date__range=(start, end))
        .values("member_id")
        .annotate(total=Sum("count"))
    )
    meals_by_member = {row["member_id"]: row["total"] for row in meal_rows}
    summary.total_meals = sum(meals_by_member.values())

    # Payments per member in the period.
    payment_rows = (
        Payment.objects.filter(date__range=(start, end))
        .values("member_id")
        .annotate(total=Sum("amount"))
    )
    paid_by_member = {row["member_id"]: row["total"] for row in payment_rows}

    if summary.total_meals > 0:
        summary.meal_rate = (
            summary.total_expense / Decimal(summary.total_meals)
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    for member in members:
        member_meals = meals_by_member.get(member.id, 0)
        share = (Decimal(member_meals) * summary.meal_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        summary.members.append(
            MemberBill(
                member=member,
                meals=member_meals,
                share=share,
                paid=paid_by_member.get(member.id, Decimal("0.00")),
            )
        )

    return summary
