from playwright.sync_api import sync_playwright
import urllib.parse
import re


def extract_infos(text):

    prix = None
    prix_kg = None
    quantite = None

    # prix au kg
    match_kg = re.search(r"(\d+[,.]\d+)\s*€\s*/\s*kg", text.lower())
    if match_kg:
        prix_kg = match_kg.group(1).replace(",", ".") + " € / KG"

    # prix produit
    match_price = re.search(r"(\d+[,.]\d+)\s*€(?!\s*/)", text)
    if match_price:
        prix = match_price.group(1).replace(",", ".") + " €"

    # quantité
    match_qte = re.search(r"\d+\s?[xX]\s?\d+\s?(g|kg|ml|l)|\d+\s?(g|kg|ml|l)", text.lower())
    if match_qte:
        quantite = match_qte.group(0)

    return prix, prix_kg, quantite


def scrape_superu(produit):

    query = urllib.parse.quote(produit)

    # URL de recherche directe
    url = f"https://www.coursesu.com/recherche?text={query}"

    resultats = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            user_agent="Mozilla/5.0",
            locale="fr-FR",
            viewport={"width": 1280, "height": 900}
        )

        page = context.new_page()

        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        # accepter cookies si popup
        try:
            page.click("button:has-text('Accepter')", timeout=3000)
        except:
            pass

        # attendre que les produits chargent
        page.wait_for_timeout(5000)

        # scroll pour lazy loading
        for _ in range(5):
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(1200)

        produits = page.locator("article")

        count = produits.count()

        for i in range(count):

            try:

                bloc = produits.nth(i)

                nom = bloc.locator("h3").inner_text()

                texte = bloc.inner_text()

                prix, prix_kg, quantite = extract_infos(texte)

                # ignorer blocs vides
                if prix is None and prix_kg is None:
                    continue

                resultats.append({
                    "lieu": "Super U",
                    "nom": nom,
                    "quantite": quantite,
                    "prix": prix,
                    "prix_kg": prix_kg,
                    "reduction": None,
                    "note": None,
                    "avis": None
                })

            except:
                pass

        browser.close()

    return resultats