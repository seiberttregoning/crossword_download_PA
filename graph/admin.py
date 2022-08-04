from django.contrib import admin

# Register your models here.

from .models import Solve

class SolveAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ['id',
    'solve_Year',
    'solve_Month',
    'solve_Day',
    'solve_Date',
    'solve_Player',
    'solve_Time',
    'solve_Seconds',]

admin.site.register(Solve, SolveAdmin)