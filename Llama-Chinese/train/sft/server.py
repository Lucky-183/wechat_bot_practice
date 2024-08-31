from flask import Flask, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel, PeftConfig
import time

app = Flask(__name__)

# ===== MODEL LOADING =====
finetune_model_path = "her_model"  # Replace with your model path
base_model_name_or_path = "../../../Atom-7B-Chat"  # Replace with your base model path
device_map = "cuda:0" if torch.cuda.is_available() else "auto"

config = PeftConfig.from_pretrained(finetune_model_path)
tokenizer = AutoTokenizer.from_pretrained(base_model_name_or_path, use_fast=False)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    config.base_model_name_or_path,
    device_map=device_map,
    torch_dtype=torch.float16,
    load_in_8bit=True,
    trust_remote_code=True,
)
model = PeftModel.from_pretrained(model, finetune_model_path, device_map={"":0})
model= model.eval()
# ===== HELPER FUNCTIONS =====
def generate_prompt_llama(messages):
    prompt = ""
    for message in messages:
        role = message["role"]
        content = message["content"]
        if role == "system":
            continue
        prompt += f"<s>{role.capitalize()}: {content.strip()}\n</s>"
    prompt += "<s>Assistant: "
    return prompt

def evaluate_llama(prompt, temperature=0.1, top_p=0.95, top_k=20, num_beams=1, max_new_tokens=128, **kwargs):
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs["input_ids"].to('cuda')

    with torch.no_grad():
        generation_output = model.generate(
            input_ids=input_ids,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            num_beams=num_beams,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            repetition_penalty=1.3,
            eos_token_id=tokenizer.eos_token_id,
            bos_token_id=tokenizer.bos_token_id,
            pad_token_id=tokenizer.pad_token_id,


            **kwargs,
        )
    output = tokenizer.decode(generation_output[0], skip_special_tokens=True)
    generated_text = output.split("Assistant: ")[-1].strip()
    return generated_text

def decode_kwargs(data):
    kwargs = {}
    if "n" in data:
        kwargs["num_return_sequences"] = data["n"]
    if "stop" in data:
        kwargs["early_stopping"] = True
    if "frequency_penalty" in data:
        kwargs["repetition_penalty"] = data["frequency_penalty"]
    return kwargs

# ===== API ROUTES =====
@app.route("/chat/completions", methods=["POST"])
def chat_completions():
    data = request.get_json(force=True)
    model_name = data["model"]
    messages = data["messages"]

    prompt = generate_prompt_llama(messages)

    max_tokens = 64
    temperature = 0.6
    top_p =  0.97
    top_k = 30
    num_beams =  1
    max_new_tokens = 64

    #kwargs = decode_kwargs(data)

    generated_text = evaluate_llama(
        prompt,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        num_beams=num_beams,
        max_new_tokens=max_new_tokens,
#        **kwargs,
    )

    prompt_tokens = len(tokenizer.encode(prompt))
    completion_tokens = len(tokenizer.encode(generated_text))
    total_tokens = prompt_tokens + completion_tokens
    print(f'prompt:{prompt}')
    print(f'reply:{generated_text}')
    return jsonify(
        {
            "object": "chat.completion",
            "id": "dummy",
            "created": int(time.time()),
            "model": model_name,
            "choices": [
                {
                    "message": {"role": "assistant", "content": generated_text},
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
            },
        }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4512)

