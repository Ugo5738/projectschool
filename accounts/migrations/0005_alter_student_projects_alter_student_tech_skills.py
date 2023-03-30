# Generated by Django 4.1.7 on 2023-03-30 10:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_alter_student_projects_alter_student_tech_skills"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="projects",
            field=models.ManyToManyField(
                blank=True, related_name="projects", to="accounts.project"
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="tech_skills",
            field=models.ManyToManyField(
                blank=True, related_name="tech_skills", to="accounts.techskill"
            ),
        ),
    ]