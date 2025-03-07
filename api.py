from fastapi import FastAPI
from pydantic import BaseModel
from transformers import MBartForConditionalGeneration, AutoTokenizer
import torch

app = FastAPI()

# **1️⃣ Charger le modèle et le tokenizer**
def load_model():
    model_path = "/Users/ashleyratier/Downloads/modele"  # Mets ton chemin exact
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = MBartForConditionalGeneration.from_pretrained(model_path)
    return model, tokenizer

model, tokenizer = load_model()

# **2️⃣ Définir le format des requêtes**
class TextInput(BaseModel):
    text: str

# **3️⃣ Endpoint pour générer une question**
@app.post("/generate")
def generate_question(input_data: TextInput):
    # Encoder le texte d'entrée
    inputs = tokenizer(input_data.text, return_tensors="pt")

    # Générer la question avec MBart
    with torch.no_grad():  # Désactiver le calcul des gradients pour économiser de la mémoire
        output = model.generate(**inputs, max_length=100, num_return_sequences=1)

    # Décoder le texte généré
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return {"generated_question": generated_text}

# **4️⃣ Endpoint de test**
@app.get("/")
def home():
    return {"message": "API FastAPI avec MBart pour la génération de questions"}
