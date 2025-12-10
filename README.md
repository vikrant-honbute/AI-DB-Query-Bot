\# 🗂️ AI DB Query Bot — Chat With Your SQL Databases



A Streamlit-based AI assistant that lets you \*\*chat with your SQL data\*\*.  

It connects either to a local \*\*SQLite `student.db`\*\* file or to a \*\*MySQL database\*\*, and uses a Groq LLM-powered LangChain agent to interpret natural-language questions and generate SQL queries behind the scenes.



---



\## 🚀 Features



\- 📁 \*\*Dual DB Mode\*\*

&nbsp; - Use a local \*\*SQLite 3\*\* database (`student.db`)

&nbsp; - Or connect to your own \*\*MySQL\*\* database from the sidebar

\- 🤖 \*\*LLM-Powered SQL Agent\*\*

&nbsp; - Uses `ChatGroq` with the \*\*llama-3.3-70b-versatile\*\* model

&nbsp; - Built with `create\_sql\_agent` and `SQLDatabaseToolkit`

\- 💬 \*\*Chat Interface\*\*

&nbsp; - Streamlit chat-style UI (`st.chat\_message`, `st.chat\_input`)

&nbsp; - Keeps \*\*conversation history\*\* in `st.session\_state`

\- 🔌 \*\*Safe DB Access\*\*

&nbsp; - SQLite is opened in \*\*read-only\*\* mode

&nbsp; - MySQL credentials are entered securely via sidebar

\- ⚡ \*\*Streaming Responses\*\*

&nbsp; - Uses `StreamlitCallbackHandler` for streaming agent output



---



\## 🖼️ Demo / Screenshot (Placeholder)



> Replace this with a real screenshot from your app.



```text

+--------------------------------------------------------+

| 🗂️ AI DB Query Bot                                    |

+--------------------------------------------------------+

|  Sidebar:                                              |

|  \[x] Use SQLite 3 Database - student.db                |

|  \[ ] Connect to your MySQL Database                    |

|  GROQ API Key: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*                         |

+--------------------------------------------------------+

|  Assistant: How can I help you?                        |

|  User: Show top 5 students with highest marks.         |

|  Assistant: SELECT name, marks FROM ...                |

+--------------------------------------------------------+









\## 🧱 Tech Stack



| Layer            | Technology/Library                           |

|------------------|-----------------------------------------------|

| UI               | Streamlit                                     |

| LLM              | Groq ChatGroq (llama-3.3-70b-versatile)       |

| Agent            | LangChain Classic `create\_sql\_agent`          |

| Toolkit          | SQLDatabaseToolkit                           |

| DB Abstraction   | SQLDatabase                                   |

| Databases        | SQLite (`student.db`), MySQL                  |

| ORM / Engine     | SQLAlchemy                                    |

| Others           | sqlite3, pathlib.Path                         |



---



\## 📦 Installation



These commands assume you have \*\*Python 3.10+\*\* installed.



\### 1️⃣ Clone the repository



```bash

git clone https://github.com/yourusername/ai-db-query-bot.git

cd ai-db-query-bot



\## 2️⃣ Create and activate a virtual environment



\### Windows (CMD/PowerShell):

```bash

python -m venv venv

venv\\Scripts\\activate

```



\### macOS / Linux:

```bash

python -m venv venv

source venv/bin/activate

```



---



\## 3️⃣ Install dependencies



```bash

pip install -r requirements.txt

```



\### A minimal `requirements.txt` for this app would include:



```

streamlit

langchain-community

langchain-classic

langchain-groq

sqlalchemy

mysql-connector-python

```



(Plus anything else you already use in your environment.)



---



\## 4️⃣ Make sure `student.db` exists



Place your `student.db` file in the same directory as `app.py`:



```

ai-db-query-bot/

├── app.py

└── student.db

```



---



\## 🔑 Configuration / Credentials



This app does not read environment variables directly.  

All credentials are entered via the \*\*Streamlit sidebar\*\*.



\### 🧠 Groq API Key  

\- Required  

\- Entered in the field: \*\*"GRoq API Key"\*\*



\### 🗄️ MySQL Connection Details (only if you choose the MySQL option):

\- Host (e.g., localhost or server IP)  

\- User  

\- Password  

\- Database name  



\### SQLite Mode  

For SQLite mode, the app automatically uses `student.db` located next to `app.py` and opens it in \*\*read-only mode\*\*.



---



\## 📘 How to Use



\### Start the app:

```bash

streamlit run app.py

```



\### In the sidebar:



Choose one:



\- \*\*Use SQLLite 3 Database – Student.db\*\* (local SQLite)

\- \*\*Connect to your MySQL Database\*\* (your own MySQL DB)



If using MySQL, fill:



\- Provide MySQL Host  

\- MYSQL User  

\- MYSQL password  

\- MySQL database  



Enter your \*\*Groq API Key\*\*.



---



\### The chat area will show:

> “How can I help you?”



---



\### Example natural-language questions:



\- “Show the top 5 students with highest marks”

\- “How many students are enrolled in each course?”

\- “List all students from the Computer Science department”



---



\### The agent will:



\- Interpret your question  

\- Generate SQL queries using `create\_sql\_agent` + `SQLDatabaseToolkit`  

\- Execute them against the selected database  

\- Return the answer in plain text in the chat  



Use the \*\*“Clear message history”\*\* button to reset the chat.



---



\## 🧩 Important Code Pieces



\### 1️⃣ LLM Initialization

```python

llm = ChatGroq(

&nbsp;   groq\_api\_key=api\_key,

&nbsp;   model\_name="llama-3.3-70b-versatile",

&nbsp;   streaming=True,

)

```



---



\### 2️⃣ Database Configuration (SQLite \& MySQL)

```python

@st.cache\_resource(ttl="2h")

def configure\_db(db\_uri, mysql\_host=None, mysql\_user=None, mysql\_password=None, mysql\_db=None):

&nbsp;   if db\_uri == LOCALDB:

&nbsp;       dbfilepath = (Path(\_\_file\_\_).parent / "student.db").absolute()

&nbsp;       creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)

&nbsp;       return SQLDatabase(create\_engine("sqlite:///", creator=creator))

&nbsp;   elif db\_uri == MYSQL:

&nbsp;       if not (mysql\_host and mysql\_user and mysql\_password and mysql\_db):

&nbsp;           st.error("Please provide all MySQL connection details.")

&nbsp;           st.stop()

&nbsp;       return SQLDatabase(

&nbsp;           create\_engine(f"mysql+mysqlconnector://{mysql\_user}:{mysql\_password}@{mysql\_host}/{mysql\_db}")

&nbsp;       )

```



---



\### 3️⃣ Agent Creation

```python

toolkit = SQLDatabaseToolkit(db=db, llm=llm)



agent = create\_sql\_agent(

&nbsp;   llm=llm,

&nbsp;   toolkit=toolkit,

&nbsp;   verbose=True,

&nbsp;   agent\_type=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION,

)

```



---



\### 4️⃣ Chat Loop

```python

if "messages" not in st.session\_state or st.sidebar.button("Clear message history"):

&nbsp;   st.session\_state\["messages"] = \[{"role": "assistant", "content": "How can I help you?"}]



for msg in st.session\_state.messages:

&nbsp;   st.chat\_message(msg\["role"]).write(msg\["content"])



user\_query = st.chat\_input(placeholder="Ask anything from the database")



if user\_query:

&nbsp;   st.session\_state.messages.append({"role": "user", "content": user\_query})

&nbsp;   st.chat\_message("user").write(user\_query)



&nbsp;   with st.chat\_message("assistant"):

&nbsp;       streamlit\_callback = StreamlitCallbackHandler(st.container())

&nbsp;       response = agent.run(user\_query, callbacks=\[streamlit\_callback])

&nbsp;       st.session\_state.messages.append({"role": "assistant", "content": response})

&nbsp;       st.write(response)

```



---



\## 📝 License



Add your preferred license here, for example:



```

MIT License

```



---



\## 🙌 Credits



\- App logic \& UI built with \*\*Streamlit\*\*  

\- SQL agent logic powered by \*\*LangChain Classic\*\* (`create\_sql\_agent`, `SQLDatabaseToolkit`)  

\- LLM responses powered by \*\*Groq ChatGroq\*\*





