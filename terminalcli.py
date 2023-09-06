import asyncio
import tkinter as tk

root = tk.Tk()

messages = []

connections = []

async def send_messages_async(message):
  """Envoi un message au serveur."""
  # Ouvre une connexion au serveur
  connection = await asyncio.open_connection("localhost", 8080)

  # Décompose les tuples de retour de la fonction asyncio.gather()
  stream_readers, stream_writers = zip(*connections)

  # Convertit le message en bytes
  message_bytes = message.encode("utf-8")

  # Envoie le message au serveur
  for i, stream_writer in enumerate(stream_writers):
    await stream_writer.write(message_bytes)
    await stream_writer.drain()

  # Attend les réponses du serveur
  data = await asyncio.gather(*[stream_reader.readuntil(b"\n") for stream_reader in stream_writers])

  # Affiche les réponses du serveur
  for i, message in enumerate(messages):
    print(data[i].decode())

  # Ferme les StreamWriters
  await asyncio.gather(*[stream_writer.close() for stream_writer in stream_writers])


def main():
  """Créer une zone de texte pour saisir le message et l'envoyer au serveur."""
  # Crée une zone de texte pour saisir le message
  entry = tk.Entry(root)

  # attache un écouteur d'événement à la zone de texte pour envoyer le message lorsque la touche `Enter` est pressée

  def on_enter_pressed(event):
    message = entry.get().strip()

    # Ouvre une connexion au serveur
    connection = asyncio.open_connection("localhost", 8083)
    connections.append(connection)

    # Envoie le message au serveur
    asyncio.run(send_messages_async(message.strip().encode("utf-8")))
    entry.delete(0, tk.END)

  entry.bind("<Return>", on_enter_pressed)

  # Place les widgets sur la fenêtre
  entry.pack()

  # Lance la boucle d'événements

  asyncio.run(root.mainloop())


if __name__ == "__main__":
  # Le call à asyncio.run() est maintenant placé ici
  asyncio.run(main())
