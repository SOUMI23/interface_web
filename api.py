from fastapi import FastAPI
from pydantic import BaseModel
from transformers import MBartForConditionalGeneration, AutoTokenizer
import torch

app = FastAPI()

# Chargement du modèle et du tokenizer
def load_model():
    model_path = "AshleyRatier/modele_generation_questions"  
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = MBartForConditionalGeneration.from_pretrained(model_path)
    return model, tokenizer

model, tokenizer = load_model()

class TextInput(BaseModel):
    text: str

# Endpoint pour générer une question**
@app.post("/generate")
def generate_question(input_data: TextInput):
    
    inputs = tokenizer(input_data.text, return_tensors="pt")

    # Générer la question avec MBart
    with torch.no_grad():  
        output = model.generate(**inputs, max_length=100, num_return_sequences=1)

    # Décoder le texte généré
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return {"generated_question": generated_text}

#Endpoint de test
@app.get("/")
def home():
    return {"message": "API FastAPI avec MBart pour la génération de questions"}
