# 💬 SentiSocial  
### *Analyzing Comments, Understanding Sentiment & Insights*

SentiSocial is an AI-powered web application that analyzes social media post comments to deliver detailed sentiment insights and generate meaningful summaries. Built for content creators, marketers, and analysts, it helps you gauge public perception, engagement tone, and audience feedback — all in one place.

---

## 🚀 Features

- 🔹 **Comment-Level Sentiment Detection**
  - Analyzes individual comments for emotional tone.
  - Sentiment categories:
    - Extremely Positive
    - Moderately Positive
    - Neutral
    - Negative

- 📊 **Overall Sentiment Score**
  - Aggregated sentiment rating for the entire comment section.
  - Score measured out of **5**, based on intensity and distribution of sentiments.

- 📝 **Smart Summary Generator**
  - Summarizes all comments into a concise paragraph.
  - Highlights opinions, praise, criticism, and trends.

- ⚡ **Interactive Web Interface**
  - Built with Streamlit for fast and user-friendly interactions.

---

## 🛠️ Tech Stack

| Tool / Library          | Description                                       |
|-------------------------|---------------------------------------------------|
| **Python**              | Core backend and data processing logic            |
| **Streamlit**           | Frontend framework for the web UI                 |
| **LangChain + LangGraph** | LLM workflow orchestration and graph structuring |
| **OpenAI API**          | LLM-based sentiment analysis and summarization    |
| **Gemini API**          | Complementary model for enhanced response quality |

---

## 📷 Screenshots
<img src="https://raw.githubusercontent.com/soh-kaz/SentiSocial/refs/heads/main/Screenshot.png" />

---

## 🧪 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/soh-kaz/SentiSocial.git
cd sentisocial
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Your API Keys
  Create a .env file in the root directory and add:
```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_gemini_api_key
```

### 5. Run the App
```bash
streamlit run app.py
```


## 🖼️ Workflow
<img src="https://raw.githubusercontent.com/soh-kaz/SentiSocial/refs/heads/main/workflow.png" />

## 📄 License
This project is licensed under the MIT License.

## 🤝 Contributing
Contributions, suggestions, and feedback are welcome!
Feel free to open an issue or submit a pull request.




