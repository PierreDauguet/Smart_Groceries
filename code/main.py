from playwright.sync_api import sync_playwright
import urllib.parse
import yaml
import os
import re

MAGASIN = "Carrefour Express Brest Victor Eusen"


def scrape_carrefour(produit):

    query = urllib.parse.quote(produit)
    url = f"https://www.carrefour.fr/s?q={query}&sort=price_asc"

    resultats = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(url)

        try:
            page.click("button:has-text('Tout accepter')", timeout=5000)
        except:
            pass

        page.wait_for_load_state("networkidle")

        cartes = page.locator("article").all()

        for c in cartes:

            nom = None
            prix = None
            prix_kg = None
            note = None
            avis = None

            # nom
            if c.locator("h3").count() > 0:
                nom = c.locator("h3").first.inner_text()

            # prix et prix/kg
            spans = c.locator("span").all()

            for s in spans:

                texte = s.inner_text()

                if "€" in texte:

                    if "/KG" in texte or "/kg" in texte:
                        prix_kg = texte
                    else:
                        prix = texte

            # note et avis
            aria = c.locator("[aria-label]").all()

            for a in aria:

                label = a.get_attribute("aria-label")

                if label and "avis" in label:

                    note_match = re.search(r"(\d+\.\d+)", label)
                    avis_match = re.search(r"(\d+)\s*avis", label)

                    if note_match:
                        note = note_match.group(1)

                    if avis_match:
                        avis = avis_match.group(1)

            if nom:

                resultats.append({
                    "lieu": MAGASIN,
                    "nom": nom,
                    "prix": prix,
                    "prix_kg": prix_kg,
                    "note": note,
                    "avis": avis
                })

        browser.close()

    return resultats


def save_yaml(data):

    path = "../data/resume.yaml"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    yaml_data = {"produits": data}

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)

    print("YAML créé :", path)


if __name__ == "__main__":

    produits = scrape_carrefour("yaourt fraise")
    save_yaml(produits)