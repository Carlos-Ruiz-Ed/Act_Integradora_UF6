import streamlit as st
import datetime 
from Incident_Reports import *

st.set_page_config(
    page_title='Contact Police',
)

st.markdown("### Contact Police / Make a Report")
user_name = st.text_input("Your Name")
user_email = st.text_input("Your Email (optional)")
user_phone = st.text_input("Your Phone Number")
incident_location = st.text_input("Incident Location ")

incident_date = st.date_input("Incident Date", datetime.datetime.now())

report_details = st.text_area("Report Details", height=100)

submit_button = st.button("Submit Report")

def save_report(user, email, phon, location, details, date):

    with open('reports.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        # Escribe una nueva fila con la información de la denuncia
        writer.writerow([user, email, phon, location, details, date])


if submit_button:
    if not user_name or not report_details or not user_phone or not incident_location:
        st.error("Pease fill all the required fields")
    else:
        save_report(user_name, user_email, user_phone, incident_location, report_details, incident_date)
        st.success("Report saved succesfully!")
