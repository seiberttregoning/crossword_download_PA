from django.db import models
from django.utils import timezone
import datetime
from datetime import date


# Create your models here.

class Solve(models.Model):
    solve_Month = models.IntegerField()
    solve_Day = models.IntegerField()
    solve_Year = models.IntegerField()
    solve_Date = models.DateField()
    solve_Player = models.CharField(max_length = 50)
    solve_Time = models.DurationField(null=True, blank=True)
    solve_Seconds = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'ID: {self.id}, solve_Date: {self.solve_Date}, {self.solve_Player}, {self.solve_Seconds}'

    def was_recent(self):
        return self.solve_Date >= date.today() - datetime.timedelta(days=3)