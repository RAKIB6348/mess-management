from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MemberForm
from .models import Member


@login_required
def member_list(request):
    members = Member.objects.all()
    return render(
        request, "members/member_list.html", {"members": members}
    )


@login_required
def member_add(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Member added.")
            return redirect("member_list")
    else:
        form = MemberForm()
    return render(request, "members/member_form.html", {"form": form})


@login_required
def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Member updated.")
            return redirect("member_list")
    else:
        form = MemberForm(instance=member)
    return render(
        request,
        "members/member_form.html",
        {"form": form, "member": member},
    )
