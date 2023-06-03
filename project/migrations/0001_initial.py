# Generated by Django 4.1.7 on 2023-06-03 04:30

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("priority", models.IntegerField(default=1)),
                ("progress", models.IntegerField(default=0)),
                (
                    "status",
                    models.CharField(
                        choices=[("new", "New"), ("completed", "Completed")],
                        default="new",
                        max_length=10,
                    ),
                ),
                ("start_date", models.DateField(default=datetime.date.today)),
                ("duration", models.PositiveIntegerField(default=12)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("paid", models.BooleanField(default=True)),
                (
                    "budget",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("completed_date", models.DateField(blank=True, null=True)),
                ("comments", models.TextField(blank=True, null=True)),
                (
                    "assigned_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assigned_projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="TechSkill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("priority", models.IntegerField(default=1)),
                ("progress", models.IntegerField(default=0)),
                (
                    "status",
                    models.CharField(
                        choices=[("new", "New"), ("completed", "Completed")],
                        default="new",
                        max_length=10,
                    ),
                ),
                ("due_date", models.DateField()),
                (
                    "estimated_hours",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                (
                    "actual_hours",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                ("comments", models.TextField(blank=True, null=True)),
                (
                    "assigned_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assigned_tasks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.project",
                    ),
                ),
                ("tags", models.ManyToManyField(blank=True, to="project.tag")),
            ],
        ),
        migrations.CreateModel(
            name="ProjectAttachment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="project_attachments/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                [
                                    "pdf",
                                    "docx",
                                    "doc",
                                    "xls",
                                    "xlsx",
                                    "ppt",
                                    "pptx",
                                    "zip",
                                    "rar",
                                    "7zip",
                                ]
                            )
                        ],
                    ),
                ),
                (
                    "uploaded_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("comments", models.TextField(blank=True, null=True)),
                ("tags", models.ManyToManyField(blank=True, to="project.tag")),
            ],
        ),
        migrations.AddField(
            model_name="project",
            name="attachments",
            field=models.ManyToManyField(blank=True, to="project.projectattachment"),
        ),
        migrations.AddField(
            model_name="project",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="tags",
            field=models.ManyToManyField(blank=True, to="project.tag"),
        ),
        migrations.CreateModel(
            name="Activity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "activity_type",
                    models.CharField(
                        choices=[
                            ("created_project", "Created a new project"),
                            ("updated_project", "Updated a project"),
                            ("deleted_project", "Deleted a project"),
                            ("created_task", "Created a new task"),
                            ("updated_task", "Updated a task"),
                            ("deleted_task", "Deleted a task"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.project",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.task",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-date_created",),
            },
        ),
    ]
