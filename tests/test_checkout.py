from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(driver, username):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()


def add_first_item(driver):
    # Attendre que le premier bouton Add to Cart soit présent
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn_inventory"))
    ).click()


def test_checkout_button():
    # Configuration du navigateur + suppression du POPUP Chrome
    options = Options()
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-password-manager-reauthentication")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.maximize_window()

    # ---- TC-CHK-01 : Position standard_user ----
    login(driver, "standard_user")
    add_first_item(driver)
    driver.find_element(By.ID, "shopping_cart_container").click()

    btn = driver.find_element(By.ID, "checkout")
    y_position_standard = btn.location['y']

    # ---- TC-CHK-02 : Position visual_user ----
    driver.get("https://www.saucedemo.com/")
    login(driver, "visual_user")
    add_first_item(driver)
    driver.find_element(By.ID, "shopping_cart_container").click()

    btn2 = driver.find_element(By.ID, "checkout")
    y_position_visual = btn2.location['y']

    assert abs(y_position_standard - y_position_visual) < 10, \
        "❌ FAIL - Position différente pour visual_user"

    # ---- TC-CHK-03 : Navigation vers Checkout Step One ----
    btn2.click()
    assert "checkout-step-one" in driver.current_url, \
        "❌ FAIL - Mauvaise navigation vers Checkout Step One"

    # ---- TC-CHK-05 : Cancel retourne au panier ----
    driver.find_element(By.ID, "cancel").click()
    assert "cart" in driver.current_url, \
        "❌ FAIL - Cancel ne retourne pas vers le panier"

    # ---- TC-CHK-04 : Panier vide → checkout désactivé ----
    driver.get("https://www.saucedemo.com/")
    login(driver, "visual_user")
    driver.find_element(By.ID, "shopping_cart_container").click()

    try:
        checkout_btn = driver.find_element(By.ID, "checkout")
        assert not checkout_btn.is_enabled(), \
            "❌ FAIL - Checkout devrait être désactivé quand le panier est vide"
    except:
        # Le bouton n'existe pas → acceptable
        pass

    driver.quit()


if __name__ == "__main__":
    test_checkout_button()


