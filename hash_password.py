import streamlit_authenticator as stauth

# Replace with your plaintext password
passwords = ['Ruparani@17']

hashed_passwords = stauth.Hasher(passwords).generate()
print(hashed_passwords[0])
