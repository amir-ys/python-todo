
from dataclasses import dataclass
import dataclasses
import json


print("Welcome to todo app")
command = input("Please enter your command: ")

@dataclass
class User:
    name: str
    email: str
    password: str

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


match command :
    case "register-user" | "r" : register_user()

