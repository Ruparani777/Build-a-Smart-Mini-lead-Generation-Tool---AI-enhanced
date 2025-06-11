# auth_config.py
import streamlit_authenticator as stauth

# Password hash for: demo123
hashed_pw = "$2b$12$r3XiUnT8BtYvO1FNL1/7I.FgZswLZJ1vuP3lmvYmIoh9xHTakHQxC"

credentials = {
    "usernames": {
        "roopa@example.com": {
            "name": "Roopa",
            "password": hashed_pw
        }
    }
}

def get_authenticator():
    return stauth.Authenticate(
        credentials,
        "auth_cookie",
        "some_signature_key",
        cookie_expiry_days=1
    )
