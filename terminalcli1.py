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

        # Crée la base de données si elle n'existe pas
        db = sqlite3.connect("chat.db")
        if not db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'").fetchone():
            db.execute("CREATE TABLE messages (username TEXT, message TEXT)")
        db.commit()

        # Enregistre le message dans la base de données
        cursor = db.cursor()
        cursor.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (username, message))
        db.commit()

        # Affiche le message dans la fenêtre tk
        message = message.rstrip("\t").rstrip(" ")
        message = message.encode("utf-8")
        lines = message.split(b"\n")

        # Redimensionne la zone de texte à la taille du texte
        entry.config(width=max(len(line) for line in lines))

        for line in lines:
            entry.insert("end", line + b"\n")
            entry.update()


host = "localhost"
port = 8081

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
root.title("DALM1TCPCHAT")
root.configure(bg="black")

# Crée une zone de texte pour saisir le message
entry = tk.Entry(root)

# attache un écouteur d'événement à la zone de texte pour envoyer le message lorsque la touche `Enter` est pressée

def on_enter_pressed(event):
    global entry

    message = entry.get().strip() + " "

    # Envoie le message au serveur
    send_message(message)
    entry.delete(0, tk.END)
    entry.focus_set()

entry.bind("<Return>", on_enter_pressed)

# Place les widgets sur la fenêtre
entry.pack(fill="both", expand=True)

# Place le curseur en haut à gauche
entry.focus_set()

root.geometry("800x600")

# Lance la boucle d'événements

asyncio.run(root.mainloop())

# Ferme la connexion au serveur
client_socket.close()
