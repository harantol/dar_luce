# Dar Luce — site web

Site statique d'une page présentant la maison Dar Luce, location de vacances à
Sidi Kaouki, au Maroc (Airbnb et Booking.com).
HTML, CSS et JavaScript purs : aucune dépendance, aucune étape de build.

## Structure

```
index.html                          Contenu de la page (français)
en/index.html                       Version anglaise, à tenir à jour en parallèle
css/style.css                       Styles (couleurs et polices en haut du fichier)
js/main.js                          Menu mobile, lien e-mail, animations d'apparition
js/calendar.js                      Calendrier des disponibilités
images/                             Photos et favicon
scripts/update_availability.py      Récupération des calendriers iCal
.github/workflows/availability.yml  Mise à jour automatique des disponibilités
data/availability.json              Dates indisponibles (généré, ne pas modifier)
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

## Créer un site pour un autre logement

Ce dépôt sert de modèle : le code (JavaScript, script et workflow des
disponibilités, mise en page) est générique, seul le contenu est propre à Dar Luce.

1. Créer un nouveau dépôt vide sur GitHub et y copier ce dépôt **sans** son
   historique (`.git/`), ni `data/` (il sera régénéré), ni `.idea/`.
2. Adapter tout ce qui est propre à la maison, en français (`index.html`) **et** en
   anglais (`en/index.html`) :
   - **En-tête de page** : `<title>`, `meta description`, `og:title`, `og:description`.
   - **Nom** : logo du menu (`.brand`), titre `<h1>`, pied de page.
   - **Liens de réservation** : adresse de l'annonce Airbnb (`airbnb.fr` en
     français, `airbnb.com` en anglais) et lien Booking.com, dans l'accueil et
     dans la section « Réserver ».
   - **Widget Airbnb** (section « Réserver ») : lien de l'annonce et ligne de
     résumé (type, lieu, chambres, lits, salles de bain).
   - **Sections** : textes et titres de « La maison », « Galerie », « Équipements »,
     « Situation » ; ajouter, retirer ou renommer des sections au besoin (penser
     aussi aux liens du menu).
   - **Vidéo** : identifiant YouTube de l'`<iframe>` de la section « La maison »,
     ou retirer le bloc s'il n'y a pas de vidéo.
   - **Carte** : coordonnées `q=lat,lon` de l'`<iframe>` Google Maps (garder
     `hl=fr` / `hl=en`) et lien « Ouvrir dans Google Maps ».
   - **Calendrier** : dans la section `data-availability`, remplacer
     `harantol/dar_luce` par le nouveau dépôt dans `data-remote`.
   - **Contact** : `data-user` et `data-domain` de l'adresse e-mail, et le texte
     affiché à côté.
3. **Photos** : remplacer le contenu de `images/` et mettre à jour la galerie
   (attributs `src` et `alt`).
4. **Ambiance visuelle**, en haut de `css/style.css` :
   - couleurs du thème clair et du thème sombre (`--bg`, `--accent`…) ;
   - photo d'accueil (`--hero-photo`) ;
   - polices (`--serif`, `--sans`) ;
   - motif décoratif (`--pattern`, l'étoile du zellige) : le remplacer ou le
     mettre à `none`.
   - **Favicon** `images/favicon.svg` : sa couleur reprend `--accent`, son dessin
     l'étoile du motif.
5. **README** : remplacer le nom et la description du logement en tête de fichier.
6. Pousser, puis dans le nouveau dépôt GitHub :
   - ajouter les secrets `AIRBNB_ICAL_URL` et `BOOKING_ICAL_URL` du logement
     (voir « Calendrier des disponibilités ») et lancer une première fois le workflow ;
   - activer GitHub Pages (voir ci-dessous).

Pour vérifier qu'il ne reste rien de l'ancien logement :

```
git grep -n -i -E "dar.?luce|kaouki|essaouira|maroc|morocco|1055538272395774971|Share-Bm2w2zM|bj7D6IWCdGA|pharant69"
```

## Publication sur GitHub Pages

1. Créer un dépôt sur GitHub et y pousser la branche `main`.
2. Dans le dépôt : **Settings → Pages → Build and deployment**, choisir
   **Deploy from a branch**, branche `main`, dossier `/ (root)`.
3. Le site est en ligne après une à deux minutes à l'adresse
   `https://<utilisateur>.github.io/<dépôt>/`.

Pour un nom de domaine personnalisé, le renseigner dans **Settings → Pages → Custom domain**.
