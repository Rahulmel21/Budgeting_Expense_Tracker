import hashlib
import secrets
from database import add_user, get_user_by_id, get_user_by_username


def hash_password(password):
    salt = secrets.token_bytes(16)
    pwd_bytes = password.encode("utf-8")
    derived_key = hashlib.pbkdf2_hmac("sha256", pwd_bytes, salt, 100000)
    return f"{salt.hex()}${derived_key.hex()}"


def check_password(password, stored_password):
    try:
        salt_hex, target_hash = stored_password.split("$")
        salt = bytes.fromhex(salt_hex)
        pwd_bytes = password.encode("utf-8")
        computed_hash = hashlib.pbkdf2_hmac("sha256", pwd_bytes, salt, 100000).hex()
        return secrets.compare_digest(computed_hash, target_hash)
    except (ValueError, AttributeError):
        return False


def validate_registration(username, password, email):
    clean_username = username.strip()
    clean_email = email.strip()

    if not clean_username:
        return False, "Username cannot be empty."
    if not password:
        return False, "Password cannot be empty."
    if not clean_email:
        return False, "Email cannot be empty."
    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if get_user_by_username(clean_username) is not None:
        return False, "Username already exists."

    return True, "Registration details are valid."


def register_user(username, password, email):
    is_valid, msg = validate_registration(username, password, email)
    if not is_valid:
        return False, msg

    hashed_pwd = hash_password(password)
    user_id = add_user(username.strip(), hashed_pwd, email.strip())

    if user_id:
        return True, "Registration successful."
    return False, "Registration failed."


def login_user(username, password):
    user_record = get_user_by_username(username.strip())
    if not user_record:
        return False, "Username does not exist."

    if not check_password(password, user_record.get("passwordHash", "")):
        return False, "Incorrect password."

    return True, user_record.get("userID")


def get_logged_in_user(user_id):
    return get_user_by_id(user_id)


def logout_user():
    return True