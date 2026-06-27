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
st.title("👁️ Sri Sankara Vision Care")
st.subheader("Complete Eye Care Solutions")

st.success("🌟 Welcome to Sri Sankara Vision Care")

st.write("""
We provide complete eye care with modern equipment,
experienced doctors and affordable treatment.

✔ Eye Checkup
✔ Cataract Screening
✔ Vision Testing
✔ Diabetic Eye Care
✔ Emergency Eye Care
""")
st.markdown("---")

# ================= ABOUT =================
st.header("🏥 About Clinic")
st.write("Advanced eye care with modern diagnosis and treatment.")

# ================= DOCTOR =================
st.header("👨‍⚕️ Doctor Profile")

col1, col2 = st.columns(2)

with col1:
    st.subheader("👨‍⚕️ Doctor")
    st.write("Dr. Y. Veera")
    st.write("Opthalmologist")


with col2:
    st.subheader("🕒 Timings")
    st.write("9:00 AM - 11:30 PM")

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
st.markdown(
"""
### Sri Sankara Vision Care

📍 Sri Surya Complex, Shabul Bazar, Bandar Road, Challapalli

📞 7793927222

📧 srisankaravisioncare@gmail.com
"""
)

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

    if not name or not phone or not problem:
        st.warning("Please fill all fields")

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
        cursor.close()
        conn.close()

        st.success(f"Appointment Booked! ID: {appointment_id}")

    
        

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
        if cursor.rowcount > 0:

            st.success("Deleted successfully")
        else:
            st.warning("Appointment ID not found")
        cursor.close()
        conn.close()

        # ================= UPDATE =================
        st.subheader("✏️ Update Appointment")

        update_id = st.text_input("Appointment ID to Update")

        
        new_phone = st.text_input("New Phone")
        new_problem = st.text_area("New Problem")

        if st.button("Update"):
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE appointments
                SET phone=%s, problem=%s
                WHERE appointment_id=%s
            """, (new_phone, new_problem , update_id))

            conn.commit()
            conn.close()
        if cursor.rowcount > 0:

            st.success("Updated successfully")
        else:
            st.warning("Appointment ID not found")

        # ================= DOWNLOAD =================
        st.subheader("📥 Download Appointments")

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download CSV",
            csv,
            "appointments.csv",
            "text/csv"
        ) 