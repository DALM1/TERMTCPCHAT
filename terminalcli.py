import asyncio
import tkinter as tk

root = tk.Tk()

def main():
  # Crée une zone de texte pour saisir le message
  entry = tk.Entry(root)

  # attache un écouteur d'événement à la zone de texte pour envoyer le message lorsque la touche `Enter` est pressée, seulement si la zone de texte a une valeur
  entry.bind("<Return>", lambda event: asyncio.run(send_message(message=entry.get().strip() or b"")))

  # Place les widgets sur la fenêtre
  entry.pack()

  # Lance la boucle d'événements
  asyncio.run(root.mainloop())

async def send_message(message=None):
  # Envoie le message au serveur
  connection = await asyncio.open_connection("localhost", 8080)

  # Décompose le tuple de retour de la fonction asyncio.open_connection()
  stream_reader, stream_writer = connection

  # Convertit le message en bytes
  message_bytes = asyncio.coalesce(message.encode("utf-8"), b"")

  # Envoie le message au serveur en utilisant le StreamWriter
  await stream_writer.write(message_bytes)
  await stream_writer.drain()

  # Attend la réponse du serveur
  data = await stream_reader.readuntil(b"\n")

  # Affiche la réponse du serveur
  print(data.decode())

  # Ferme le StreamWriter
  await stream_writer.close()

if __name__ == "__main__":
  asyncio.run(main())