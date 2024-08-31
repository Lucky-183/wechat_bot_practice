import requests

# API URL
url = "http://localhost:4512/chat/completions"

# Initialize the conversation with a system message
conversation = [
]

# Function to send a request and update the conversation
def send_message(message):
    # Add user's message to the conversation
    conversation.append({"role": "user", "content": message})
    
    # Data to send in POST request
    data = {
        "model": "my_llama_model",
        "messages": conversation,
        "max_tokens": 128,
        "temperature": 0.15,
        "top_p": 0.95,
        "top_k": 50,
        "num_beams": 1,
    }
    
    # Send POST request
    response = requests.post(url, json=data)
    
    # Get the response from the server
    result = response.json()
    assistant_message = result["choices"][0]["message"]["content"]
    
    # Add assistant's message to the conversation
    conversation.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message

# Example of a conversation
print(send_message("你知道什么是量子计算吗？"))
print(send_message("刚才说到哪了？"))

