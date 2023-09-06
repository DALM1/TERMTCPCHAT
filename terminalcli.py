import asyncio
import tkinter as tk

root = tk.Tk()

async def send_messages_async(message):
  """Envoi un message au serveur."""
  # Ouvre une connexion au serveur
  connections = await asyncio.gather(
      *[asyncio.open_connection("localhost", 8080) for message in messages])

  # Décompose les tuples de retour de la fonction asyncio.gather()
  stream_readers, stream_writers = zip(*connections)

  # Convertit le message en bytes
  message_bytes = message.encode("utf-8")

  # Envoie le message au serveur
  for i, stream_writer in enumerate(stream_writers):
    await stream_writer.write(message_bytes)
    await stream_writer.drain()

  # Attend les réponses du serveur
  data = await asyncio.gather(*[stream_reader.readuntil(b"\n") for stream_reader in stream_readers])

  # Affiche les réponses du serveur
  for i, message in enumerate(messages):
    print(data[i].decode())

  # Ferme les StreamWriters
  await asyncio.gather(*[stream_writer.close() for stream_writer in stream_writers])


async def main():
  """Créer une zone de texte pour saisir le message et l'envoyer au serveur."""
  # Crée une zone de texte pour saisir le message
  entry = tk.Entry(root)

  # attache un écouteur d'événement à la zone de texte pour envoyer le message lorsque la touche `Enter` est pressée
  entry.bind("<Return>", lambda event: send_messages_async(entry.get().strip().encode("utf-8")))

  # Place les widgets sur la fenêtre
  entry.pack()

  # Lance la boucle d'événements

  asyncio.run(root.mainloop())


if __name__ == "__main__":
  # Le call à asyncio.run() est maintenant placé ici
  asyncio.run(main())
