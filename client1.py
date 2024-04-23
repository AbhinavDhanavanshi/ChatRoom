import threading
import socket
import argparse
import os
import sys
import customtkinter as ctk
import tkinter as tk



class Send(threading.Thread):
    
    def __init__(self, sock, name):
        super().__init__()
        self.sock=sock
        self.name=name
        
    def run(self):
        while True:
            message=input('\r{}: '.format(self.name))
            
            if message.lower()=='quit':
                self.sock.sendall('Server: {} has left the chat'.format(self.name).encode('ascii'))
                print('\nQuitting....')
                self.sock.close()
                os.exit(0)
                break
            else:
                self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))
                
        print('\nQuitting....')
        self.sock.close
        os.exit(0)    
                
class Recieve(threading.Thread):
    def __init__(self,sock,name):
        super().__init__()
        self.sock=sock
        self.name=name
        self.messages=None
        
    def run(self):
        message=self.sock.recv(1024).decode('ascii')
        
        while message:
            print('\r{}\n{}: '.format(message, self.name), end='')
            self.messages.insert(ctk.END, message)
            message=self.sock.recv(1024).decode('ascii')
            
        print('\nDisconnected from the server')
        self.sock.close()
        os.exit(0)
         
    
class Client:
    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name=None
        self.messages=None
        
    def start(self):
        print(f'Connecting to {self.host}:{self.port}')
        self.sock.connect((self.host,self.port))
        print(f'successfully connected to {self.host}:{self.port}')
        self.name=input("Enter your username: ")
        print(f'Welcome to the chat {self.name}! Ready to send messages...')
        
        send=Send(self.sock,self.name)
        receive=Recieve(self.sock, self.name)
        
        send.start()
        receive.start()
        
        self.sock.sendall('Server: {} has joined the chat'.format(self.name).encode('ascii'))
        print(f'Ready! Leave the chat anytime by typing "QUIT"')
        
        print(f'{self.name}: ', end='')
        
        return receive
    
    def send(self, textInput):
        message=textInput.get()
        textInput.delete(0,ctk.END)
        self.messages.insert(ctk.END, f'{self.name}: {message}') 
        
        if message.lower()=='quit':
            self.sock.sendall(f'Server: {self.name} has left the chat'.encode('ascii'))
            print('\nQuitting...')
            self.sock.close()
            sys.exit(0)
        else:
            self.sock.sendall(f'{self.name}: {message}'.encode('ascii'))
            
def main(host,port):
    client=Client(host,port)
    receive=client.start()
    
    window=ctk.CTk()
    window.title('Chatroom')
    window.geometry('800x600')
    window._set_appearance_mode('classic')
    # image=ctk.CTkImage('image.png')
    # window.iconphoto(False, image)

    fromMessage=ctk.CTkFrame(master=window,bg_color='#313131')
    # set frame color to dark
    scrollBar=ctk.CTkScrollbar(master=fromMessage,width=10)
    messages=tk.Listbox(master=fromMessage, yscrollcommand=scrollBar.set, bg='#313131', fg='#EEEEEE', font=('roboto', 16), selectbackground='#CA3E47',border=0,highlightbackground='#313131',highlightthickness=0,highlightcolor='#313131',activestyle='none')
    messages.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
    scrollBar.pack(side=ctk.RIGHT, fill=ctk.Y, expand=False)
    # messages.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
    # scrollBar=tk.Scrollbar(master=fromMessage, activebackground='black', bg='black',width=20, relief=tk.FLAT, troughcolor='black', bd=10)
    # messages=tk.Listbox(master=fromMessage, yscrollcommand=scrollBar.set, bg='#222831', fg='#EEEEEE', font=('roboto', 12), selectbackground='#31363F')
    # scrollBar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    # messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    client.messages=messages
    receive.messages=messages
    fromMessage.grid(row=0, column=0, columnspan=2, sticky="nsew")
    fromEntry=ctk.CTkFrame(master=window, bg_color='#313131')
    textInput=ctk.CTkEntry(master=fromEntry,bg_color='#282424', fg_color='#313131', font=('roboto', 14), placeholder_text="Enter your message here.")
    textInput.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    textInput.bind("<Return>", lambda x: client.send(textInput))
    # textInput.insert(0, "Enter your message here.")
    
    btnSend=ctk.CTkButton(
        master=window,
        text="Send",
        font=('roboto', 14),
        command=lambda: client.send(textInput),
        bg_color='#282424',
        fg_color='#313131',  # Adjust text color for better visibility
        corner_radius=10,
        hover_color='#CA3E47',
        border_color='#545c5c',
        border_width=2,
    )
    
    fromEntry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    btnSend.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    
    window.rowconfigure(0, weight=1, minsize=500)
    window.rowconfigure(1, weight=0, minsize=50)
    window.columnconfigure(0, weight=1, minsize=500)
    window.columnconfigure(1, weight=0, minsize=200)
    
    window.mainloop()
    
        
if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Chatroom Client')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=12345, help='Port the server listens at')
    args=parser.parse_args()
    
    main(args.host, args.p)