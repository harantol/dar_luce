"""Télécharge les calendriers iCal des annonces (Airbnb, Booking.com) et n'en
publie que les plages de dates indisponibles, dans data/availability.json.

Les adresses sont lues dans les variables d'environnement AIRBNB_ICAL_URL
(obligatoire) et BOOKING_ICAL_URL (facultative). Ni ces adresses ni le contenu
brut des calendriers (qui contient des détails de réservation) ne sont écrits
ou affichés.
"""
import datetime
import json
import os
import re
import sys
import urllib.request

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "data", "availability.json")
# (variable d'environnement, nom affiché, obligatoire)
SOURCES = [
    ("AIRBNB_ICAL_URL", "Airbnb", True),
    ("BOOKING_ICAL_URL", "Booking.com", False),
]
DATE_LINE = re.compile(r"^(DTSTART|DTEND)[^:]*:(\d{8})")


def parse_ranges(ics_text):
    """Retourne les plages [arrivée, départ) de chaque événement du calendrier."""
    # Une ligne iCal repliée continue sur la suivante, qui commence par un blanc.
    lines = re.sub(r"\r?\n[ \t]", "", ics_text).splitlines()
    ranges, current = [], None
    for line in lines:
        if line.startswith("BEGIN:VEVENT"):
            current = {}
        elif line.startswith("END:VEVENT"):
            if current and "DTSTART" in current:
                start = current["DTSTART"]
                end = current.get("DTEND", start + datetime.timedelta(days=1))
                if end > start:
                    ranges.append((start, end))
            current = None
        elif current is not None:
            match = DATE_LINE.match(line)
            if match:
                current[match.group(1)] = datetime.datetime.strptime(match.group(2), "%Y%m%d").date()
    return ranges


def merge_ranges(ranges):
    """Fusionne les plages qui se chevauchent ou se suivent."""
    merged = []
    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


def download(url, name):
    """Retourne le texte du calendrier, ou arrête tout sans toucher au fichier publié."""
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (dar-luce-site)"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            ics_text = response.read().decode("utf-8", errors="replace")
    except Exception as error:  # ne pas afficher l'adresse, qui est confidentielle
        sys.exit("%s : téléchargement du calendrier impossible (%s)." % (name, type(error).__name__))
    if "BEGIN:VCALENDAR" not in ics_text:
        sys.exit("%s : la réponse n'est pas un calendrier iCal." % name)
    return ics_text


def main():
    # Si une source configurée échoue, on garde le fichier précédent tel quel :
    # mieux vaut un calendrier en retard qu'un calendrier qui oublie des réservations.
    ranges = []
    for variable, name, required in SOURCES:
        url = os.environ.get(variable, "").strip()
        if not url:
            if required:
                sys.exit("%s n'est pas défini (secret du dépôt manquant)." % variable)
            print("%s : non configuré, ignoré." % name)
            continue
        found = parse_ranges(download(url, name))
        print("%s : %d événement(s)." % (name, len(found)))
        ranges.extend(found)

    today = datetime.date.today()
    booked = [
        [start.isoformat(), end.isoformat()]
        for start, end in merge_ranges(ranges)
        if end > today
    ]

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8", newline="\n") as output:
        json.dump({"booked": booked}, output, indent=1)
        output.write("\n")
    print("%d plage(s) indisponible(s) enregistrée(s)." % len(booked))


if __name__ == "__main__":
    main()
