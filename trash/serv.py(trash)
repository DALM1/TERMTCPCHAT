def main():
  """Exécute le terminal."""

  # Crée une base de données pour stocker les informations sur les clients et les discussions
  conn = sqlite3.connect("chat.db")
  cur = conn.cursor()

  # Crée une table pour stocker les clients
  cur.execute("CREATE TABLE clients (id INTEGER PRIMARY KEY, name TEXT, ip TEXT, port INTEGER)")

  # Crée une table pour stocker les discussions
  cur.execute("CREATE TABLE discussions (id INTEGER PRIMARY KEY, name TEXT, participants TEXT)")

  # Ajoute le client actuel à la table des clients
  cur.execute("INSERT INTO clients (name, ip, port) VALUES ('[Votre nom]', '127.0.0.1', 8080)")
  conn.commit()

  socket = create_socket()
  connect_to_server(socket, "localhost", 8080)

  while True:
    message = input("Entrez votre message : ")
    send_message(socket, message)

    # Récupère les messages du serveur
    data = receive_message(socket)

    # Affiche les messages du serveur
    print(data)

    # Traite les messages du serveur
    if data.startswith("NEW_CLIENT"):
      # Un nouveau client
      print("Un nouveau client s'est connecté : " + data[7:])
