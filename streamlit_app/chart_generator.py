import json
import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import date
import datetime
import requests
import os

CURRENT_DATE = date.today()
DATABASE_API_URL = os.getenv('DATABASE_API_URL')


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
        new_task['Finish'] = CURRENT_DATE + datetime.timedelta(days=delta_days)
        new_task['description'] = task['Description']
        new_task['status'] = 'Not Started'

        headers = {
                'Content-Type': 'application/json'
        }
        api_payload = new_task.copy()
        api_payload['Start'] = ''
        api_payload['Finish'] = ''
        api_payload['due_date'] = new_task['Finish'].strftime('%Y-%m-%d')
        print(api_payload)
        response = requests.post(f'{DATABASE_API_URL}tasks', headers=headers, data=json.dumps(api_payload))
        if response.status_code == 201:
            print('Task created successfully')
        else:
            print('Error creating task')

        cleaned_tasks.append(new_task)
        CURRENT_DATE = CURRENT_DATE + datetime.timedelta(days=delta_days)

    df = pd.DataFrame(cleaned_tasks)
    st.dataframe(df)
    return cleaned_tasks


def generate_chart(data):
    data = clean_data(data)
    df = pd.DataFrame(data)
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="title")
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
    return fig