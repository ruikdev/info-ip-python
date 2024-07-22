import requests
import socket
import concurrent.futures

def verifier_ip(ip):
    url = f"http://api.eris.rakuven.com:2006/get_ip?ip={ip}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"\nRésultats pour l'IP {ip}:")
            print(f"VPN: {'Oui' if data['vpn'] else 'Non'}")
            print(f"Fournisseur: {data['provider']}")
            print(f"Région: {data['region']}")
            print(f"Ville: {data['city']}")
            print(f"Pays: {data['country']}")
        else:
            print(f"Erreur lors de la requête: Code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite lors de la requête: {e}")

def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    return port if result == 0 else None

def scan_ports(ip, port_range):
    start_port, end_port = map(int, port_range.split('-'))
    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future.result()
            if port:
                open_ports.append(port)
                print(f"Port {port} : ouvert")

    return open_ports

def get_ip_from_domain(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None

def main():
    print("1: Vérifier une IP")
    print("2: Scanner les ports ouverts d'une IP")
    print("3: Obtenir l'adresse IP d'un nom de domaine")
    choix = input("Choix: ")

    if choix == "1":
        print("Vérification d'adresse IP VPN")
        while True:
            ip = input("Entrez une adresse IP (ou 'q' pour quitter): ")
            if ip.lower() == 'q':
                break
            verifier_ip(ip)
    elif choix == "2":
        ip = input("Entrez l'adresse IP à scanner : ")
        port_range = input("Entrez la plage de ports à scanner (ex: 1-1000) : ")
        open_ports = scan_ports(ip, port_range)
        print(f"\nPorts ouverts : {open_ports}")
    elif choix == "3":
        domain = input("Entrez le nom de domaine : ")
        ip_address = get_ip_from_domain(domain)
        if ip_address:
            print(f"L'adresse IP de {domain} est {ip_address}")
        else:
            print(f"Impossible de trouver l'adresse IP pour le domaine {domain}")
    else:
        print("Choix invalide.")

main()
