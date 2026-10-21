from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ExpenseForm
from .models import Expense


@login_required
def expense_list(request):
    expenses = Expense.objects.select_related("paid_by").all()
    return render(request, "bazaar/expense_list.html", {"expenses": expenses})


@login_required
def expense_add(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense recorded.")
            return redirect("expense_list")
    else:
        form = ExpenseForm()
    return render(request, "bazaar/expense_form.html", {"form": form})


@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated.")
            return redirect("expense_list")
    else:
        form = ExpenseForm(instance=expense)
    return render(
        request, "bazaar/expense_form.html", {"form": form, "expense": expense}
    )


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted.")
    return redirect("expense_list")
