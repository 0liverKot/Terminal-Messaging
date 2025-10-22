import json

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
            
            username = input('''
            Enter a username: ''')

            password =  input('''
            Enter a password: ''')

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