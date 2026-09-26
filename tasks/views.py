from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum

from .models import Task, TimeSession, TaskActivity
from .forms import TaskForm


@login_required
def dashboard(request):
    tasks_qs = Task.objects.filter(user=request.user).order_by("-created_at")
    today = date.today()

    tasks_list = []
    total_seconds = 0
    overdue_count = 0

    for task in tasks_qs:
        # Dynamic flags for UI
        task.is_overdue = bool(task.due_date and task.due_date < today and task.status != "Completed")
        task.is_due_today = bool(task.due_date and task.due_date == today and task.status != "Completed")
        if task.is_overdue:
            overdue_count += 1
        total_seconds += (task.worked_seconds or 0)
        tasks_list.append(task)

    total_tasks = len(tasks_list)
    completed_tasks = sum(1 for t in tasks_list if t.status == "Completed")
    pending_tasks = sum(1 for t in tasks_list if t.status == "Pending")
    running_tasks = sum(1 for t in tasks_list if t.status == "Running")
    paused_tasks = sum(1 for t in tasks_list if t.status == "Paused")

    completion_rate = round((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0

    # Human readable total worked time
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    total_worked_display = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"

    context = {
        "tasks": tasks_list,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "running_tasks": running_tasks,
        "paused_tasks": paused_tasks,
        "overdue_count": overdue_count,
        "completion_rate": completion_rate,
        "total_worked_display": total_worked_display,
    }

    return render(request, "dashboard.html", context)


@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f"Task '{task.title}' created successfully!")
            return redirect("dashboard")
    else:
        form = TaskForm(user=request.user)

    return render(
        request,
        "task_form.html",
        {
            "form": form,
            "title": "Create New Task",
            "is_edit": False,
        },
    )


@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Task '{task.title}' updated successfully.")
            return redirect("dashboard")
    else:
        form = TaskForm(instance=task, user=request.user)

    return render(
        request,
        "task_form.html",
        {
            "form": form,
            "task": task,
            "title": "Edit Task",
            "is_edit": True,
        },
    )


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)

    if request.method == "POST":
        title = task.title
        task.delete()
        messages.success(request, f"Task '{title}' has been deleted.")
        return redirect("dashboard")

    return render(
        request,
        "task_confirm_delete.html",
        {
            "task": task,
        },
    )


# Quick toggle completed/pending
@require_POST
@login_required
def toggle_status(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)

    if task.status == "Completed":
        task.status = "Pending"
        messages.info(request, f"Marked '{task.title}' as Pending.")
    else:
        # If timer was running, stop active session
        now = timezone.now()
        active_sessions = task.time_sessions.filter(is_active=True)
        for s in active_sessions:
            elapsed = int((now - s.started_at).total_seconds())
            s.duration_seconds = max(0, elapsed)
            s.ended_at = now
            s.is_active = False
            s.save()
            TaskActivity.objects.create(task=task, action="STOP")
        task.status = "Completed"
        messages.success(request, f"Congratulations! '{task.title}' marked as completed! 🎉")

    task.save()
    return redirect("dashboard")


# Quick duplicate task
@require_POST
@login_required
def duplicate_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    new_task = Task.objects.create(
        user=request.user,
        title=f"[Copy] {task.title}",
        description=task.description,
        category=task.category,
        priority=task.priority,
        status="Pending",
        due_date=task.due_date,
    )
    messages.success(request, f"Duplicated task as '{new_task.title}'.")
    return redirect("dashboard")



# Timer controls
@require_POST
@login_required
def start_timer(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)

    if task.status != "Running":
        now = timezone.now()
        # End any lingering active sessions
        for s in task.time_sessions.filter(is_active=True):
            s.is_active = False
            s.ended_at = now
            s.duration_seconds = max(0, int((now - s.started_at).total_seconds()))
            s.save()

        TimeSession.objects.create(
            task=task,
            started_at=now,
            is_active=True
        )
        TaskActivity.objects.create(
            task=task,
            action="START"
        )
        task.status = "Running"
        task.save()
        messages.success(request, f"Timer started for '{task.title}'. Focus time!")

    return redirect("dashboard")


@require_POST
@login_required
def pause_timer(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)

    now = timezone.now()
    active_sessions = task.time_sessions.filter(is_active=True)
    for s in active_sessions:
        elapsed = int((now - s.started_at).total_seconds())
        s.duration_seconds = max(0, elapsed)
        s.ended_at = now
        s.is_active = False
        s.save()

    TaskActivity.objects.create(
        task=task,
        action="PAUSE"
    )
    task.status = "Paused"
    task.save()
    messages.info(request, f"Timer paused for '{task.title}'.")

    return redirect("dashboard")


@require_POST
@login_required
def resume_timer(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)

    if task.status != "Running":
        now = timezone.now()
        for s in task.time_sessions.filter(is_active=True):
            s.is_active = False
            s.ended_at = now
            s.duration_seconds = max(0, int((now - s.started_at).total_seconds()))
            s.save()

        TimeSession.objects.create(
            task=task,
            started_at=now,
            is_active=True
        )
        TaskActivity.objects.create(
            task=task,
            action="RESUME"
        )
        task.status = "Running"
        task.save()
        messages.success(request, f"Timer resumed for '{task.title}'.")

    return redirect("dashboard")


@require_POST
@login_required
def stop_timer(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)

    now = timezone.now()
    active_sessions = task.time_sessions.filter(is_active=True)
    for s in active_sessions:
        elapsed = int((now - s.started_at).total_seconds())
        s.duration_seconds = max(0, elapsed)
        s.ended_at = now
        s.is_active = False
        s.save()

    TaskActivity.objects.create(
        task=task,
        action="STOP"
    )
    task.status = "Completed"
    task.save()

    messages.success(request, f"Task '{task.title}' completed! Great job! 🎉")
    return redirect("dashboard")