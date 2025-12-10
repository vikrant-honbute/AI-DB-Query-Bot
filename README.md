# 🗂️ **AI DB Query Bot — Chat With Your SQL Databases**

A Streamlit-based AI assistant that lets you **chat with your SQL data** using natural language.

It connects either to a local **SQLite `student.db`** or your own **MySQL database**, and uses a Groq LLM-powered LangChain SQL agent to generate SQL queries automatically.

---

# 🚀 **Features**

### 📁 **Dual DB Mode**

- Use a local **SQLite 3** database (`student.db`)
- Or connect to your own **MySQL** database via sidebar

### 🤖 **LLM-Powered SQL Agent**

- Powered by **ChatGroq (llama-3.3-70b-versatile)**
- Uses **create_sql_agent** + **SQLDatabaseToolkit**

### 💬 **Smart Chat Interface**

- Streamlit **chat-style UI**
- Maintains **conversation history** with `st.session_state`

### 🔌 **Secure & Safe DB Access**

- SQLite opened in **read-only** mode
- MySQL credentials entered securely from the sidebar

### ⚡ **Streaming Responses**

- Real-time outputs via `StreamlitCallbackHandler`

---

# 🖼️ **Demo / Screenshot (Placeholder)**

Replace with your actual app screenshot.

```
+--------------------------------------------------------+
| 🗂️ AI DB Query Bot                                    |
+--------------------------------------------------------+
|  Sidebar:                                              |
|  [x] Use SQLite 3 Database - student.db                |
|  [ ] Connect to your MySQL Database                    |
|  GROQ API Key: ***************                         |
+--------------------------------------------------------+
|  Assistant: How can I help you?                        |
|  User: Show top 5 students with highest marks.         |
|  Assistant: SELECT name, marks FROM ...                |
+--------------------------------------------------------+
```

---

# 🧱 **Tech Stack**

| Layer          | Technology / Library                    |
| -------------- | --------------------------------------- |
| **UI**         | Streamlit                               |
| **LLM**        | Groq ChatGroq (llama-3.3-70b-versatile) |
| **Agent**      | LangChain Classic `create_sql_agent`    |
| **Toolkit**    | SQLDatabaseToolkit                      |
| **DB Layer**   | SQLDatabase                             |
| **Databases**  | SQLite (`student.db`), MySQL            |
| **ORM/Engine** | SQLAlchemy                              |
| **Other**      | sqlite3, pathlib.Path                   |

---

# 📦 **Installation**

_Requires Python **3.10+**_

---

## **1️⃣ Clone the repository**

```bash
git clone https://github.com/yourusername/ai-db-query-bot.git
cd ai-db-query-bot
```

---

## **2️⃣ Create and activate a virtual environment**

### 🔹 Windows (CMD / PowerShell)

```bash
python -m venv venv
venv\Scripts\activate
```

### 🔹 macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

## **3️⃣ Install dependencies**

```bash
pip install -r requirements.txt
```

### Minimal `requirements.txt`:

```
streamlit
langchain-community
langchain-classic
langchain-groq
sqlalchemy
mysql-connector-python
```

---

## **4️⃣ Ensure `student.db` exists**

```
ai-db-query-bot/
├── app.py
└── student.db
```

---

# 🔑 **Configuration / Credentials**

All configuration is done **inside the Streamlit sidebar**.

### 🧠 **Groq API Key**

- Required
- Enter it in the field: **“GRoq API Key”**

### 🗄️ **MySQL Connection Details** (if selected)

- Host
- User
- Password
- Database name

### 🪶 **SQLite Mode**

SQLite runs in **read-only mode** for safety.

---

# 📘 **How to Use**

## ▶️ Start the app

```bash
streamlit run app.py
```

---

## 📌 In the Sidebar:

Choose one:

### **✔ SQLite Mode**

- Use SQLLite 3 Database – `student.db`

### **✔ MySQL Mode**

- Provide MySQL Host
- MYSQL User
- MYSQL Password
- MySQL Database

Then enter your **Groq API Key**.

---

## 💬 Chat Examples

Ask natural-language questions like:

- “Show the top 5 students with highest marks”
- “How many students are enrolled in each course?”
- “List all students from the Computer Science department”

The agent will:

- Interpret your question
- Generate SQL automatically
- Execute on DB
- Return results in clean text

Use **“Clear message history”** to reset the chat.

---

# 🧩 **Important Code Pieces**

---

## **1️⃣ LLM Initialization**

```python
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.3-70b-versatile",
    streaming=True,
)
```

---

## **2️⃣ Database Configuration (SQLite & MySQL)**

```python
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(
            create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}")
        )
```

---

## **3️⃣ Agent Creation**

```python
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
```

---

## **4️⃣ Chat Loop**

```python
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query, callbacks=[streamlit_callback])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
```

---

# 📝 **License**

```
MIT License
```

---

# 🙌 **Credits**

- UI created with **Streamlit**
- SQL Agent powered by **LangChain Classic**
- LLM inference via **Groq ChatGroq**
