import streamlit as st
import io
from contextlib import redirect_stdout

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Student Admission Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    /* Gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Hide default streamlit menu */
    #MainMenu {visibility: hidden;}

    /* Hero header */
    .hero {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    .hero h1 {
        font-size: 2.8rem;
        margin: 0;
        font-weight: 800;
    }
    .hero p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 8px;
    }

    /* White card */
    .card {
        background: white;
        border-radius: 18px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        margin-top: 10px;
    }

    /* Result badge */
    .badge-success {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
        padding: 15px 25px;
        border-radius: 12px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 15px 0;
    }
    .badge-fail {
        background: linear-gradient(135deg, #eb3349, #f45c43);
        color: white;
        padding: 15px 25px;
        border-radius: 12px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ================= ORIGINAL CLASSES (UNCHANGED) =================
class students():
    def __init__(self, name, age, email, contact):
        self.name = name
        self.age = age
        self.email = email
        self.contact = contact

    def display_details(self):
        print(self.name)
        print(self.age)
        print(self.email)
        print(self.contact)


class class10Admission(students):
    def __init__(self, name, age, email, contact):
        super().__init__(name, age, email, contact)
        print("admission successful")


class class12Admission(students):
    def __init__(self, name, age, email, contact):
        super().__init__(name, age, email, contact)

        if self.age >= 16:
            print("admission successful")
        else:
            print("admission failed")


# ================= HELPER =================
def run_admission(cls, name, age, email, contact):
    """Runs the class and captures its print() output."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        student = cls(name, age, email, contact)
        student.display_details()
    lines = buffer.getvalue().strip().split("\n")
    status = lines[0]                      # first printed line = admission status
    details = lines[1:]                    # remaining lines = student details
    return status, details, student


# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🎯 Admission Type")
    choice = st.radio(
        "Select a class for admission:",
        options=["Class 10th", "Class 12th"],
        captions=["Open to all students", "Minimum age requirement: 16 years"],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### 📋 Requirements")
    st.markdown("""
    | Field | Rule |
    |-------|------|
    | 👤 Name | Required |
    | 🎂 Age | 16+ for Class 12 |
    | 📧 Email | Must contain `@` |
    | 📞 Contact | Digits only |
    """)

    # Admission history (session-based)
    if "history" not in st.session_state:
        st.session_state.history = []
    if st.session_state.history:
        st.divider()
        st.markdown("### 🕒 Recent Admissions")
        for h in reversed(st.session_state.history[-5:]):
            st.markdown(f"- **{h['name']}** → {h['status_emoji']} `{h['cls']}`")

# ================= HERO HEADER =================
st.markdown("""
<div class="hero">
    <h1>🎓 Student Admission Portal</h1>
    <p>Fast • Simple • Secure — Complete your admission in under a minute</p>
</div>
""", unsafe_allow_html=True)

# ================= ADMISSION FORM =================
with st.container():
    st.markdown(f'<div class="card">', unsafe_allow_html=True)

    st.markdown(f"### 📝 {choice} Admission Form")
    st.caption("Fill in all the details below and click **Submit**")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("👤 Full Name", placeholder="e.g. Rahul Sharma")
        email = st.text_input("📧 Email Address", placeholder="e.g. rahul@gmail.com")

    with col2:
        age = st.number_input("🎂 Age", min_value=1, max_value=100, value=15, step=1)
        contact = st.text_input("📞 Contact Number", placeholder="e.g. 9876543210")

    st.write("")
    submitted = st.button("🚀 Submit Admission", use_container_width=True, type="primary")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= RESULT SECTION =================
if submitted:
    # ---- Validation ----
    errors = []
    if not name.strip():
        errors.append("Name cannot be empty.")
    if "@" not in email or "." not in email:
        errors.append("Please enter a valid email address.")
    if not contact.isdigit() or len(contact) < 10:
        errors.append("Contact must be at least 10 digits.")
    if choice == "Class 12th" and age < 16:
        errors.append("Age must be 16 or above for Class 12th admission.")

    if errors:
        for e in errors:
            st.error(f"⚠️ {e}")
    else:
        # ---- Run admission logic ----
        with st.spinner("Processing admission... ⏳"):
            if choice == "Class 10th":
                status, details, student = run_admission(class10Admission, name, age, email, contact)
            else:
                status, details, student = run_admission(class12Admission, name, age, email, contact)

        success = "successful" in status

        # ---- Status badge ----
        if success:
            st.markdown('<div class="badge-success">🎉 Admission Successful!</div>',
                        unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown('<div class="badge-fail">❌ Admission Failed — Age requirement not met</div>',
                        unsafe_allow_html=True)

        # ---- Student detail card ----
        st.markdown("### 🪪 Student Details")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("👤 Name", details[0])
        c2.metric("🎂 Age", details[1])
        c3.metric("📧 Email", details[2])
        c4.metric("📞 Contact", details[3])

        # ---- Save to history ----
        st.session_state.history.append({
            "name": name,
            "cls": choice,
            "status_emoji": "✅" if success else "❌",
        })

        # ---- Downloadable receipt ----
        receipt = (f"--- ADMISSION RECEIPT ---\nClass: {choice}\nStatus: {status.upper()}\n"
                   f"Name: {details[0]}\nAge: {details[1]}\nEmail: {details[2]}\nContact: {details[3]}")
        st.download_button("⬇️ Download Receipt", receipt, file_name="admission_receipt.txt")

# ================= FOOTER =================
st.divider()
st.markdown(
    "<div style='text-align:center; color:white; opacity:0.85;'>"
    "🎓 Student Admission Portal &nbsp;|&nbsp; Built with Streamlit & Python OOP"
    "</div>",
    unsafe_allow_html=True,
)