import streamlit as st
import mysql.connector
import pandas as pd

# ================= MYSQL CONNECTION =================
def get_connection():
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        port=int(st.secrets["DB_PORT"]),
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"]
    )
# ================= PAGE SETTINGS =================
st.set_page_config(
    page_title="Sri Sankara Vision Care",
    page_icon="👁️",
    layout="wide"
)

# ================= HEADER =================
st.title("👁️ Sri Sankara Vision Care")
st.subheader("Complete Eye Care Solutions")

st.markdown("---")

# ================= ABOUT =================
st.header("🏥 About Clinic")
st.write("Advanced eye care with modern diagnosis and treatment.")

# ================= DOCTOR =================
st.header("👨‍⚕️ Doctor Profile")
st.write("Dr. Y. Veera")
st.write("Ophthalmologist")

# ================= SERVICES =================
st.header("🩺 Services")
st.write("""
✔ Eye Checkup  
✔ Vision Testing  
✔ Cataract Screening  
✔ Glass Prescription  
✔ Diabetic Eye Care  
✔ Emergency Eye Care  
""")

# ================= WORKING HOURS =================
st.header("🕒 Working Hours")
st.info("Sunday - Saturday: 9:00 AM to 11:30 PM")

# ================= CONTACT =================
st.header("📞 Contact Information")
st.write("📍 Sri Surya Complex, Challapalli")
st.write("📱 7793927222")
st.write("📧 srisankaravisioncare@gmail.com")

st.markdown("---")

# ================= ADMIN LOGIN =================
st.sidebar.title("🔐 Admin Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

admin_logged_in = (username == "admin" and password == "eyeclinic123")

if admin_logged_in:
    st.sidebar.success("Login Successful")
elif username or password:
    st.sidebar.error("Invalid Credentials")

# ================= BOOK APPOINTMENT =================
st.header("📅 Book Appointment")

name = st.text_input("Patient Name")
phone = st.text_input("Phone Number")
age = st.number_input("Age", 1, 120)
date = st.date_input("Appointment Date")
problem = st.text_area("Eye Problem")

if st.button("Book Appointment"):

    if name and phone and problem:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM appointments")
        count = cursor.fetchone()[0]

        appointment_id = "APT" + str(1001 + count)

        cursor.execute("""
            INSERT INTO appointments
            (appointment_id, name, phone, age, appointment_date, problem)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (appointment_id, name, phone, age, date, problem))

        conn.commit()
        conn.close()

        st.success(f"Appointment Booked! ID: {appointment_id}")

    else:
        st.warning("Please fill all fields")

# ================= ADMIN DASHBOARD =================
if admin_logged_in:

    st.header("📊 Admin Dashboard")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM appointments")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    st.metric("Total Appointments", len(data))

    if data:

        df = pd.DataFrame(data, columns=[
            "ID",
            "Appointment ID",
            "Name",
            "Phone",
            "Age",
            "Appointment Date",
            "Problem"
        ])

        st.subheader("📋 Appointments")
        st.dataframe(df, use_container_width=True)

        # ================= SEARCH =================
        st.subheader("🔍 Search Patient")
        search = st.text_input("Enter Name")

        if st.button("Search"):
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM appointments WHERE name LIKE %s",
                ("%" + search + "%",)
            )

            result = cursor.fetchall()
            cursor.close()
            conn.close()

            if result:
                st.dataframe(pd.DataFrame(result, columns=df.columns))
            else:
                st.warning("No patient found")

        # ================= DELETE =================
        st.subheader("🗑️ Delete Appointment")
        delete_id = st.text_input("Appointment ID")

        if st.button("Delete"):
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM appointments WHERE appointment_id=%s",
                (delete_id,)
            )

            conn.commit()
            conn.close()

            st.success("Deleted successfully")

        # ================= UPDATE =================
        st.subheader("✏️ Update Appointment")

        
        new_phone = st.text_input("New Phone")
        new_problem = st.text_area("New Problem")

        if st.button("Update"):
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE appointments
                SET phone=%s, problem=%s
                WHERE appointment_id=%s
            """, (new_phone, new_problem))

            conn.commit()
            conn.close()

            st.success("Updated successfully")

        # ================= DOWNLOAD =================
        st.subheader("📥 Download Appointments")

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download CSV",
            csv,
            "appointments.csv",
            "text/csv"
        ) 