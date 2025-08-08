from fastapi import FastAPI
from dotenv import load_dotenv
from together import Together
from pydantic import BaseModel
import re
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from googletrans import Translator

# Load environment variables
load_dotenv()
app = FastAPI()

# Initialize Together API client
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
user_context = {}

# Load embeddings and FAISS index   meta-llama/Llama-3-8B-Instruct
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("data/faiss_gym_index", embedding_model, allow_dangerous_deserialization=True)

# Request/Response models for chat
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/llm/", response_model=ChatResponse)
def l_l_m(chat_input: ChatRequest):
    user_input = chat_input.query

    # Detect and translate language if Arabic
    translator = Translator()
    detected_lang = translator.detect(user_input).lang
    if detected_lang == 'ar':
        user_input = translator.translate(user_input, src='ar', dest='en').text

    # Capture user's name if mentioned
    name_match = re.search(r"my name is (\w+)", user_input.lower())
    if name_match:
        user_context["name"] = name_match.group(1).capitalize()

    if "name" in user_context and "my name is" not in user_input.lower():
        user_input = f"{user_context['name']} said: {user_input}"

    # Retrieve relevant context from vectorstore
    retrieved_docs = vectorstore.similarity_search(user_input, k=1)
    max_context_chars = 4000  
    retrieved_text = ""
    for doc in retrieved_docs:
        if len(retrieved_text) + len(doc.page_content) <= max_context_chars:
            retrieved_text += "\n\n" + doc.page_content
        else:
            break

    # Build clean prompt 
    full_prompt = f"""
You are a professional gym coach.
Answer the user's question in a clear, complete sentence that makes sense.
Do not say "based on the context" or similar phrases.
If the question is about exercises, give the name and a short useful description.
Be natural and concise.

Context:
{retrieved_text}

Question: {user_input}
Answer in English:"""

    try:
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.1",
            messages=[{"role": "user", "content": full_prompt}]
        )
        model_ans = response.choices[0].message.content.strip()

        # Remove unwanted starting phrases
        remove_phrases = [
            "Based on the context, ",
            "According to the context, ",
            "Given the context, ",
            "From the retrieved documents, ",
            "Using the provided context, ",
        ]
        for phrase in remove_phrases:
            if model_ans.lower().startswith(phrase.lower()):
                model_ans = model_ans[len(phrase):].strip()
                break

        # Avoid broken/too short answers
        if len(model_ans.split()) < 3:
            model_ans = "I couldn't find a clear answer. Please rephrase your question."

    except Exception as e:
        model_ans = f"❌ LLM Error: {e}"

    # Translate back to Arabic if original input was Arabic
    if detected_lang == 'ar':
        model_ans = translator.translate(model_ans, src='en', dest='ar').text

    return ChatResponse(answer=model_ans)

# Request/Response models for nutrition
class NutritionRequest(BaseModel):
    weight: float
    height: float
    age: int
    gender: str
    activity_level: float

class NutritionResponse(BaseModel):
    calories: int
    protein_min: int
    protein_max: int

@app.post("/nutrition/", response_model=NutritionResponse)
def calculate_nutrition(data: NutritionRequest):
    # Calculate BMR
    if data.gender == "male":
        bmr = 10 * data.weight + 6.25 * data.height - 5 * data.age + 5
    else:
        bmr = 10 * data.weight + 6.25 * data.height - 5 * data.age - 161

    calories = int(bmr * data.activity_level)
    protein_min = int(data.weight * 1.6)
    protein_max = int(data.weight * 2.2)

    return NutritionResponse(
        calories=calories,
        protein_min=protein_min,
        protein_max=protein_max
    )
