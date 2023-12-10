
from flask import Flask, request, jsonify
import json
# from your_audio_processing_module import process_audio_with_whisper  # Replace with your actual module
# from your_text_processing_module import process_text_with_cohere  # Replace with your actual module

app = Flask(__name__)

def extract_fields_from_line(line):
    try:
        # Split the line into a list using commas as the delimiter
        fields = line.split(',')

        # Ensure that the line has exactly three fields
        if len(fields) == 3:
            # Extract the fields
            task = fields[0].strip()
            description = fields[1].strip()
            timeframe = fields[2].strip()

            # Return the extracted fields
            return {'task': task, 'description': description, 'timeframe': timeframe}
        else:
            # Handle the case where the line does not have exactly three fields
            raise ValueError("Each line must have exactly three fields.")

    except Exception as e:
        # Handle any exceptions and return an error message
        return {'error': str(e)}

@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        # Assuming the MP3 data is sent in the 'audio' field of the request - uncomment later
        print("before reading audio file name")

        mp3_data = request.files['audio'].read()

        print("after reading audio file name")

        # # Call the function from your_audio_processing_module - uncomment later
        # text_result = process_audio_with_whisper(mp3_data)

        # dummy text
        text_result = ""
        # text_result = request.json['text']
        # text_result = json.loads(request.form['text'])

        # lines = text_result.strip().split('\n')

        # result_list = []
        # for line in lines:
        #     result = extract_fields_from_line(line)
        #     result_list.append(result)

        # json_result = json.dumps(result_list, indent=2)
        dummy_json_data = {
            "result": "success",
            "message": "Audio processing completed",
            "data": [
                {"task": "Task 1", "description": "Description 1", "timeframe": "Timeframe 1"},
                {"task": "Task 2", "description": "Description 2", "timeframe": "Timeframe 2"},
                {"task": "Task 3", "description": "Description 3", "timeframe": "Timeframe 3"}
            ]
        }

        return jsonify(dummy_json_data)

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({'error': str(e)}), 500
    
@app.route('/process_text', methods=['POST'])
def process_text():
    try:
        # Assuming the text data is sent in the 'text' field of the request - uncomment later
        # text_data = request.json['text']

        # # Call the function from your_text_processing_module
        # text_result = process_text_with_cohere(text_data)

        text_result = request.json['text']

        lines = text_result.strip().split('\n')

        result_list = []
        for line in lines:
            result = extract_fields_from_line(line)
            result_list.append(result)

        json_result = json.dumps(result_list, indent=2)

        return json_result

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)