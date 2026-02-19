import json
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials





app = Flask(__name__)

def connecter_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # On vérifie si on est sur Render (via une variable d'environnement)
    google_creds_json = os.environ.get("GOOGLE_CREDS_JSON")
    
    if google_creds_json:
        # Si on est sur Render, on utilise la variable d'environnement
        creds_dict = json.loads(google_creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    else:
        # Si on est en local, on utilise le fichier physique
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        
    client = gspread.authorize(creds)
    return client.open("Pointage UMAC").sheet1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pointer', methods=['POST'])
def pointer():
    try:
        data = request.json
        nom = data.get('nom')
        lat = data.get('lat')
        lng = data.get('long')
        
        # Date et Heure générées par le serveur (plus sûr)
        maintenant = datetime.now()
        date_str = maintenant.strftime("%d/%m/%Y")
        heure_str = maintenant.strftime("%H:%M:%S")

        # Enregistrement dans Google Sheets
        feuille = connecter_google_sheets()
        feuille.append_row([nom, date_str, heure_str, lat, lng])

        return jsonify({"status": "success", "message": f"Merci {nom}, pointage réussi !"})
    
    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({"status": "error", "message": "Erreur lors de l'enregistrement."}), 500
  
if __name__ == '__main__':
    # Configuration pour le déploiement sur Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
