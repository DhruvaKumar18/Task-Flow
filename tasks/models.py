from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# 1. CATEGORY: Organizes tasks into folders/labels (e.g., Work, Personal)
class Category(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="categories"
    )
    name = models.CharField(max_length=100)
    color = models.CharField(
        max_length=20,
        default="#0d6efd",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


# 2. TASK: The main todo task
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Running', 'Running'),
        ('Paused', 'Paused'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    due_date = models.DateField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_total_worked_seconds(self):
        result = self.time_sessions.aggregate(total=Sum('duration_seconds'))['total']
        return result or 0

    @property
    def total_worked_seconds(self):
        return self.get_total_worked_seconds()

    @property
    def worked_seconds(self):
        return self.get_total_worked_seconds()

    def get_worked_hours(self):
        total = self.get_total_worked_seconds()
        hours = total // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    @property
    def current_session(self):
        return self.time_sessions.filter(is_active=True).last()

    @property
    def timer_running(self):
        return self.time_sessions.filter(is_active=True).exists()

    @property
    def start_time(self):
        session = self.current_session
        return session.started_at if session else None


# 3. TIME SESSION: Records duration for each focus timer run
class TimeSession(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="time_sessions"
    )
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(
        null=True,
        blank=True
    )
    duration_seconds = models.PositiveIntegerField(
        default=0
    )
    is_active = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"Session for {self.task.title} ({self.started_at})"


# 4. TASK ACTIVITY: History logbook of actions (START, PAUSE, RESUME, STOP)
class TaskActivity(models.Model):
    ACTION_CHOICES = [
        ('START', 'START'),
        ('PAUSE', 'PAUSE'),
        ('RESUME', 'RESUME'),
        ('STOP', 'STOP'),
    ]

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="activities"
    )
    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name_plural = "Task Activities"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.action} on {self.task.title} at {self.timestamp}"