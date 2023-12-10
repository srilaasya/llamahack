import together
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key using os.getenv
key = os.getenv('TOGETHER_API_KEY')
together.api_key = str(key)

# User input prompt question
# user_msg = "The question is: How to write and publish a book on Feminism with Penguin publishers under 6 months?"

# Together function that takes user input prompt and returns task list for EPIC Flow 1


def generate_task_response(user_msg):
    system_prompt = system_prompt = (
        "You are a verified and famous product and project manager. For every question asked, you output your response in the form of a JSON object as: [{'Task':'', 'Description':'', 'Timeframe':''; 'Task':'', 'Description':'', 'Timeframe':''; and so on}] where 'task' is the name of the task, 'Description' is the process of finishing the task in no more than 2 sentences, and 'Timeframe' is the time required to finish the task in weeks (integer values only). Meticulously break down the question into extremely specific, detail-oriented tasks and give the output in the format mentioned above. The answer should always be JSON Serializable. None of the tasks should last beyond 2 weeks. Now answer the following question in the above format: "
    )

    prompt = f"<s>[INST] <<SYS>>{system_prompt}<</SYS>>\\n\\n{user_msg}[/INST]"

    output = together.Complete.create(
        prompt,
        model="upstage/SOLAR-0-70b-16bit",
        max_tokens=1500,
        temperature=0.01,
        top_k=90,
        top_p=0.8,
        repetition_penalty=1.1,
        stop=['</s>']
    )

    json_output = output['output']['choices'][0]['text']
    return json_output


# json_output = generate_task_response(user_msg)
# print(json_output)
