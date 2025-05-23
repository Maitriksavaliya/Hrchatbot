import requests

GROQ_API_KEY = "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"

def generate_natural_response(intent,employee_name, field_data: dict):
    """
    Generates a natural language response using Groq's LLaMA3-8B model.

#     Args:
#         employee_name (str): e.g. "Ajay Desai"
#         field_data (dict): e.g. {"dob": "2024-04-02", "joiningDate": "2023-06-24"}

#     Returns:
#         str: A natural language sentence generated by the LLM
#     """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Build a prompt using all fields
    field_lines = "\n".join([f"{key}: {value}" for key, value in field_data.items()])

    prompt = (
    f"Generate a professional HR auditor response using the following employee details.\n"
    f"Employee name: {employee_name}\n"
    f"{field_lines}\n\n"
    f"Write only one sentence containing all the provided details. "
    f"Do not add any introductions like 'Here is the response'. "
    f"Do not add explanations or extra context. "
    f"Only return the sentence with the factual information in a formal HR tone.\n"
    f"- If intent is null or unknown, respond with: 'Please enter a valid query.'\n"
    f"- If employee name is not provided, respond with: 'Please enter the query with the employee name.'\n"
    f"- If no field information is provided, respond with: 'I do not have information related to the requested fields.'\n"
    f"- should not contain any kind of additional text other then response"
    f"- remove intoductory text before response like here is a professional response"
)


    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "top_p": 0.85
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"


    # headers = {
    #     "Authorization": f"Bearer {GROQ_API_KEY}",
    #     "Content-Type": "application/json"
    # }

    # # Build prompt instructions
    # prompt = (
    #     "You are an HR assistant. Your job is to generate a professional response for HR queries.\n\n"
    #     "Rules:\n"
    #     "- If intent is null or unknown, respond with: 'Please enter a valid query.'\n"
    #     "- If employee name is not provided, respond with: 'Please enter the query with the employee name.'\n"
    #     "- If no field information is provided, respond with: 'I do not have information related to the requested fields.'\n"
    #     "- If all required data is available, generate a single professional sentence containing the provided field values "
    #     "in formal HR tone, without explanations or introductions.\n"
    #     "- should not contain any kind of additional text other then response"
    #     "- remove intoductory text before response like here is a professional response"
    # )

    # # Input data
    # prompt += f"\nIntent: {intent or 'null'}"
    # prompt += f"\nEmployee Name: {employee_name or 'null'}"
    # prompt += "\nField Data:\n"
    # if field_data:
    #     for key, value in field_data.items():
    #         prompt += f"{key}: {value}\n"
    # else:
    #     prompt += "null\n"

    # # Example output when all data is present
    # # prompt += (
    # #     "\nExample output (when all inputs are valid):\n"
    # #     "'Ajay Desai's last name is Desai, date of birth is 28th April 2002, and Aadhaar number is 123412341234.'\n"
    # # )

    # payload = {
    #     "model": "llama3-8b-8192",
    #     "messages": [
    #         {"role": "user", "content": prompt}
    #     ],
    #     "temperature": 0.2,
    #     "top_p": 0.85
    # }

    # response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    # if response.status_code == 200:
    #     return response.json()["choices"][0]["message"]["content"].strip()
    # else:
    #     return f"Error: {response.status_code} - {response.text}"
