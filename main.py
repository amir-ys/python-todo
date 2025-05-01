from dataclasses import dataclass
import dataclasses
import json
from typing import Optional

authenticated_user = None

print("Welcome to todo app")
command = input("Please enter your command ")

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

    with open("users.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                user = User.from_json(line)
                if user.email == input_user.email and user.password == input_user.password:
                    global authenticated_user
                    authenticated_user = user.email
                    break
            
            except json.JSONDecodeError as e:
                print("خطا در خواندن JSON:", e)
        

            
    if authenticated_user is None:
        print("authentication failed: invalid email or password.")
        return False
    else:
        print(f"welcome back, {authenticated_user}!")
        return True

     


match command :
    case "register-user" | "r" : register_user()
    case "login" | "l" : login_user()

