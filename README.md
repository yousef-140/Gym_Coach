# 🏋️‍♂️ Gym Assistant

A smart personal gym assistant using RAG (with FAISS) to answer workout and nutrition questions.  
With a dedicated page to help you calculate your daily calorie and protein needs.

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
│   ├── Gym Exercises Dataset     ← workouts data
│   └── daily_food_nutrition_datase     ← nutrition data
│
├── app/
│   ├── app.py            ← Streamlit UI
│   └── pages/
│       └── Nutrition_page.py        ← calculator page
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
- All datasets used (nutrition and workouts) are included locally in the GitHub repository under the `data/` folder.

---

## 📊 Data Sources

- All datasets used in this project are available in the repository under the `data/` directory:
  - `Gym Exercises Dataset` for workout data
  - `daily_food_nutrition_dataset` for nutrition facts
  - `faiss_gym_index/` for the FAISS vector index

---

## 🙌 Contributing

Feel free to open a Pull Request or Issue if you want to contribute or suggest improvements!

---

**Built with ❤️ for all athletes.**
