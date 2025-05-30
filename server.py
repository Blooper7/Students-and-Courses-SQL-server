from dataAccess import DataAccess
from http.server import HTTPServer, BaseHTTPRequestHandler

class Server(BaseHTTPRequestHandler):
    address="10.140.4.100" #"10.140.4.121"
    port=80
    print(DataAccess().get_all_student_data())
    print(DataAccess().get_all_course_data())
    
    def do_GET(self):
        try:
            self.send_response(200)
            message="Connected\n"
            self.end_headers()
            self.wfile.write(bytes(message, 'utf-8'))
        except:
            print("Unable to connect\n")
    
    def do_POST(self):
        
        '''
        Paths:
            /get?firstName=firstName&lastName=lastName&id=id
            /add?firstName=firstName&lastName=lastName
            /del?firstName=firstName&lastName=lastName
        '''
        
        print("POST request recieved")
        self.send_response(200)
        
        
        self.send_header("Acess-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/text")
        self.end_headers()

        content_len=int(self.headers.get("Content-Length"))
        body=self.rfile.read(content_len)
        print(f"Path: {self.path}")
        print(f"Recieved data: {body}")

        message="Got it!"
        if self.path=="/whoami":
            message="I'm Sam's SQL server!"
            
        elif self.path=="/get":
            message=f"[Tables: {DataAccess().get_table_names()}]\n"
            
            if "Students" in body.decode('utf-8'):
                data=DataAccess().get_all_student_data()
                headers=["ID", "First Name", "Last Name"]
            elif "Courses" in body.decode('utf-8'):
                data=DataAccess().get_all_course_data()
                headers=["ID", "Course Code", "Course Name"]
            
            
            message+=f"{headers[0]:<5} {headers[1]:<12} {headers[2]:<12}\n"
            #print(message)
            message+="-"*30
            message+="\n"
            #print(message)
            
            for row in data:
                message+=f"{row[0]:<5} {row[1]:<12} {row[2]:<12}\n"
                
        elif self.path=="/get-schedule":
            data=body.decode('utf-8')
            message=""
            try:
                schedule=DataAccess().get_student_schedule(data)
               #schedule=DataAccess().make_schedule_references(schedule)
                message+=f"\nSchedule for {schedule[0][0]}\n"
                message+="-"*30
                message+="\n"
                for i in schedule:
                    message+=f"{i[1]}\n"
            except Exception as ex:
                message=f"Couldn't get schedule for student #{data}:\n{ex}"
                print(ex)
        
        elif self.path=="/schedules":
            message=""
            headers=["Student Name", "Course"]
            data=DataAccess().get_all_schedules()
            data=DataAccess().make_schedule_references(data)
            
            message+=f"{headers[0]:<12} {headers[1]:<12}\n"
            message+="-"*30
            message+="\n"
            
            for row in data:
                message+=f"{row[0]:<12} {row[1]:<12}\n"
            
        
        elif self.path=="/add":
            data=body.decode('utf-8').split(",")
            message=f"{data[0]}, {data[1]}"
            print(f"Data: {data}")
            ''' #Shouldn't need this anymore
            for i in range(len(data)):
                data[i]=data[i].split("=")[1]
            '''
            try:
                if data[0]=="Students":
                    DataAccess().create_student(data[1], data[2])
                    message=f"Successfully created student {data[1]} {data[2]}"
                elif data[0]=="Courses":
                    DataAccess().create_course(data[1], data[2])
                    message=f"Successfully created course {data[1]} {data[2]}"
                elif data[0]=="Schedules":
                    DataAccess().create_schedule_item(data[1], data[2])
                    message=f"Successfully created schedule item with course id '{data[2]}' for student #{data[1]}"
                    
            except Exception as ex:
                message=f"Couldn't create item:\n{ex}"
                print(ex)
                
        elif self.path=="/del":
            data=body.decode('utf-8').split(",")
            message=f"{data[0]}, {data[1]}"
            '''
            for i in range(len(data)):
                data[i]=data[i].split("=")[1]
            '''
            try:
                if data[0]=="Students":
                    DataAccess().delete_student(data[1], data[2])
                    message=f"Successfully deleted student {data[1]} {data[2]}"
                elif data[0]=="Courses":
                    DataAccess().delete_course(data[1], data[2])
                    message=f"Successfully deleted course {data[1]} {data[2]}"
                elif data[0]=="Schedules":
                    DataAccess().delete_schedule_item(data[1], data[2])
                    message=f"Successfully deleted schedule item with course id '{data[2]}' from student #{data[1]}"
                    
            except Exception as ex:
                message=f"Couldn't delete student:/n{ex}"
                print(ex)
        
        if data==[]:
            message="Empty table!\n"
        print(f"Sent back:\n{message}")
        self.wfile.write(bytes(message,'utf-8'))
        print("Completed POST request")
        
if __name__ == "__main__":
    httpd = HTTPServer((Server.address, Server.port), Server)
    print("Server started.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Keyboard interrupt. Stopping server")
    finally:
        print("Closing server")
        httpd.server_close()
        httpd.socket.close()
