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

async def send_messages(messages):
  # Envoie les messages au serveur
  connections = await asyncio.gather(*[asyncio.open_connection("localhost", 8080) for message in messages])

  # Décompose les tuples de retour de la fonction asyncio.gather()
  stream_readers, stream_writers = zip(*connections)

  # Convertit les messages en bytes
  message_bytes = [message.encode("utf-8") for message in messages]

  # Envoie les messages au serveur en utilisant les StreamWriters
  await asyncio.gather(*[stream_writer.write(message_bytes[i]) for i, stream_writer in enumerate(stream_writers)])
  await asyncio.gather(*[stream_writer.drain() for stream_writer in stream_writers])

  # Attend les réponses du serveur
  data = await asyncio.gather(*[stream_reader.readuntil(b"\n") for stream_reader in stream_readers])

  # Affiche les réponses du serveur
  for i, message in enumerate(messages):
    print(data[i].decode())

  # Ferme les StreamWriters
  await asyncio.gather(*[stream_writer.close() for stream_writer in stream_writers])


if __name__ == "__main__":
  asyncio.run(main())