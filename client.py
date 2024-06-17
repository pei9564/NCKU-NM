import requests
import tkinter as tk
from tkinter import scrolledtext, filedialog
from PIL import Image, ImageTk
import io

def send_message():
    message = entry.get()
    if message.lower() == 'exit':
        root.destroy()
        return

    response = requests.post(server_url, json={'message': message})

    if response.status_code == 200:
        data = response.json()
        print(data)
        log.insert(tk.END, f"Header: {data['log']['headers']}\n")
        log.insert(tk.END, f"-----------------------------------------\n")        
        log.insert(tk.END, f"From: {data['log']['source']}\n")
        log.insert(tk.END, f"To: {data['log']['destination']}\n")
        log.insert(tk.END, f"data: {data['log']['data']}\n")
        log.insert(tk.END, f"Server response: {data['response']}\n")
        log.insert(tk.END, f"=========================================\n")
    else:
        log.insert(tk.END, "Failed to send message\n")

    entry.delete(0, tk.END)

def send_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
            return

    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(server_url, files=files)

    if response.status_code == 200:
        try:
            data = response.json()
            print(data)
            log.insert(tk.END, f"Header: {data['log']['headers']}\n")
            log.insert(tk.END, f"-----------------------------------------\n")
            log.insert(tk.END, f"From: {data['log']['source']}\n")
            log.insert(tk.END, f"To: {data['log']['destination']}\n")
            log.insert(tk.END, f"data: {data['log']['data']}\n")
            log.insert(tk.END, f"Server response: {data['response']}\n")
            log.insert(tk.END, f"=========================================\n")
            filename = data.get('filename')
            
            if filename and filename.endswith('.txt'):
                file_content = requests.get(f'{server_url}/files/{filename}').text
                log.insert(tk.END, f"File Content: {file_content}\n")
                print(file_content) 
            elif filename and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_data = requests.get(f'{server_url}/files/{filename}').content
                image = Image.open(io.BytesIO(image_data))
                img = ImageTk.PhotoImage(image)
                image_label.configure(image=img)
                image_label.image = img
        except ValueError as e:
            log.insert(tk.END, "Failed to parse response\n")
            print(f"Failed to parse response: {e}")
    else:
        log.insert(tk.END, "Failed to send message\n")


root = tk.Tk()
root.title("Client Program")

frame = tk.Frame(root)
frame.pack(pady=10)

log = scrolledtext.ScrolledText(frame, width=50, height=20)
log.pack()

entry = tk.Entry(frame, width=40)
entry.pack(side=tk.LEFT, padx=10)

send_button = tk.Button(frame, text="Send Message", command=send_message)
send_button.pack(side=tk.LEFT)

file_button = tk.Button(frame, text="Send File", command=send_file)
file_button.pack(side=tk.LEFT)

image_label = tk.Label(frame)
image_label.pack()

server_url = 'http://127.0.0.1:9999/message'

root.mainloop()
