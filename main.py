import json
import bcrypt
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, ValidationError

authenticated_user = None
users = {}
categories = {}

print("Welcome to todo app")

PasswordStr = constr(min_length=6)

class User(BaseModel):
    id: int
    email: EmailStr
    password: PasswordStr
    name: Optional[str] = None


def register_user():
    name = input("Please enter your name:\n")
    email = input("Please enter your email:\n")
    password = input("Please enter your password:\n")
    try:
        user_data = User(
            id=len(users) + 1,
            name=name,
            email=email,
            password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

        user_json_data = user_data.model_dump_json() + "\n"
        with open("users.txt", "a") as f:
            f.write(user_json_data)

        print("✅ User registered successfully:")
        print(user_json_data)
    except ValidationError as e:
        print("❌ Validation failed:")
        for error in e.errors():
            print(f"  - {error['loc'][0]}: {error['msg']}")


def login_user():
    email = input("Please enter your email:\n")
    password = input("Please enter your password:\n")

    def check_user_is_logged_in(line):
        user = User.model_validate_json(line)
        if user.email == email and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            global authenticated_user
            authenticated_user = user
            return True
        return False

    read_json_file("users.txt", check_user_is_logged_in)

    if authenticated_user is None:
        print("❌ Authentication failed: invalid email or password.")
        return False
    else:
        print(f"✅ Welcome back, {authenticated_user.email}!")
        return True


def load_users_from_storage():
    def save_users_in_dict(line):
        user = User.model_validate_json(line)
        users[user.id] = user
        return False

    read_json_file("users.txt", save_users_in_dict)


def read_json_file(file_path, callback):
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    if callback(line):
                        break
                except json.JSONDecodeError as e:
                    print("❌ JSON read error:", e)
    except FileNotFoundError:
        pass


def user_info():
    if authenticated_user is None:
        print("❌ Unauthenticated")
        return
    print(authenticated_user.model_dump())


class Category(BaseModel):
    id: int
    title: str
    color: str
    userId: int


def create_category():
    title = input("Please enter title of category:\n")
    color = input("Please enter color of category:\n")

    user_id = authenticated_user.id
    id = len(categories) + 1
    category = Category(
        id=id,
        title=title,
        color=color,
        userId=user_id
    )

    categories[id] = category
    print(f"✅ Category '{title}' created for user {user_id}")


def list_categories():
    response = {}
    for key, category in categories.items():
        if category.userId == authenticated_user.id:
            response[key] = category
    if not response:
        print("❕ No categories found.")
    else:
        print("📂 Your categories:")
        for cat in response.values():
            print(f"- {cat.title} (color: {cat.color})")


# main loop
while True:
    load_users_from_storage()
    command = input("Please enter your command: ").strip().lower()

    if authenticated_user is None:
        if command not in ["r", "register-user", "l", "login"]:
            print("❗ You must be logged in.")
            continue

    match command:
        case "register-user" | "r":
            register_user()
        case "login" | "l":
            login_user()
        case "info" | "i":
            user_info()
        case "create-category":
            create_category()
        case "list-category":
            list_categories()
        case "exit" | "q":
            print("👋 Goodbye")
            break
        case _:
            print("❓ Unknown command. Please try again.")
