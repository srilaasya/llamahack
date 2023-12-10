from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok

# Local application imports
from db_operations import (
    create_task,
    read_task,
    update_task,
    delete_task,
    read_all_tasks,
    read_all_meetings,
    create_meeting,
    read_meeting,
    delete_meeting,
    read_transcript,
    read_all_transcripts,
    delete_transcript,
    create_transcript,
)
from bson.objectid import ObjectId
from flask_cors import CORS
from datetime import datetime
import re
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/tasks', methods=['POST', 'DELETE', 'GET'])
def tasks_route():
    if request.method == 'POST':
        return create_task_route()
    elif request.method == 'DELETE':
        return delete_all_tasks_route()
    elif request.method == 'GET':
        return read_all_tasks_route()

@app.route('/tasks/<taskID>', methods=['GET', 'POST', 'DELETE'])
def task_route(taskID):
    if request.method == 'GET':
        return read_task_route(taskID)
    elif request.method == 'POST':
        return create_or_update_task_route(taskID)
    elif request.method == 'DELETE':
        return delete_task_route(taskID)


def create_task_route():
    try:
        data = request.get_json()
        # Validate the dueDate field
        due_date = data.get('dueDate')
        if due_date:
            try:
                data['dueDate'] = datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                return jsonify({'error': 'Invalid dueDate format. It should be in ISO 8601 format.'}), 400
        task_id = create_task(data)
        return jsonify({'message': 'Task created', 'taskID': task_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# def delete_all_tasks_route():
#     try:
#         delete_all_tasks()
#         return jsonify({'message': 'All tasks deleted'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400


def delete_task_route(taskID):
    try:
        response, status_code = delete_task(taskID)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 400


def read_all_tasks_route():
    try:
        tasks = read_all_tasks()
        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/tasks/<taskID>', methods=['GET'])
def read_task_route(taskID):
    try:
        task = read_task(taskID)
        if task:
            return jsonify(task), 200
        else:
            return jsonify({'message': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Error in read_task_route: ' + str(e)}), 400


def create_or_update_task_route(taskID):
    try:
        data = request.get_json()
        # Validate the dueDate field
        due_date = data.get('dueDate')
        if due_date:
            try:
                data['dueDate'] = datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                return jsonify({'error': 'Invalid dueDate format. It should be in ISO 8601 format.'}), 400
        update_task(taskID, data)
        return jsonify({'message': 'Task updated'}), 200
    except Exception as e:
        return jsonify({'error': 'Error in create_or_update_task_route: ' + str(e)}), 400


@app.route('/meetings', methods=['POST', 'GET'])
def meetings_route():
    if request.method == 'POST':
        return create_meeting_route()
    elif request.method == 'GET':
        return read_all_meetings_route()


@app.route('/meetings/<meeting_id>', methods=['GET'])
def meeting_route(meeting_id):
    response, status_code = read_meeting(meeting_id)
    return jsonify(response), status_code


def create_meeting_route():
    try:
        data = request.get_json(force=True)

        # Validate the date and time fields
        date = data.get('date')
        time = data.get('time')
        if date and time:
            try:
                # Try to parse the date and time strings as datetime objects
                data['date'] = datetime.strptime(date, '%Y-%m-%d').date()
                data['time'] = datetime.strptime(time, '%H:%M:%S').time()
            except ValueError as ve:
                # If the date or time string is not a valid datetime, return an error
                return jsonify({'error': 'Invalid date or time format. ' + str(ve)}), 400

        # Check required fields for creating a meeting
        required_fields = ['taskID', 'title', 'date', 'time', 'email']
        if not all(field in data for field in required_fields):
            missing_fields = ', '.join(field for field in required_fields if field not in data)
            return jsonify({'error': f'Missing required field(s): {missing_fields}'}), 400

        # Ensure the taskID exists in the Tasks collection
        task_id = data.get('taskID')
        task = read_task(task_id)
        if not task:
            return jsonify({'error': 'Task with the provided taskID does not exist.'}), 404

        # Create meeting and link it to the taskID
        response, status_code = create_meeting(data)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 400


def read_all_meetings_route():
    try:
        meetings = read_all_meetings()
        return jsonify(meetings), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/meetings/<meeting_id>', methods=['GET'])
def read_meeting_route(meeting_id):
    response, status_code = read_meeting(meeting_id)
    return jsonify(response), status_code


@app.route('/meetings/<meeting_id>', methods=['DELETE'])
def delete_meeting_route(meeting_id):
    response, status_code = delete_meeting(meeting_id)
    return jsonify(response), status_code


@app.route('/transcripts', methods=['POST'])
def create_transcript_route():
    data = request.get_json(force=True)
    try:
        transcript_id = create_transcript(data)
        return jsonify({'message': 'Transcript created', 'transcriptID': transcript_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/transcripts/<transcript_id>', methods=['GET'])
def read_transcript_route(transcript_id):
    response, status_code = read_transcript(transcript_id)
    return jsonify(response), status_code


@app.route('/transcripts', methods=['GET'])
def read_all_transcripts_route():
    response, status_code = read_all_transcripts()
    return jsonify(response), status_code


@app.route('/transcripts/<transcript_id>', methods=['DELETE'])
def delete_transcript_route(transcript_id):
    response, status_code = delete_transcript(transcript_id)
    return jsonify(response), status_code


if __name__ == '__main__':
    app.run(port=8000, debug=True)
    run_with_ngrok(app)
