import socket
import threading
import tkinter as tk
import asyncio
import sqlite3


def send_message(message):
  client_socket.send(message.encode())


def receive_messages():
  while True:
    message = client_socket.recv(1024).decode()

    # Enregistre le message dans la base de données
    db = sqlite3.connect("chat.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (username, message))
    db.commit()

    # Affiche le message dans la fenêtre tk
    root.insert("end", message + "\n")


host = "localhost"
port = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Importe le module simpledialog
import tkinter.simpledialog

# Demande le nom d'utilisateur à l'utilisateur
username = tkinter.simpledialog.askstring("Nom d'utilisateur", "Entrez votre nom d'utilisateur :")
client_socket.send(username.encode())
print("\n")

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Crée une fenêtre Tk
root = tk.Tk()

# Crée une zone de texte pour saisir le message
entry = tk.Entry(root)

# attache un écouteur d'événement à la zone de texte pour envoyer le message lorsque la touche `Enter` est pressée

def on_enter_pressed(event):
  global entry

  message = entry.get().strip()

  # Envoie le message au serveur
  send_message(message)
  entry.delete(0, tk.END)

# Place les widgets sur la fenêtre
entry.pack(fill="both", expand=True)

root.geometry("800x600")

# Lance la boucle d'événements

asyncio.run(root.mainloop())

# Ferme la connexion au serveur
client_socket.close()
