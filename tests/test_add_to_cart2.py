from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter


# -----------------------------------------------
# CONFIG
# -----------------------------------------------
def get_chrome_options():
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    return options


# -----------------------------------------------
# LOGIN
# -----------------------------------------------
def login(driver, username):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()


# -----------------------------------------------
# RÉCUPÉRER X/Y DE 6 BOUTONS ADD TO CART
# -----------------------------------------------
def get_all_buttons_positions(username):

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=get_chrome_options()
    )

    try:
        login(driver, username)

        # utilisateur bloqué
        try:
            driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
            print(f"⚠️ {username} est bloqué — aucune mesure possible.\n")
            driver.quit()
            return None
        except:
            pass

        # attendre les produits
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
        )

        # récupérer 6 boutons
        buttons = driver.find_elements(By.XPATH, "//button[contains(@class,'btn_inventory')]")

        positions = []
        for i, btn in enumerate(buttons[:6], start=1):
            pos = btn.location
            positions.append((pos["x"], pos["y"]))

        print(f"➡️ {username} → {positions}\n")

        driver.quit()
        return positions

    except Exception as e:
        print(f"❌ ERREUR pour {username} : {e}")
        driver.quit()
        return None


# -----------------------------------------------
# TEST GLOBAL
# -----------------------------------------------
def test_buttons_on_all_accounts():

    accounts = [
        "standard_user",
        "locked_out_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user"
    ]

    results = {}

    print("\n🔵 TEST D'ALIGNEMENT DES 6 BOUTONS ADD TO CART POUR LES 6 COMPTES\n")

    # 1. récupérer positions pour chaque compte
    for acc in accounts:
        print("===================================================")
        print(f"TEST DU COMPTE : {acc}")
        print("===================================================")

        positions = get_all_buttons_positions(acc)
        results[acc] = positions

    # 2. déterminer la position normale (majoritaire) bouton par bouton
    print("\n📌 CALCUL DE LA POSITION NORMALE…\n")

    normal_positions = []

    for i in range(6):
        btn_positions = []
        for acc in accounts:
            if results[acc] is not None:
                btn_positions.append(results[acc][i])

        if btn_positions:
            ref_position = Counter(btn_positions).most_common(1)[0][0]
            normal_positions.append(ref_position)
        else:
            normal_positions.append(None)

    print(f"✔ Position normale par bouton : {normal_positions}\n")

    # 3. comparer chaque compte avec la position normale
    print("\n📊 RAPPORT FINAL\n")

    for acc, positions in results.items():
        if positions is None:
            print(f"⚠️ {acc} : COMPTE BLOQUÉ — ignoré.\n")
            continue

        print(f"Compte : {acc}")
        all_ok = True

        for i in range(6):
            if positions[i] != normal_positions[i]:
                print(f"  ❌ Bouton {i+1} incorrect : {positions[i]} ≠ {normal_positions[i]}")
                all_ok = False

        if all_ok:
            print("  ✅ Tous les boutons sont bien alignés pour ce compte.")

        print()

    print("===================================================\n")


# -----------------------------------------------
# MAIN
# -----------------------------------------------
if __name__ == "__main__":
    test_buttons_on_all_accounts()

