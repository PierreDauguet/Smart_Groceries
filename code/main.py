from carrefour import scrape_carrefour
from superu import scrape_superu
from export_yaml import save_yaml


LATITUDE = 48.8566
LONGITUDE = 2.3522


def main():

    produit = "yaourt fraise"

    print("Recherche du produit :", produit)
    print()

    # Carrefour
    print("Scraping Carrefour...")
    produits_carrefour = scrape_carrefour(
        produit,
        LATITUDE,
        LONGITUDE
    )

    print("Produits Carrefour trouvés :", len(produits_carrefour))

    save_yaml(
        produits_carrefour,
        "../data/resume_carrefour.yaml"
    )

    print()

    # # Super U
    # print("Scraping Super U...")
    # produits_superu = scrape_superu(produit)
    #
    # print("Produits Super U trouvés :", len(produits_superu))
    #
    # save_yaml(
    #     produits_superu,
    #     "../data/resume_superu.yaml"
    # )
    #
    # print()
    # print("Exports YAML terminés")
    #

if __name__ == "__main__":
    main()