from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from bazaar.models import Expense
from meals.models import Meal
from members.models import Member

from .forms import PaymentForm
from .models import Payment
from .services import calculate_bill


def parse_month(request, default=None):
    """Return (year, month) from ?month=YYYY-MM, else the current month."""
    raw = request.GET.get("month")
    if raw:
        try:
            parsed = datetime.strptime(raw, "%Y-%m").date()
            return parsed.year, parsed.month
        except ValueError:
            pass
    today = default or date.today()
    return today.year, today.month


@login_required
def dashboard(request):
    year, month = parse_month(request)

    members_count = Member.objects.filter(status=Member.Status.ACTIVE).count()
    meals_count = Meal.objects.filter(
        date__year=year, date__month=month
    ).count()
    meals_total = (
        Meal.objects.filter(date__year=year, date__month=month).aggregate(
            total=Sum("count")
        )["total"]
        or 0
    )
    expense_total = (
        Expense.objects.filter(date__year=year, date__month=month).aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    recent_meals = Meal.objects.select_related("member").all()[:10]
    recent_expenses = Expense.objects.select_related("paid_by").all()[:10]

    context = {
        "year": year,
        "month": month,
        "members_count": members_count,
        "meals_count": meals_count,
        "meals_total": meals_total,
        "expense_total": expense_total,
        "recent_meals": recent_meals,
        "recent_expenses": recent_expenses,
    }
    return render(request, "billing/dashboard.html", context)


@login_required
def bill(request):
    year, month = parse_month(request)
    summary = calculate_bill(year, month)
    context = {
        "summary": summary,
        "year": year,
        "month": month,
        "month_str": f"{year:04d}-{month:02d}",
    }
    return render(request, "billing/bill.html", context)


@login_required
def payment_list(request):
    payments = Payment.objects.select_related("member").all()
    return render(
        request, "billing/payment_list.html", {"payments": payments}
    )


@login_required
def payment_add(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment recorded.")
            return redirect("payment_list")
    else:
        form = PaymentForm()
    return render(request, "billing/payment_form.html", {"form": form})


@login_required
def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment updated.")
            return redirect("payment_list")
    else:
        form = PaymentForm(instance=payment)
    return render(
        request,
        "billing/payment_form.html",
        {"form": form, "payment": payment},
    )


@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        payment.delete()
        messages.success(request, "Payment deleted.")
    return redirect("payment_list")
