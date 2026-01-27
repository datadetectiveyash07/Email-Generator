import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Email Generator",
    page_icon="📧",
    layout="centered"
)

# ---------------- API CONFIG ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- EMAIL TEMPLATES ----------------
TEMPLATES = {
    "Formal Request": """Subject: Request for Approval Regarding {topic}

Dear {recipient},

I hope this email finds you well.

I am writing to respectfully request your approval regarding {topic}. This request is important for {purpose}.

Please let me know if any additional information is required.

Kind regards,  
{sender}
""",

    "Follow-up": """Subject: Follow-up on {topic}

Dear {recipient},

I hope you are doing well.

I am following up on my previous email regarding {topic}. I wanted to check if there are any updates.

Looking forward to your response.

Best regards,  
{sender}
""",

    "Apology": """Subject: Apology for {topic}

Dear {recipient},

I sincerely apologize for {topic}. This was unintentional, and I take full responsibility.

Thank you for your understanding.

Sincerely,  
{sender}
""",

    "Congratulation": """Subject: Congratulations!

Dear {recipient},

Congratulations on your achievement related to {topic}. Your hard work and dedication truly deserve recognition.

Wishing you continued success.

Warm regards,  
{sender}
""",

    "Invitation": """Subject: Invitation to {topic}

Dear {recipient},

You are cordially invited to {topic}. We would be honored by your presence.

Please let us know your availability.

Best regards,  
{sender}
""",

    "Promotion": """Subject: Announcement – {topic}

Hello {recipient},

We are excited to announce {topic}. This initiative aims to bring value and new opportunities.

Feel free to reach out for more details.

Regards,  
{sender}
"""
}

# ---------------- UI ----------------
st.title("📧 AI Email Generator")
st.caption("Templates + AI-powered custom emails")

template_choice = st.selectbox(
    "📂 Choose Email Type",
    ["Custom (AI Generated)"] + list(TEMPLATES.keys())
)

topic = st.text_input("📌 Topic")
recipient = st.text_input("👤 Recipient Name", "Sir/Madam")
sender = st.text_input("✍️ Your Name", "Your Name")

tone = st.selectbox(
    "🎭 Tone",
    ["Professional", "Casual", "Motivational", "Informative"]
)

purpose = st.selectbox(
    "🎯 Purpose",
    ["Inform", "Request", "Apologize", "Follow-up", "Congratulate", "Invite", "Promote"]
)

length = st.selectbox(
    "📏 Length",
    ["Short", "Medium", "Long"]
)

politeness = st.selectbox(
    "🗣️ Politeness Level",
    ["Very polite", "Neutral", "Direct / assertive"]
)

# ---------------- TEMPLATE PREVIEW ----------------
email_text = ""

if template_choice != "Custom (AI Generated)":
    email_text = TEMPLATES[template_choice].format(
        topic=topic or "________",
        recipient=recipient,
        sender=sender,
        purpose=purpose.lower()
    )

email_text = st.text_area(
    "📝 Email Preview (Editable)",
    value=email_text,
    height=300
)

# ---------------- GENERATE AI EMAIL ----------------
if st.button("🚀 Generate / Improve with AI"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        prompt = f"""
You are an AI email writing assistant.

Improve or generate an email using the details below:

Template Type: {template_choice}
Topic: {topic}
Recipient: {recipient}
Sender: {sender}
Tone: {tone}
Purpose: {purpose}
Length: {length}
Politeness Level: {politeness}

Existing Draft (if any):
{email_text}

Ensure:
- Clear subject line
- Proper greeting
- Professional structure
- Clear closing
"""

        with st.spinner("Generating email..."):
            try:
                response = model.generate_content(prompt)
                st.subheader("📨 Final Email")
                st.text_area(
                    "Generated Email",
                    value=response.text,
                    height=350
                )

            except Exception as e:
                st.error(f"Error: {e}")
