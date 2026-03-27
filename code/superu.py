from playwright.sync_api import sync_playwright
import urllib.parse
import re
import time


def extract_infos(text):

    prix = None
    prix_kg = None
    quantite = None

    text = text.replace("\n", " ").lower()

    match_kg = re.search(r"(\d+[,.]\d+)\s*€\s*/\s*(kg|l)", text)
    if match_kg:
        prix_kg = match_kg.group(1).replace(",", ".") + " € / KG"

    matchs = re.findall(r"(\d+[,.]\d+)\s*€", text)
    if matchs:
        prix = matchs[0].replace(",", ".") + " €"

    match_qte = re.search(
        r"(\d+\s?[xX]\s?\d+\s?(g|kg|ml|l))|(\d+\s?(g|kg|ml|l))",
        text
    )
    if match_qte:
        quantite = match_qte.group(0)

    return prix, prix_kg, quantite


def scrape_superu(produit):

    query = urllib.parse.quote(produit)

    # 🔥 URL CORRIGÉE
    url = f"https://www.coursesu.com/s?q={query}"

    resultats = []

    with sync_playwright() as p:

        context = p.chromium.launch_persistent_context(
            user_data_dir="user_data_superu",
            headless=False,
            locale="fr-FR",
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0"
        )

        context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """)

        page = context.new_page()

        time.sleep(2)
        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        try:
            page.click("button:has-text('Accepter')", timeout=4000)
        except:
            pass

        page.wait_for_timeout(5000)

        for _ in range(6):
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(1.5)

        # 🔥 ATTENTE PRODUITS
        try:
            page.wait_for_selector("article", timeout=10000)
        except:
            print("⚠️ Aucun produit trouvé (mauvaise page)")
            context.close()
            return []

        produits = page.locator("article")
        count = produits.count()

        for i in range(count):

            try:
                bloc = produits.nth(i)

                nom = bloc.locator("h3").inner_text()

                texte = bloc.inner_text()

                prix, prix_kg, quantite = extract_infos(texte)

                if prix is None:
                    try:
                        prix = bloc.locator("[class*=price]").first.inner_text()
                    except:
                        pass

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
                continue

        context.close()

    return resultats


# TEST
if __name__ == "__main__":

    produits = scrape_superu("yaourt fraise")

    for p in produits[:10]:
        print(p)