import streamlit as st
import requests
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

BACKEND = "http://127.0.0.1:8000"

st.set_page_config(page_title="NoteGen AI", layout="wide")
st.title("🧠 NoteGen AI ")


# ---------------- PDF Helper ---------------- #
def make_pdf_bytes(text: str):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50
    pdf.setFont("Helvetica", 11)

    for line in text.split("\n"):
        pdf.drawString(50, y, line)
        y -= 15
        if y < 50:
            pdf.showPage()
            y = height - 50

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


# ---------------- Session State ---------------- #
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None


# ---------------- LOGIN / SIGNUP ---------------- #
if st.session_state.user_id is None:
    st.sidebar.header("Login / Signup")
    mode = st.sidebar.radio("Select option", ["Login", "Signup"])

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    # Signup
    if mode == "Signup" and st.sidebar.button("Create Account"):
        res = requests.post(f"{BACKEND}/signup", json={"username": username, "password": password}).json()

        if "message" in res:
            st.success("✅ Account created! Please log in.")
        else:
            st.error("❌ Username already exists.")

    # Login
    if mode == "Login" and st.sidebar.button("Login"):
        res = requests.post(f"{BACKEND}/login", json={"username": username, "password": password}).json()

        if "user_id" in res:
            st.session_state.user_id = res["user_id"]
            st.session_state.username = username
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

    st.stop()


# ---------------- LOGGED IN UI ---------------- #
st.sidebar.success(f"✅ Logged in as **{st.session_state.username}**")

if st.sidebar.button("Logout"):
    st.session_state.user_id = None
    st.session_state.username = None
    st.rerun()


# ---------------- Tabs ---------------- #
tab1, tab2 = st.tabs(["✍️ Generate Notes", "📚 Your Saved Notes"])


# ---------------- TAB 1 - Generate Notes ---------------- #
with tab1:
    text = st.text_area("Enter text to convert into notes:", height=220)

    if st.button("✨ Generate Notes"):
        if text.strip():
            res = requests.post(
                f"{BACKEND}/generate_notes",
                json={"user_id": st.session_state.user_id, "text": text}
            ).json()

            notes_text = res.get("notes", "")
            st.text_area("Generated Notes", value=notes_text, height=280)

            # Download TXT
            st.download_button(
                "📄 Download as TXT",
                data=notes_text.encode("utf-8"),
                file_name="notes.txt",
                mime="text/plain"
            )

            # Download PDF
            pdf_bytes = make_pdf_bytes(notes_text)
            st.download_button(
                "📝 Download as PDF",
                data=pdf_bytes,
                file_name="notes.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ Please enter some text before generating notes.")


# ---------------- TAB 2 - Saved Notes ---------------- #
with tab2:
    res = requests.get(f"{BACKEND}/notes/{st.session_state.user_id}").json()
    notes = res.get("notes", [])

    if not notes:
        st.info("📄 No saved notes yet. Generate some in the first tab!")
    else:
        for content, created_at in notes:
            created_at = str(created_at)[:19]  # Clean timestamp
            with st.expander(f"🕒 Saved on {created_at}"):
                st.write(content)




