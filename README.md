
# 🏋️‍♂️ Gym Assistant

An intelligent personal gym assistant powered by RAG (retrieval-augmented generation) with FAISS, supporting workout and nutrition question answering, plus a calories and protein needs calculator.

---

## ✅ Features

- Smart chatbot for workout and nutrition questions  
- Arabic and English language support  
- RAG (retrieval-augmented generation) with FAISS for accurate context  
- Nutrition and workout datasets indexed  
- Calories and protein needs calculator  
- User-friendly Streamlit interface

---

## 📁 Project Structure

```
GYM ASSISTANT/
│
├── Backend/
│   └── fast.py            ← FastAPI backend
│
├── data/
│   ├── faiss_gym_index/   ← FAISS index
│   ├── exercises.json     ← workouts data
│   └── nutrition.json     ← nutrition data
│
├── app/
│   ├── main.py            ← Streamlit UI
│   └── pages/
│       └── calc.py        ← calculator page
│
├── .env                   ← environment variables
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run

1️⃣ Install requirements

```bash
pip install -r requirements.txt
```

2️⃣ Create your `.env` file:

```env
TOGETHER_API_KEY=your_api_key_here
```

3️⃣ Run Streamlit app

```bash
cd app
streamlit run app.py
```

4️⃣ Run the FastAPI backend

```bash
cd Backend
uvicorn fast:app --reload
```

---

## 🚀 How it works

- Uses LangChain + FAISS to retrieve relevant knowledge from nutrition/workout files.  
- Translates user queries if in Arabic, and translates back the answers.  
- Offers a calories and protein needs calculator using simple formulas inside the Streamlit page.

---

## 🙌 Contributing

Feel free to open a Pull Request or Issue if you want to contribute or suggest improvements!  

---

**Built with ❤️ for all athletes.**
