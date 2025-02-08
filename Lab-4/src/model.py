import openai

def get_openai_response(prompt, API_KEY, vAR_system_instr):
    client = openai.OpenAI(api_key=API_KEY)

    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": vAR_system_instr
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            }
        ]
        }
    ],
    temperature=1,
    max_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format={
        "type": "text"
    }
    )
    return response.choices[0].message.content
