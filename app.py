import streamlit as st
import ollama

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="InternBuddy AI",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #eef2ff 0%, #f8fafc 100%);
}

/* Main header */
.main-header {
    text-align: center;
    padding: 25px 10px 15px 10px;
}

.main-header h1 {
    color: #4f46e5;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.main-header p {
    color: #64748b;
    font-size: 17px;
}

/* Chat box */
.chat-area {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 20px;
    padding: 20px;
    margin-top: 15px;
    box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.08);
}

/* AI message */
.ai-message {
    background: #eef2ff;
    color: #1e293b;
    padding: 16px;
    border-radius: 18px 18px 18px 5px;
    margin: 15px 0;
    line-height: 1.6;
}

/* User message */
.user-message {
    background: #4f46e5;
    color: white;
    padding: 16px;
    border-radius: 18px 18px 5px 18px;
    margin: 15px 0;
    line-height: 1.6;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #1e1f2b;
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* Input */
.stChatInput {
    border-radius: 15px;
}

/* Buttons */
.stButton button {
    border-radius: 12px;
    font-weight: 600;
}

/* Error box */
.error-box {
    background: #fee2e2;
    color: #991b1b;
    padding: 15px;
    border-radius: 12px;
    margin-top: 15px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="main-header">

<h1>🤖 InternBuddy AI</h1>

<p>
Your friendly AI companion for internships & career guidance 🚀
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content":
            "Hi there! 👋 I'm InternBuddy!\n\n"
            "I can help you with internships, resumes, "
            "skills, projects and interview preparation.\n\n"
            "What would you like help with? 😊"
        }
    ]


# =========================================================
# DISPLAY CHAT
# =========================================================

st.markdown('<div class="chat-area">', unsafe_allow_html=True)

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                👤 <b>You</b><br><br>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        # Convert new lines to HTML
        ai_text = message["content"].replace("\n", "<br>")

        st.markdown(
            f"""
            <div class="ai-message">
                🤖 <b>InternBuddy</b><br><br>
                {ai_text}
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# CHAT INPUT
# =========================================================

question = st.chat_input(
    "Ask me anything about internships..."
)


# =========================================================
# AI RESPONSE
# =========================================================

if question:

    # Add user question
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Show loading
    with st.spinner("🤖 InternBuddy is thinking..."):

        try:

            response = ollama.chat(
                model="llama3.2",

                messages=[
                    {
                        "role": "system",
                        "content": """
You are InternBuddy, a friendly and supportive AI career assistant.

Your main purpose is to help students with internships and careers.

You can help with:

1. Finding internships
2. Creating resumes
3. LinkedIn profiles
4. GitHub profiles
5. Technical skills
6. Soft skills
7. Interview preparation
8. Project ideas
9. Career roadmaps
10. Internship applications

Always:

- Be friendly 😊
- Be encouraging
- Use simple English
- Give practical advice
- Give step-by-step guidance when useful
- Keep answers reasonably short
- Talk like a helpful friend and mentor

If the student is confused, explain things simply.

Do not give unnecessarily complicated answers.
"""
                    },

                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            # Get AI answer
            answer = response["message"]["content"]

            # Save answer
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            # Refresh page
            st.rerun()

        except Exception as e:

            st.error("❌ Unable to connect to Ollama.")

            st.warning(
                "Please make sure Ollama is installed, "
                "running and llama3.2 is available."
            )

            st.code(str(e))


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 InternBuddy")

    st.write(
        "Your personal AI companion for starting your career."
    )

    st.divider()

    st.subheader("💡 Try asking")

    st.write("🎯 How can I get my first internship?")

    st.write("📄 How do I make a resume?")

    st.write("💻 What skills should I learn?")

    st.write("🧑‍💼 How do I prepare for interviews?")

    st.write("🚀 Give me some project ideas")

    st.write("🐙 How can I improve my GitHub profile?")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content":
                "Hi again! 👋 What would you like to work on today?"
            }
        ]

        st.rerun()
