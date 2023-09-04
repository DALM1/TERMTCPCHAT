import tkinter as tk

root = tk.Tk()

# Crée une zone de texte pour afficher les messages
text = tk.Text(root)
text.pack()

# Crée une entrée pour saisir les messages
entry = tk.Entry(root)
entry.pack()

# Définit la fonction appelée lorsque le bouton "Envoyer" est cliqué
def send_message():
  # Récupère le message dans l'entrée
  message = entry.get()

  # Envoie le message au serveur
  send_message(socket, message)

  # Efface le message de l'entrée
  entry.delete(0, tk.END)

# Crée un bouton "Envoyer"
button = tk.Button(root, text="Envoyer", command=send_message)
button.pack()

root.mainloop()
