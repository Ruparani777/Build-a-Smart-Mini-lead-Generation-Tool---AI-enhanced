import streamlit_authenticator as stauth

# Replace with your plaintext password
password = 'Ruparani@17"

# Hash the password
hashed_password = stauth.Hasher([password]).generate()[0]
print(f"Hashed password: {hashed_password}")
