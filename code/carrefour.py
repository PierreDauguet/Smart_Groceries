from playwright.sync_api import sync_playwright
import urllib.parse
import re


def extract_infos(text):

    prix = None
    prix_kg = None
    reduction = None
    quantite = None

    match_kg = re.search(r"(\d+[,.]\d+)\s*€\s*/\s*kg", text.lower())
    if match_kg:
        prix_kg = match_kg.group(1) + " € / KG"

    match_price = re.search(r"(\d+[,.]\d+)\s*€(?!\s*/)", text)
    if match_price:
        prix = match_price.group(1) + " €"

    match_reduc = re.search(r"-\s*\d+\s*%", text)
    if match_reduc:
        reduction = match_reduc.group(0).replace(" ", "")

    match_qte = re.search(r"\d+\s?[xX]\s?\d+\s?(g|kg|ml|l)|\d+\s?(g|kg|ml|l)", text.lower())
    if match_qte:
        quantite = match_qte.group(0)

    return prix, prix_kg, reduction, quantite


def scrape_carrefour(produit, lat, lon):

    query = urllib.parse.quote(produit)
    url = f"https://www.carrefour.fr/s?q={query}"

    resultats = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        context = browser.new_context(

            geolocation={"latitude": lat, "longitude": lon},
            permissions=["geolocation"],

            # simulation vrai navigateur
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",

            viewport={"width": 1280, "height": 900},

            locale="fr-FR"
        )

        page = context.new_page()

        page.goto(url)

        try:
            page.click("button:has-text('Tout accepter')", timeout=4000)
        except:
            pass

        page.wait_for_load_state("domcontentloaded")

        # scroll pour charger produits
        for _ in range(6):

            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1200)

        cartes = page.locator("article").all()

        for c in cartes:

            try:

                nom = c.locator("h3").inner_text()

                texte = c.inner_text()

                prix, prix_kg, reduction, quantite = extract_infos(texte)

                resultats.append({
                    "lieu": "Carrefour le plus proche",
                    "nom": nom,
                    "quantite": quantite,
                    "prix": prix,
                    "prix_kg": prix_kg,
                    "reduction": reduction,
                    "note": None,
                    "avis": None
                })

            except:
                pass

        browser.close()

    return resultats