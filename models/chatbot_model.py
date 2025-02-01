from transformers import pipeline

pipe = pipeline("text-generation", model="Rakesh7n/Qwen2.5-0.5_alpaca-finance_finetuned")

def generate_response(prompt):
    response = pipe(prompt, max_length=256, temperature=0.7)
    return response[0]['generated_text']
