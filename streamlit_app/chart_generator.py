import plotly.express as px
import pandas as pd
from datetime import date
import datetime

CURRENT_DATE = date.today()

def clean_data(tasks):
    global CURRENT_DATE
    cleaned_tasks = []
    for task in tasks:
        new_task = dict()
        new_task['title'] = task['Task']
        new_task['Start'] = CURRENT_DATE
        # Check if key Timeframe of task is string or number
        if isinstance(task['Timeframe'], str):
            delta_days = int(task['Timeframe'].split()[0])
        else:
            delta_days = task['Timeframe']
        delta_days *= 4
        new_task['due_date'] = CURRENT_DATE + datetime.timedelta(days=delta_days)
        new_task['description'] = task['Description']
        new_task['status'] = 'Not Started'
        cleaned_tasks.append(new_task)
        CURRENT_DATE = CURRENT_DATE + datetime.timedelta(days=delta_days)

    return cleaned_tasks


def generate_chart(data):
    #data = clean_data(data)
    df = pd.DataFrame(data)
    fig = px.timeline(df, x_start="Start", x_end="due_date", y="title")
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
    return fig