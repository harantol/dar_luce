# Dar Luce — site web

Site statique d'une page présentant la maison Dar Luce (location Airbnb au Maroc).
HTML, CSS et JavaScript purs : aucune dépendance, aucune étape de build.

## Structure

```
index.html        Contenu de la page
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

Chercher `TODO` dans `index.html` : chaque élément provisoire est signalé.

- **Lien Airbnb** : remplacer les trois `https://www.airbnb.fr/` par l'adresse de l'annonce.
- **Textes** : remplacer les passages entre crochets `[…]` (ville, présentation, chiffres, équipements, distances).
- **E-mail** : remplacer `contact@example.com`.
- **Photos** : déposer les fichiers dans `images/`, puis remplacer dans chaque bloc
  `<span>…</span>` par `<img src="images/nom.jpg" alt="Description" loading="lazy">`.
- **Photo d'accueil** : dans `css/style.css`, remplacer `--hero-photo: none;` par
  `--hero-photo: url("../images/hero.jpg");`.

Conseil : exporter les photos en JPEG ou WebP, 1600 px de large au maximum, pour garder un site rapide.

## Publication sur GitHub Pages

1. Créer un dépôt sur GitHub et y pousser la branche `main`.
2. Dans le dépôt : **Settings → Pages → Build and deployment**, choisir
   **Deploy from a branch**, branche `main`, dossier `/ (root)`.
3. Le site est en ligne après une à deux minutes à l'adresse
   `https://<utilisateur>.github.io/<dépôt>/`.

Pour un nom de domaine personnalisé, le renseigner dans **Settings → Pages → Custom domain**.
