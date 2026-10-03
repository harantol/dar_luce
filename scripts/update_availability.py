"""Télécharge le calendrier iCal de l'annonce Airbnb et n'en publie que les
plages de dates indisponibles, dans data/availability.json.

L'adresse du calendrier est lue dans la variable d'environnement
AIRBNB_ICAL_URL. Ni cette adresse ni le contenu brut du calendrier (qui
contient des détails de réservation) ne sont écrits ou affichés.
"""
import datetime
import json
import os
import re
import sys
import urllib.request

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "data", "availability.json")
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


def main():
    url = os.environ.get("AIRBNB_ICAL_URL", "").strip()
    if not url:
        sys.exit("AIRBNB_ICAL_URL n'est pas défini (secret du dépôt manquant).")

    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (dar-luce-site)"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            ics_text = response.read().decode("utf-8", errors="replace")
    except Exception as error:  # ne pas afficher l'adresse, qui est confidentielle
        sys.exit("Téléchargement du calendrier impossible : %s" % type(error).__name__)

    # En cas de réponse inattendue, on garde le fichier précédent tel quel.
    if "BEGIN:VCALENDAR" not in ics_text:
        sys.exit("La réponse n'est pas un calendrier iCal.")

    today = datetime.date.today()
    booked = [
        [start.isoformat(), end.isoformat()]
        for start, end in merge_ranges(parse_ranges(ics_text))
        if end > today
    ]

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8", newline="\n") as output:
        json.dump({"booked": booked}, output, indent=1)
        output.write("\n")
    print("%d plage(s) indisponible(s) enregistrée(s)." % len(booked))


if __name__ == "__main__":
    main()
