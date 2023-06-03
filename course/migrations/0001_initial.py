# Generated by Django 4.1.7 on 2023-06-03 04:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("project", "0001_initial"),
        ("membership", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
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
                ("title", models.CharField(max_length=200, null=True)),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True, editable=False, populate_from="title", unique=True
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("is_published", models.BooleanField(default=False)),
                ("active", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CourseContent",
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
                ("syllabus", models.TextField(blank=True, null=True)),
                ("prerequisites", models.TextField(blank=True)),
            ],
            options={
                "verbose_name_plural": "Course content",
            },
        ),
        migrations.CreateModel(
            name="CourseMetadata",
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
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("beginner", "Beginner"),
                            ("intermediate", "Intermediate"),
                            ("advanced", "Advanced"),
                        ],
                        max_length=25,
                    ),
                ),
                (
                    "rating",
                    models.DecimalField(decimal_places=2, default=0, max_digits=3),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("certificate", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name_plural": "Course metadata",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
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
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField(blank=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("duration", models.PositiveIntegerField(blank=True, null=True)),
                ("is_published", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Program",
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
                ("title", models.CharField(max_length=150, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="program_images/"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "duration",
                    models.PositiveIntegerField(help_text="Duration in weeks"),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Quiz",
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
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("total_marks", models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Video",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "video_file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="videos/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                ["mp4", "mkv", "wmv", "3gp", "f4v", "avi", "mp3"]
                            )
                        ],
                    ),
                ),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.lesson"
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Question",
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
                ("text", models.TextField()),
                ("correct_answer", models.TextField()),
                ("marks", models.PositiveIntegerField(default=1)),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.quiz"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Module",
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
                ("title", models.CharField(max_length=200)),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True, editable=False, populate_from="title", unique=True
                    ),
                ),
                ("description", models.TextField(blank=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("duration", models.PositiveIntegerField(blank=True, null=True)),
                ("is_published", models.BooleanField(default=False)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="modules",
                        to="course.course",
                    ),
                ),
                (
                    "quiz",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.quiz",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.AddField(
            model_name="lesson",
            name="module",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="course.module"
            ),
        ),
        migrations.CreateModel(
            name="File",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="files/",
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
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.lesson"
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CourseDetails",
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
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="course_images/"
                    ),
                ),
                ("duration", models.PositiveIntegerField(default=12)),
                ("enrollment_count", models.PositiveIntegerField(default=0)),
                ("enrollment_deadline", models.DateField(blank=True, null=True)),
                (
                    "instructor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="membership.instructor",
                    ),
                ),
                (
                    "program",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.program"
                    ),
                ),
                (
                    "projects",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.project",
                    ),
                ),
                ("skills", models.ManyToManyField(to="project.techskill")),
            ],
            options={
                "verbose_name_plural": "Course details",
            },
        ),
        migrations.AddField(
            model_name="course",
            name="content",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="course.coursecontent"
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="details",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="course.coursedetails"
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="metadata",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="course.coursemetadata"
            ),
        ),
        migrations.CreateModel(
            name="Answer",
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
                ("text", models.CharField(max_length=200)),
                ("is_correct", models.BooleanField(default=False)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.question",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Enrollment",
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
                ("date_enrolled", models.DateTimeField(auto_now_add=True)),
                ("date_completed", models.DateTimeField(blank=True, null=True)),
                ("is_completed", models.BooleanField(default=False)),
                (
                    "progress",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
                ),
                (
                    "grade",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.course",
                    ),
                ),
                (
                    "program",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.program",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="membership.student",
                    ),
                ),
            ],
            options={
                "unique_together": {("student", "course", "program")},
            },
        ),
    ]
