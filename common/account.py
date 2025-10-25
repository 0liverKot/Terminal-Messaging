import json
import requests
from server.db.database import ROOT_URL
from server.routes.users import Users

class Account:

    username = None
    password = None

    def __init__(self) -> None:
        
        try: 
            with open("common/userdetails.json", "r") as file:
                details = json.loads(file.read())
                self.set_username(details["username"])
                self.set_password(details["password"])

        except:            
            # attempts to create a userdetails.json file if it doesn't exist
            # then __init__ runs again which will raise an exception prompting application for you to enter details
            file = open("common/userdetails.json", "w")
            details_template = '{"username": "", "password": ""}'
            file.write(details_template)
            file.close()
            self.__init__()


        if(self.get_username() == ""):
            
            while True:
                username = input("\n        Enter a username: ")

                # validate username
                response = requests.get(f"{ROOT_URL}users/get_user/{username}")
                if(response.json() is not None):
                    print("\n   Username is already taken \n")
                    continue 
                if(not username.isalnum()):
                    print("\n   Username must only contain alphanumeric characters \n")
                    continue 
                if(len(username) > 15): 
                    print("\n   Username must not be over 15 characters long \n")
                    continue 

                break

            password = input("\n        Enter a password: ")
            
            response = requests.post(f"{ROOT_URL}users/create", json={"username": username, "password": password})

            if(response.status_code == 500):
                print("\n Internal Server Error \n")
                exit()

            self.set_username(username)
            self.set_password(password)


    def set_username(self, username):
        self.username = username

        if username == "":
            return 

        with open("common/userdetails.json", "r") as file:
            details = json.load(file)
        
        details["username"] = username

        with open("common/userdetails.json", "w") as file:
            file.write(json.dumps(details))


    def get_username(self):
        return self.username
    

    def set_password(self, password):
        self.password = password
        
        if password == "":
            return

        with open("common/userdetails.json", "r") as file:
            details = json.load(file)
        
        details["password"] = password
        
        with open("common/userdetails.json", "w") as file:
            file.write(json.dumps(details))


    def get_password(self):
        return self.password



if __name__ == "__main__":
    account = Account()
    print(f"""
    username: {account.get_username()}
    password: {account.get_password()}
    """)    