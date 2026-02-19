from flask import Flask, render_template, request, jsonify
from datetime import datetime
import csv
import os

app = Flask(__name__)

# Nom du fichier où seront stockées les données
FICHIER_LOG = "presences.csv"

# Créer le fichier avec les entêtes s'il n'existe pas encore
if not os.path.exists(FICHIER_LOG):
    with open(FICHIER_LOG, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Nom", "Date", "Heure", "Latitude", "Longitude"])

@app.route('/')
def index():
    # Cette fonction envoie ton fichier HTML au navigateur
    return render_template('index.html')

@app.route('/pointer', methods=['POST'])
def pointer():
    # On récupère les données envoyées par le formulaire (JSON)
    data = request.json
    nom = data.get('nom')
    lat = data.get('lat')
    lng = data.get('long')
    
    # On génère la date et l'heure côté serveur (plus fiable que le téléphone)
    maintenant = datetime.now()
    date_str = maintenant.strftime("%d/%m/%Y")
    heure_str = maintenant.strftime("%H:%M:%S")

    # On enregistre dans le fichier CSV
    with open(FICHIER_LOG, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([nom, date_str, heure_str, lat, lng])

    return jsonify({"message": f"Merci {nom}, pointage réussi à {heure_str} !"})

if __name__ == '__main__':
    # On lance le serveur en mode debug pour voir les erreurs
    app.run(debug=True)

if __name__ == '__main__':
    # On récupère le port donné par l'hébergeur, sinon on utilise 5000
    port = int(os.environ.get("PORT", 5000))
    # On désactive le mode debug et on autorise toutes les adresses (0.0.0.0)
    app.run(host='0.0.0.0', port=port)