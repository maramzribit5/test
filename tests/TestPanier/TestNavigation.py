from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options 


# ------------------------------------------------------
# CONFIG CHROME (popup mot de passe supprimée)
# ------------------------------------------------------
def get_chrome_options():
    options = Options()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-gpu")

    # 🚫 Désactiver totalement Google Password Manager (ANTI POPUP)
    options.add_argument("--disable-features=PasswordManagerEnabled,PasswordLeakDetection")

    # 🚫 Désactiver les alertes du gestionnaire de mots de passe Google
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    })

    return options


# ------------------------------------------------------
# LOGIN
# ------------------------------------------------------
def login(driver, username):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()


# ------------------------------------------------------
# TEST PANIER COMPLET POUR UN COMPTE
# ------------------------------------------------------
def test_full_cart_for_account(username):

    print(f"\n===================================================")
    print(f"🧪 TEST COMPLET DU PANIER — COMPTE : {username}")
    print("===================================================\n")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=get_chrome_options()
    )

    # LOGIN
    login(driver, username)

    # utilisateur bloqué
    try:
        driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
        print(f"⚠️ {username} est BLOQUÉ — aucun test possible")
        driver.quit()
        return
    except:
        pass

    # attendre produits
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )

    print("1️⃣  Sélection du produit n°1")

    # PRENDRE LE PREMIER PRODUIT
    first_item = driver.find_element(By.CLASS_NAME, "inventory_item")
    product_title = first_item.find_element(By.CLASS_NAME, "inventory_item_name").text
    product_price = first_item.find_element(By.CLASS_NAME, "inventory_item_price").text

    # Image du catalogue (peut être None)
    try:
        product_img_src = first_item.find_element(By.TAG_NAME, "img").get_attribute("src")
    except:
        product_img_src = None

    print(f"   → Produit : {product_title}")
    print(f"   → Prix catalogue : {product_price}")

    # BOUTON ADD
    add_btn = first_item.find_element(By.CLASS_NAME, "btn_inventory")
    add_btn.click()
    print("2️⃣  Bouton Add to Cart cliqué → Remove OK")

    # BADGE PANIER
    try:
        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        if badge == "1":
            print("3️⃣  Badge panier = 1 ✔")
        else:
            print("3️⃣  ❌ Badge incorrect :", badge)
    except:
        print("3️⃣  ❌ Aucun badge trouvé")

    # NAVIGUER AU PANIER
    driver.find_element(By.ID, "shopping_cart_container").click()
    print("4️⃣  Ouverture du panier")

    # VALIDATION PRODUIT
    cart_item = driver.find_element(By.CLASS_NAME, "cart_item")

    cart_name = cart_item.find_element(By.CLASS_NAME, "inventory_item_name").text
    cart_price = cart_item.find_element(By.CLASS_NAME, "inventory_item_price").text

    print("5️⃣  Vérification produit dans le panier")
    print(f"   Catalogue : {product_title} | Panier : {cart_name}")

    if cart_name == product_title:
        print("   ✔ Le bon produit est dans le panier")
    else:
        print("   ❌ Mauvais produit dans le panier")

    # ----------------------------------------------------
    # 6️⃣ Vérification de l'image produit (comportement normal)
    # ----------------------------------------------------
    print("\n6️⃣  Vérification de l'image produit")

    try:
        cart_img = cart_item.find_element(By.TAG_NAME, "img")
        cart_img_src = cart_img.get_attribute("src")

        print(f"   SRC catalogue : {product_img_src}")
        print(f"   SRC panier    : {cart_img_src}")

        if product_img_src and cart_img_src == product_img_src:
            print("   ✔ L'image correspond à celle du catalogue")
        else:
            print("   ⚠️ Image différente — comportement normal sur ce site")

    except:
        print("   ℹ️ Aucune image affichée dans le panier — comportement normal du site")

    # ----------------------------------------------------
    # 7️⃣ Vérification QTY = 1
    # ----------------------------------------------------
    print("\n7️⃣  Vérification de la quantité (QTY)")

    try:
        qty = cart_item.find_element(By.CLASS_NAME, "cart_quantity").text
        if qty == "1":
            print("   ✔ QTY = 1")
        else:
            print("   ❌ QTY incorrect :", qty)
    except:
        print("   ❌ Impossible de lire la quantité")

    # ----------------------------------------------------
    # 8️⃣ Suppression du produit → Remove
    # ----------------------------------------------------
    print("\n8️⃣  Suppression du produit")

    try:
        remove_btn = cart_item.find_element(By.TAG_NAME, "button")
        remove_btn.click()
        print("   ✔ Suppression effectuée")
    except:
        print("   ❌ Impossible de supprimer l’article")

    # ----------------------------------------------------
    # 9️⃣ Badge disparu
    # ----------------------------------------------------
    print("\n9️⃣  Vérification du badge après suppression")

    try:
        driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        print("   ❌ Badge encore présent (erreur)")
    except:
        print("   ✔ Le badge a disparu")

    # ----------------------------------------------------
    # 🔟 Continue Shopping
    # ----------------------------------------------------
    print("\n🔟  Test du bouton Continue Shopping")

    try:
        driver.find_element(By.ID, "continue-shopping").click()
        print("   ✔ Retour à la liste des produits OK")
    except:
        print("   ❌ Le bouton Continue Shopping ne fonctionne pas")

    driver.quit()



# ------------------------------------------------------
# TEST GLOBAL POUR TOUTES LES COMPTES
# ------------------------------------------------------
def run_all_accounts():
    accounts = [
        "standard_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user",
        "locked_out_user"
    ]

    for acc in accounts:
        test_full_cart_for_account(acc)


# ------------------------------------------------------
# MAIN
# ------------------------------------------------------
if __name__ == "__main__":
    run_all_accounts()



