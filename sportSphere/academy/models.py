from django.db import models
from accounts.models import User, Player

class Program(models.Model):
    SPORT_CHOICES = [
        ('football', 'Football'),
        ('basketball', 'Basketball'),
        ('swimming', 'Swimming'),
        ('tennis', 'Tennis'),
        ('gymnastics', 'Gymnastics'),
    ]
    GENDER_CHOICES = [
        ('any', 'Any'),
        ('male', 'Boys Only'),
        ('female', 'Girls Only'),
    ]
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subprograms')
    sport = models.CharField(max_length=30, choices=SPORT_CHOICES)
    title = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='any')
    description = models.TextField()
    min_age = models.PositiveIntegerField(default=6)
    max_age = models.PositiveIntegerField(default=16)
    start_date = models.DateField()
    duration_weeks = models.PositiveIntegerField()
    coach = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'coach'}
    )
    image = models.ImageField(upload_to='programs/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.get_sport_display()})"

class Enrollment(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    enrolled_on = models.DateField(auto_now_add=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )


    class Meta:
        unique_together = ['player', 'program']

    def __str__(self):
        return f"{self.player.full_name} → {self.program.title} ({self.status})"
