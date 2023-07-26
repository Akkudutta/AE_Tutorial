from deta import Deta
import streamlit as st
import datetime
import re
import streamlit_authenticator as stauth
import os
from dotenv import load_dotenv


#Load Environment Variable
load_dotenv('.env')

DETA_KEY = os.getenv("DETA_KEY")
deta = Deta(DETA_KEY)

db = deta.Base('Studentdata')

def insert_user(email, name, username, password):
    """ 
    Inserts Users into the db
    :param email:
    :param name:
    :param username:
    :param password:
    :return User upon successful Creation:
    """
    date_joined = str(datetime.datetime.now())

    return db.put({'key':email,'name':name, 'username':username, 'password':password, 'date_joined':date_joined})

def fetch_users():
    """
    Fetch Users
    :return Dictionary of users:
    """
    users = db.fetch()
    return users.items

def get_user_emails():
    """
    Fetch user emails
    :return List of user emails:
    """
    users = db.fetch()
    emails = []
    for user in users.items:
        emails.append(user['key'])
    return emails

def get_usernames():
    """
    Fetch Usernames
    :return List of user usernames:
    """
    users = db.fetch()
    usernames = []
    for user in users.items:
        usernames.append(user['key'])
    return usernames

def validate_email(email):
    """
    Check Email Validity
    :param Email:
    :return True if email is valid els False:
    """
    pattern = "^[a-zA-Z0-9-_.]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"

    if re.match(pattern, email):
        return True
    return False

def validate_username(username):
    """
    Check validity of Username
    :param Username:
    :return True if username is valid else False:
    """
    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False

def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        c1,c2,c3 = st.columns((2,1,2))
        with c2:
            st.subheader('Sign Up')
        name = st.text_input('Name', placeholder= "Enter Your Full Name")
        email = st.text_input('Email', placeholder= 'Enter Your Email Id')
        username = st.text_input('Username', placeholder= 'Enter A Username')
        password1 = st.text_input('Password', placeholder= 'Enter A Password', type= 'password')
        password2 = st.text_input('Confirm Password', placeholder= 'Confirm Your Password', type= 'password')

        if name:
            if email:
                if validate_email(email):
                    if email not in get_user_emails():
                        if validate_username(username):
                            if username not in get_usernames():
                                if len(username) >= 3:
                                    if len(password1) >= 8:
                                        if password1 == password2:
                                            # Add user to DB
                                            hashed_password = stauth.Hasher([password2]).generate()
                                            insert_user(email, name,username,hashed_password[0])
                                            st.success(f"Congratulations **{name}**!! You have successfully signed up.")
                                            st.balloons()
                                        else:
                                            st.warning("Passwords do not match")
                                    else:
                                        st.warning("Password has to be atleast 8 characters!!")
                                else:
                                    st.warning("Username has to be atleast 3 characters!!")
                            else:
                                st.warning("Username Already Exists!!")
                        else:
                            st.warning("Invalid Username")
                    else:
                        st.warning("Email Already exists!!")
                else:
                    st.warning("Invalid Email Id")
            else:
                st.warning("Please Enter Your Email")
        else:
            st.warning("Please Enter Your Name")

        l1,l2,l3,l4,l5 = st.columns(5)
        with l5:
            st.form_submit_button("Sign Up")
#sign_up()
