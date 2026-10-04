# Dar Luce — site web

Site statique d'une page présentant la maison Dar Luce (location Airbnb au Maroc).
HTML, CSS et JavaScript purs : aucune dépendance, aucune étape de build.

## Structure

```
index.html        Contenu de la page (français)
en/index.html     Version anglaise, à tenir à jour en parallèle
css/style.css     Styles (couleurs et polices en haut du fichier)
js/main.js        Menu mobile et animations d'apparition
images/           Photos et favicon
```

## Aperçu en local

Ouvrir `index.html` dans un navigateur, ou lancer un petit serveur :

```
python -m http.server 8000
```

puis visiter http://localhost:8000.

## Contenu à compléter

Chercher `TODO` dans `index.html` et `en/index.html` : chaque élément provisoire est signalé.
Toute modification de contenu est à reporter dans les deux fichiers.

- **Textes** : présentation, capacité et équipements sont repris de l'annonce Airbnb ; les mettre à jour si l'annonce change.
- **E-mail** : l'adresse est découpée (`data-user`, `data-domain`) pour limiter le spam ; `js/main.js` la reconstitue en lien.
- **Photos** : déposer les fichiers dans `images/`, puis remplacer dans chaque bloc
  `<span>…</span>` par `<img src="images/nom.jpg" alt="Description" loading="lazy">`.
- **Photo d'accueil** : dans `css/style.css`, remplacer `--hero-photo: none;` par
  `--hero-photo: url("../images/hero.jpg");`.

Conseil : exporter les photos en JPEG ou WebP, 1600 px de large au maximum, pour garder un site rapide.

## Calendrier des disponibilités

Le workflow `.github/workflows/availability.yml` télécharge toutes les six heures le
calendrier iCal de l'annonce Airbnb (et celui de Booking.com s'il est configuré), fusionne les deux et enregistre les dates indisponibles dans
`data/availability.json` (script `scripts/update_availability.py`). La page affiche
ensuite ces dates ; sans ce fichier, la section « Disponibilités » reste masquée.

Les adresses iCal sont confidentielles : elles se règlent dans le dépôt GitHub, sous
**Settings → Secrets and variables → Actions**, secrets `AIRBNB_ICAL_URL` (obligatoire)
et `BOOKING_ICAL_URL` (facultatif).
Pour forcer une mise à jour : onglet **Actions → Mise à jour des disponibilités → Run workflow**.

## Publication sur GitHub Pages

1. Créer un dépôt sur GitHub et y pousser la branche `main`.
2. Dans le dépôt : **Settings → Pages → Build and deployment**, choisir
   **Deploy from a branch**, branche `main`, dossier `/ (root)`.
3. Le site est en ligne après une à deux minutes à l'adresse
   `https://<utilisateur>.github.io/<dépôt>/`.

Pour un nom de domaine personnalisé, le renseigner dans **Settings → Pages → Custom domain**.
