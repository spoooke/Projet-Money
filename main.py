import requests

# Dictionnaire des devises avec un exemple de nom pour simplification
devises = {
    'EUR': 'Euro (Europe)',
    'USD': 'Dollar Américain (États-Unis)',
    'CNY': 'Yuan Chinois (Chine)',
    'JPY': 'Yen Japonais (Japon)',
    'NOK': 'Couronne Norvégienne (Norvège)',
    'ZAR': 'Rand Sud-Africain (Afrique du Sud)',
    # 'ESP': 'Peseta Espagnole' est dépréciée puisque l'Espagne utilise l'euro.
}

# Fonction pour obtenir les taux de change
def get_exchange_rates(api_key, base_currency, symbols):
    response = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key={api_key}&base={base_currency}&symbols={symbols}")
    if response.status_code != 200:
        response_json = response.json()
        error_message = response_json.get('error', {}).get('info', 'Une erreur s’est produite lors de la récupération des données.')
        raise Exception(f"Erreur {response.status_code}: {error_message}")
    return response.json()['rates']

# Fonction principale
def main():
    # Chargement de la clé API à partir d'un fichier
    with open('/home/spooke/Documents/Projet_Money/API.txt', 'r') as file:
        api_key = file.readline().strip()

    # Affichage des devises disponibles à partir du dictionnaire prédéfini
    print("Voici une liste des devises disponibles et leurs noms complets :\n")
    for currency, name in devises.items():
        print(f"{currency} - {name}")
    print("\n") # Ajouter une ligne vide pour la clarté

    # Saisie utilisateur
    base_currency = input("Entrez le code de la devise de départ (ex: EUR): ").upper()
    if base_currency not in devises:
        print("Code de devise de départ non reconnu. Veuillez réessayer.")
        return

    target_currency = input("Entrez le code de la devise d'arrivée (ex: USD): ").upper()
    if target_currency not in devises:
        print("Code de devise d'arrivée non reconnu. Veuillez réessayer.")
        return

    try:
        amount = float(input("Entrez le montant à convertir (ex: 100): "))
    except ValueError:
        print("Vous n'avez pas entré un nombre valide.")
        return

    # Conversion et affichage du résultat
    try:
        rates = get_exchange_rates(api_key, base_currency, target_currency)
        converted_amount = rates[target_currency] * amount
        print(f"\n{amount} {base_currency} est égal à {converted_amount:.2f} {target_currency}.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
