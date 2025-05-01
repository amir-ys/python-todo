from dataclasses import dataclass
import dataclasses
import json
from typing import Optional

authenticated_user = None
users = {}

print("Welcome to todo app")


class Json():
    @staticmethod
    def from_json(json_str):
     return User(**json.loads(json_str))


@dataclass
class User(Json):
    email: str
    password: str
    name: Optional[str] = None

def register_user():
     
     name = input("please enter your name : \n")
     email = input("please enter your email : \n")
     password =  input("please enter your password : \n")


     user_data = User(
        name = name , 
        email = email ,
        password =  password
    )
     
     user_json_data =  json.dumps(dataclasses.asdict(user_data)) + "\n"
     print('df')
     with open("users.txt" , "a") as f:
        f.write(user_json_data)


def login_user():
    email = input("please enter your email : \n")
    password =  input("please enter your password : \n")   

    input_user = User(
        email=email,
        password=password
    ) 

    def check_user_is_loged_in(line):
        user = User.from_json(line)
        if user.email == input_user.email and user.password == input_user.password:
            global authenticated_user
            authenticated_user = user.email
            return True
        return False
        

    read_json_file("users.txt" ,check_user_is_loged_in)

    if authenticated_user is None:
        print("authentication failed: invalid email or password.")
        return False
    else:
        print(f"welcome back, {authenticated_user}!")
        return True


def load_users_from_storage():
    def save_users_in_dic(line):
         user = User.from_json(line)
         users[user.email] = user
         return False
    
    read_json_file("users.txt" , save_users_in_dic)


def read_json_file(file_path , callback):
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
              if callback(line):
                  break
            except json.JSONDecodeError as e:
                print("خطا در خواندن JSON:", e)


def user_info():
    if authenticated_user is None:
        print("unauthenticated")
        return
    print(users[authenticated_user])

while True:
    load_users_from_storage()
    command = input("Please enter your command ")
    match command :
        case "register-user" | "r" : register_user()
        case "login" | "l" : login_user()
        case "info" | "i" : user_info()
        case "exit" | "q":
            print("goodbye")
            break
        case _:
            print("Unknown command. Please try again.")

