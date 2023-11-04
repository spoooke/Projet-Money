import tkinter as tk
from tkinter import messagebox
import requests

# Dictionnaire des devises avec un exemple de nom pour simplification
devises = {
    'EUR': 'Euro (Europe)',
    'USD': 'Dollar Américain (États-Unis)',
    'CNY': 'Yuan Chinois (Chine)',
    'JPY': 'Yen Japonais (Japon)',
    'NOK': 'Couronne Norvégienne (Norvège)',
    'ZAR': 'Rand Sud-Africain (Afrique du Sud)',
}

# Fonction pour obtenir les taux de change
def get_exchange_rates(api_key, base_currency, symbols):
    response = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key={api_key}&base={base_currency}&symbols={symbols}")
    if response.status_code != 200:
        response_json = response.json()
        error_message = response_json.get('error', {}).get('info', 'Une erreur s’est produite lors de la récupération des données.')
        raise Exception(f"Erreur {response.status_code}: {error_message}")
    return response.json()['rates']

# Fonction pour la conversion avec interface utilisateur
def convert_with_ui(from_currency, to_currency, amount):
    try:
        # Lire la clé API du fichier
        with open('/home/spooke/Documents/Projet_Money/API.txt', 'r') as file:
            api_key = file.readline().strip()
        
        rates = get_exchange_rates(api_key, from_currency, to_currency)
        converted_amount = rates[to_currency] * amount
        result_var.set(f"{amount} {from_currency} est égal à {converted_amount:.2f} {to_currency}.")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def on_convert():
    from_currency = from_currency_var.get()
    to_currency = to_currency_var.get()
    amount_str = amount_entry.get()
    
    try:
        amount = float(amount_str)
    except ValueError:
        messagebox.showerror("Erreur", "Entrez un montant numérique valide.")
        return
    
    convert_with_ui(from_currency, to_currency, amount)

# Configuration de l'interface graphique
root = tk.Tk()
root.title("Convertisseur de devises")
root.geometry('400x600')  # Dimension similaire à celle d'un smartphone
root.configure(bg='#003366')  # Fond bleu foncé

# Style personnalisé
label_font = ('Arial', 12, 'bold')
entry_font = ('Arial', 10, 'bold')
button_font = ('Arial', 10, 'bold')

# Variables d'interface utilisateur
from_currency_var = tk.StringVar(value='EUR')
to_currency_var = tk.StringVar(value='USD')
result_var = tk.StringVar()

# Configuration des widgets
label_options = {'bg': '#003366', 'fg': 'white', 'font': label_font}
button_options = {'bg': 'lightgreen', 'fg': 'white', 'font': button_font}

tk.Label(root, text="Devise de départ:", **label_options).pack(pady=10)
from_currency_dropdown = tk.OptionMenu(root, from_currency_var, *devises.keys())
from_currency_dropdown.config(bg='#003366', fg='white', font=button_font)
from_currency_dropdown.pack(pady=5)

tk.Label(root, text="Devise d'arrivée:", **label_options).pack(pady=10)
to_currency_dropdown = tk.OptionMenu(root, to_currency_var, *devises.keys())
to_currency_dropdown.config(bg='#003366', fg='white', font=button_font)
to_currency_dropdown.pack(pady=5)

tk.Label(root, text="Montant à convertir:", **label_options).pack(pady=10)
amount_entry = tk.Entry(root, font=entry_font, justify='center')
amount_entry.pack(pady=5)

convert_button = tk.Button(root, text="Convertir", command=on_convert, **button_options)
convert_button.pack(pady=20)

result_label = tk.Label(root, textvariable=result_var, **label_options)
result_label.pack(pady=20)

# Lancement de l'application Tkinter
root.mainloop()
