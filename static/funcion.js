function rafraichirHorloge() {
    const horlogeElement = document.getElementById('horloge');
    const maintenant = new Date();

    // Récupération des heures, minutes, secondes
    const heures = String(maintenant.getHours()).padStart(2, '0');
    const minutes = String(maintenant.getMinutes()).padStart(2, '0');
    const secondes = String(maintenant.getSeconds()).padStart(2, '0');

    horlogeElement.textContent = `${heures}:${minutes}:${secondes}`;
    // Ligne 10 correcte :
}

// Lancer l'horloge immédiatement
rafraichirHorloge();

// Demander à JavaScript de répéter la fonction toutes les 1000ms (1 seconde)
setInterval(rafraichirHorloge, 1000);