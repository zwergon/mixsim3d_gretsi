import socket


def start_server():
    # Configuration du serveur
    HOST = '0.0.0.0'  # Écoute sur toutes les interfaces réseau
    PORT = 5000       # Port d'écoute

    # Création du socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Serveur démarré sur le port {PORT}...")

        while True:
            # Accepter une nouvelle connexion
            conn, addr = s.accept()
            with conn:
                print(f"Connexion établie depuis {addr}")
                data = conn.recv(1024)
                if data.decode().strip() == "ping":
                    print("Requête 'ping' reçue, envoi de 'pong'...")
                    conn.sendall(b"pong")
                else:
                    print(f"Requête inconnue : {data.decode().strip()}")


if __name__ == "__main__":
    start_server()
