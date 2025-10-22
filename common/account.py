import json

class Account:

    username = None
    password = None

    def __init__(self) -> None:
        
        try: 
            with open("userdetails.json") as file:
                details = json.loads(file.read())
                self.set_username(details["username"])

        
        except:            
            # attempts to create a userdetails.json file if it doesn't exist
            # then __init__ runs again which will raise an exception prompting application for you to enter details
            file = open("userdetails.json", "w")
            details_template = '{"username": ""}'
            file.write(details_template)
            file.close()
            self.__init__()


        if(self.get_username() == ""):
            raise AttributeError(" add a username ")

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username


if __name__ == "__main__":
    account = Account()
    print(f"""
    username: {account.get_username()}
    """)    