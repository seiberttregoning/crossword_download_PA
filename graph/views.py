from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from decimal import Decimal
import pandas as pd
from datetime import date, timedelta
import math


from .models import Solve

# Create your views here.


def index(request):

    list_of_solves = Solve.objects.order_by('-solve_Year', '-solve_Month', '-solve_Day', 'solve_Seconds')


    item = Solve.objects.all().values()
    df = pd.DataFrame(item)
    df.columns = ['ID', 'Month', 'Day', 'Year', 'Date', 'Player', 'Time', 'Seconds']
    df1 = df[['Month', 'Day', 'Year', 'Date', 'Player', 'Time', 'Seconds']].copy()
    df1['Date'] = pd.to_datetime(df['Date']).dt.date
    max_date = df1['Date'].max()
    week_prior = max_date - timedelta(weeks=1)
    df_last_week = df1[df1['Date'] > week_prior]
    all_pivot = df.pivot(index='Player', columns='Date', values='Seconds')
    pivoted = df_last_week.pivot(index='Player', columns='Date', values='Seconds')
    pivoted_median = pivoted.copy()
    pivoted_median['Median last Week'] = pivoted_median.median(numeric_only=True, axis = 1)
    pivoted_median['Median since 2022-07-06'] = all_pivot.median(numeric_only=True, axis = 1)
    pivoted_median = pivoted_median.sort_values(by=['Median last Week'])
    low_scorer = pivoted_median[pivoted_median['Median last Week']==pivoted_median['Median last Week'].min()].index[0]
    date_list= []
    for i in df_last_week['Date'].unique().tolist():
        date_list.append(i.strftime('%Y-%m-%d'))
    seibert_median = pivoted_median[pivoted_median.index=='Seibert']['Median last Week'][0]
    seibert_scores = []
    for i in df_last_week.loc[df['Player']=='Seibert']['Seconds']:
        if math.isnan(i):
            i = ''
        seibert_scores.append(i)
    dirk_scores = []
    for i in df_last_week.loc[df['Player']=='dirk orozco']['Seconds']:
        if math.isnan(i):
            i = ''
        dirk_scores.append(i)
    ellie_scores = []
    for i in df_last_week.loc[df['Player']=='E-thousand']['Seconds']:
        if math.isnan(i):
            i = ''
        ellie_scores.append(i)
    josh_scores = []
    for i in df_last_week.loc[df['Player']=='Joshtreg']['Seconds']:
        if math.isnan(i):
            i = ''
        josh_scores.append(i)


    template = loader.get_template('graph/index.html')
    context = {
        'list_of_solves': list_of_solves,
        'max_date':max_date,
        "df_last_week": df_last_week.to_html(index=False),
        "pivoted_median":pivoted_median.to_html(na_rep = "", classes=["table table-hover"]),
        'low_scorer':low_scorer,
        'date_list':date_list,
        'seibert_scores':seibert_scores,
        'dirk_scores':dirk_scores,
        'ellie_scores':ellie_scores,
        'josh_scores':josh_scores,
        }

    return HttpResponse(template.render(context,request))


