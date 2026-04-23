import streamlit as st
import pandas as pd
import re
from auth import login_user
from membership import *
from db import get_connection
from db import init_db

init_db()
st.set_page_config(page_title="Event Management System")

# session init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# login
if not st.session_state.logged_in:
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = login_user(username, password)

        if role:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

#main app
else:
    st.title("Event Management System")
    st.sidebar.header("Menu")

    menu = ["Add Membership", "Update Membership", "Reports"]

    if st.session_state.role == "admin":
        menu.append("Maintenance")

    choice = st.sidebar.selectbox("Select", menu)

    # add membership
    if choice == "Add Membership":
        st.subheader("Add Membership")

        # show success message (stable)
        if "msg" in st.session_state:
            st.success(st.session_state["msg"])
            del st.session_state["msg"]

        name = st.text_input("Name")
        email = st.text_input("Email (example: abc@gmail.com)")

        duration = st.radio(
            "Select Duration",
            ["6 months", "1 year", "2 years"],
            index=0
        )

        is_active = st.checkbox("Active Membership", value=True)

        if st.button("Submit"):
            if not name or not email:
                st.error("All fields are mandatory")

            else:
                pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

                if not re.match(pattern, email):
                    st.error("Invalid email format")

                else:
                    try:
                        mid = add_membership(name, email, duration)
                        st.session_state["msg"] = f" Membership added. ID = {mid}"
                        st.rerun()
                    except Exception as e:
                        st.error(f" Error: {e}")

    # updating membership
    elif choice == "Update Membership":
        st.subheader("Update Membership")

        mid = st.text_input("Membership ID")

        if st.button("Fetch"):
            data = get_member(mid)
            if data:
                st.write({
                    "ID": data[0],
                    "Name": data[1],
                    "Email": data[2],
                    "Duration": data[3],
                    "End Date": data[5],
                    "Status": data[6]
                })
            else:
                st.error("Member not found")

        action = st.radio("Action", ["Extend", "Cancel"])

        if st.button("Apply"):
            if not mid:
                st.error("Membership ID is required")
            else:
                try:
                    if action == "Extend":
                        extend_membership(mid)
                        st.success("Extended by 6 months")
                    else:
                        cancel_membership(mid)
                        st.success("Membership cancelled")
                except Exception as e:
                    st.error(str(e))

    # report
    elif choice == "Reports":
        st.subheader("Reports")

        conn = get_connection()
        df = pd.read_sql("SELECT * FROM Membership", conn)

        if df.empty:
            st.info("No records found")
        else:
            st.dataframe(df)

    # maintenance
    elif choice == "Maintenance":
        if st.session_state.role != "admin":
            st.error("Access Denied")
        else:
            st.subheader("Admin Maintenance")
            option = st.radio("Select Action", ["View Members", "Delete Member"])
            #view members
            if option == "View Members":
                conn = get_connection()
                df = pd.read_sql("SELECT * FROM Membership", conn)
                if df.empty:
                    st.info("No records found")
                else:
                    st.dataframe(df)  
            # delete member
            elif option == "Delete Member":
                mid = st.text_input("Enter Membership ID to delete")
                if st.button("Delete"):
                    if not mid.isdigit():
                        st.error("Enter valid numeric ID")
                    else:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                        "DELETE FROM Membership WHERE MembershipID=?",
                        (int(mid),)
                    )

                        conn.commit()
                        conn.close()
                        st.success("Member deleted")



    # logout
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()