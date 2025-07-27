from django.db import models
from accounts.models import User

class Program(models.Model):
    SPORT_CHOICES = [
        ('football', 'Football'),
        ('basketball', 'Basketball'),
        ('tennis', 'Tennis'),
    ]

    sport_type = models.CharField(max_length=20, choices=SPORT_CHOICES)
    image = models.ImageField(upload_to='programs/')

    def __str__(self):
        return self.get_sport_type_display()

class SubProgram(models.Model):
    GENDER_CHOICES = [
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('any', 'Any'),
    ]

    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='subprograms')
    title = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()
    start_date = models.DateField()
    description = models.TextField()
    duration_weeks = models.PositiveIntegerField()
    coach = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'coach'})
    image = models.ImageField(upload_to='subprograms/', blank=True, null=True)


    def __str__(self):
        return self.title

    def age_range(self):
        return f"{self.min_age} - {self.max_age}"
    
from accounts.models import User

class Child(models.Model):
    GENDER_CHOICES = [
        ('boy', 'Boy'),
        ('girl', 'Girl'),
        ('any', 'Any'),
    ]

    parent = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'parent'})
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='children/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.age} yrs)"
    
class Enrollment(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='enrollments')
    subprogram = models.ForeignKey(SubProgram, on_delete=models.CASCADE, related_name='enrollments')
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('child', 'subprogram')  # prevent duplicate enrollments

    def __str__(self):
        return f"{self.child.name} in {self.subprogram.title}"


