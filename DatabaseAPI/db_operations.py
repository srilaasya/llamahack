from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import os
from bson import json_util
import json
import uuid

load_dotenv(find_dotenv())

password = os.getenv('MONGO_PASSWORD')
username = os.getenv('MONGO_USERNAME')

# Connect to MongoDB
connection_string = f'mongodb+srv://{username}:{password}@cluster0.wuv7y.mongodb.net/'

client = MongoClient(connection_string)
db = client['Tasks']  # replace with your database name


def create_task(data):
    # Generate a unique taskID using UUID and add to data
    data['taskID'] = str(uuid.uuid4())

    # Check for required fields
    required_fields = ['title', 'description', 'due_date', 'status']  # 'taskID' is already added, no need to check
    if not all(field in data for field in required_fields):
        missing_fields = ', '.join(field for field in required_fields if field not in data)
        raise Exception(f'Missing required field(s): {missing_fields}')

    # Insert the task into the database and return the generated taskID
    db.Tasks.insert_one(data)
    return data['taskID']


def read_task(taskID):
    task = db.Tasks.find_one({'taskID': taskID})
    return json.loads(json_util.dumps(task)) if task else None


def read_all_tasks():
    tasks = list(db.Tasks.find())
    return json.loads(json_util.dumps(tasks))


def update_task(taskID, data):
    result = db.Tasks.update_one({'taskID': taskID}, {'$set': data})
    return {'message': 'Task updated'} if result.modified_count > 0 else {'error': 'Task not found'}


def delete_task(taskID):
    result = db.Tasks.delete_one({'taskID': taskID})
    if result.deleted_count == 0:
        return {'error': 'Task not found'}, 404
    return {'message': 'Task deleted'}, 200


def create_meeting(data):
    # Check if taskID exists in the payload and if it corresponds to an existing task
    task_id = data.get('taskID')
    if not task_id:
        raise Exception('Missing taskID in the meeting data.')

    # Verify that the task exists
    if db.Tasks.find_one({'taskID': task_id}) is None:
        raise Exception('Task with the provided taskID does not exist.')
    data['meetingID'] = str(uuid.uuid4())  # Generate a unique meetingID
    db.Meetings.insert_one(data)

    return {'message': 'Meeting created with taskID linkage'}, 201
    # Generate a unique meetingID
    data['meetingID'] = str(uuid.uuid4())

    # Now insert the meeting data
    db.Meetings.insert_one(data)

    return {'message': 'Meeting created with taskID linkage'}, 200


def delete_meeting(meeting_id):
    result = db.Meetings.delete_one({'meetingID': meeting_id})
    if result.deleted_count == 0:
        return {'error': 'Meeting not found'}, 404
    return {'message': 'Meeting deleted'}, 200


def read_all_meetings():
    meetings = list(db.Meetings.find())
    return json.loads(json_util.dumps(meetings))


def read_meeting(meeting_id):
    meeting = db.Meetings.find_one({'meetingID': meeting_id})
    if meeting is None:
        return {'error': 'Meeting not found'}, 404
    return json.loads(json_util.dumps(meeting)), 200


def create_transcript(data):
    # Generate a unique transcriptID using UUID and add to data
    data['transcriptID'] = str(uuid.uuid4())

    # Check for the 'message' or 'transcript' field
    if 'message' not in data:
        raise Exception('Missing required field: message')

    # Insert the transcript into the database and return the generated transcriptID
    db.Transcripts.insert_one(data)
    return data['transcriptID']


def read_transcript(transcript_id):
    transcript = db.Transcripts.find_one({'transcriptID': transcript_id})
    if transcript is None:
        return {'error': 'Transcript not found'}, 404
    return json.loads(json_util.dumps(transcript)), 200


def read_all_transcripts():
    transcripts = list(db.Transcripts.find())
    return json.loads(json_util.dumps(transcripts)), 200


def delete_transcript(transcript_id):
    result = db.Transcripts.delete_one({'transcriptID': transcript_id})
    if result.deleted_count == 0:
        return {'error': 'Transcript not found'}, 404
    return {'message': 'Transcript deleted'}, 200


def test_connection():
    tasks = read_all_tasks()
    print(tasks)
