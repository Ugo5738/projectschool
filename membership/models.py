from accounts.models import User
from django.db import models
from django.db.models import Q
from helpers.models import TrackingModel
from project.models import Project, Task, TechSkill

LEARNING_STYLES = [
    ('visual', 'Visual'), 
    ('auditory', 'Auditory'), 
    ('kinesthetic', 'Kinesthetic')
]

GOALS = [
    ('employment', 'Get a job'), 
    ('entrepreneur', 'Build a Startup'), 
    ('experience', 'Work in a team')
]

DAYS = [
    ('monday', 'Monday'), 
    ('tuesday', 'Tuesday'), 
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'), 
    ('friday', 'Friday'), 
    ('saturday', 'Saturday'),
    ('sunday', 'Sunday'),
]

class SearchManager(models.Manager):
    def search(self, query=None):
        if query is not None:
            student_query = Q(goals__icontains=query) | Q(learning_style__icontains=query)
            instructor_query = Q(bio__icontains=query) | Q(education__icontains=query)
            client_query = Q(company_name__icontains=query) | Q(industry__icontains=query)

            student_results = Student.objects.filter(student_query)
            instructor_results = Instructor.objects.filter(instructor_query)
            client_results = Client.objects.filter(client_query)

            # Combine and return the search results
            return student_results, instructor_results, client_results
        
        # If no query is provided, return an empty result
        return [], [], []


class Student(TrackingModel):
    student = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='student_profile'
    )
    goals = models.CharField(choices=GOALS, max_length=50, blank=True, null=True)  # make it so that students can select multiple options
    learning_style = models.CharField(choices=LEARNING_STYLES, max_length=50) 
    availability = models.CharField(choices=DAYS, max_length=50, blank=True, null=True)   # make it so that students can select multiple options
    tech_skills = models.ManyToManyField(TechSkill, related_name='tech_skills', blank=True)
    projects = models.ManyToManyField(Project, related_name='projects', blank=True)
    tasks = models.ManyToManyField(Task, related_name='tasks', blank=True)
    referrer_code = models.CharField(max_length=20, blank=True, null=True)

    objects = SearchManager() 

    def __str__(self):
        return self.student.get_full_name

    def delete(self, *args, **kwargs):
        self.student.delete()
        super().delete(*args, **kwargs)


class Instructor(TrackingModel):
    instructor = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='instructor_profile'
    )
    bio = models.TextField(blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    reviews = models.PositiveIntegerField(default=0)
    referrer_code = models.CharField(max_length=20, blank=True, null=True)

    objects = SearchManager() 
    
    def __str__(self):
        return self.instructor.get_full_name
    
    def delete(self, *args, **kwargs):
        self.instructor.delete()
        super().delete(*args, **kwargs)


class Client(TrackingModel):
    client = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    # contact_person = models.CharField(max_length=100)
    # email = models.EmailField()
    # phone_number = models.CharField(max_length=20)
    referrer_code = models.CharField(max_length=20, blank=True, null=True)

    objects = SearchManager() 

    def __str__(self):
        return self.client.get_full_name
    
    def delete(self, *args, **kwargs):
        self.client.delete()
        super().delete(*args, **kwargs)
    

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred_student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='referred_by', blank=True, null=True)
    referred_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='referred_by', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        referring_user = self.referrer.get_full_name
        referred_user = self.referred_student or self.referred_client
        referred_user_type = 'Student' if self.referred_student else 'Client'
        return f"{referring_user} referred {referred_user} ({referred_user_type}) on {self.date_created}"
    