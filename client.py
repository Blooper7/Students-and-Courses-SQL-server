import requests as requests
import json
from dataAccess import DataAccess

class Client:
    port=80
    address = "10.140.4.121" #"10.140.4.100"
    currentTable="Students"
    
    @classmethod
    def get_data(cls):
        req=requests.get(f"http://{cls.address}:{str(cls.port)}")
        print(req.text)
        
    @classmethod
    def send_message(cls, path, message=''):
        req=requests.post(f"http://{cls.address}:{str(cls.port)}/{path}",bytes(message, 'utf-8'))
        print(req.text)
        
    ''' # URL-Based
    @classmethod
    def send_message(cls, data):
        req=requests.post(f"https://{cls.address}:{str(cls.port)}/{data}")
        print(req.text)
    '''
    
if __name__ == "__main__":
    #Client.get_data()
    #Client.send_message("/get","hello")
    #Client.send_message("/add","first=Bob&last=Ross")
    #Client.send_message("/get")
    
    print("Student & Course database")
    print("*"*30)
    
    
    while True:
        valid_commands=["a","d","t","q"]
        Client.send_message("/get",Client.currentTable)
        print("Commands:\n\ta: add item\n\td: delete item\n\tt: change tables\n\tq: quit")
        c=input(f"[{Client.currentTable}] >> ")
        if not c in valid_commands:
            print(f"Command {c} invalid")
            continue
        if c=="a":
            if Client.currentTable=="Students":
                p1=input("First name : ")
                p2=input("Last name  : ")
            elif Client.currentTable=="Courses":
                p1=input("Course code:")
                p2=input("Course name:")
            Client.send_message("/add",f"{Client.currentTable},{p1},{p2}")
        elif c=="d":
            if Client.currentTable=="Students":
                p1=input("First name : ")
                p2=input("Last name  : ")
            elif Client.currentTable=="Courses":
                p1=input("Course code: ")
                p2=input("Course name: ")
            Client.send_message("/del",f"{Client.currentTable},{p1},{p2}")
        elif c=="t":
            table=input("Table name : ")
            if table in DataAccess().get_table_names():
                Client.currentTable=table
            else:
                print("Table doesn't exist.")
        elif c=="q":
            print("Bye!")
            break
        print("\n"+("#"*30)+"\n")