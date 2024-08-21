import os
import time
import undetected_chromedriver as uc

class ChromeProxy:

    def __init__(self, host: str, port: int, username: str = "", password: str = ""):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def get_path(self) -> str:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "proxy_extension")

    def create_extension(self, name: str = "Chrome Proxy", version: str = "1.0.0") -> str:
        proxy_folder = self.get_path()
        os.makedirs(proxy_folder, exist_ok=True)

        # Gerar manifesto (estabelecer nome e versão da extensão)
        manifest = ChromeProxy.manifest_json
        manifest = manifest.replace("<ext_name>", name)
        manifest = manifest.replace("<ext_ver>", version)

        # Escrever manifesto no diretório da extensão
        with open(f"{proxy_folder}/manifest.json", "w") as f:
            f.write(manifest)

        # Gerar código JavaScript (substituir alguns marcadores)
        js = ChromeProxy.background_js
        js = js.replace("<proxy_host>", self.host)
        js = js.replace("<proxy_port>", str(self.port))
        js = js.replace("<proxy_username>", self.username)
        js = js.replace("<proxy_password>", self.password)

        # Escrever código JavaScript no diretório da extensão
        with open(f"{proxy_folder}/background.js", "w") as f:
            f.write(js)

        return proxy_folder

    manifest_json = """
    {
        "version": "<ext_ver>",
        "manifest_version": 3,
        "name": "<ext_name>",
        "permissions": [
            "proxy",
            "tabs",
            "storage",
            "webRequest",
            "webRequestAuthProvider"
        ],
        "host_permissions": [
            "<all_urls>"
        ],
        "background": {
            "service_worker": "background.js"
        },
        "minimum_chrome_version": "22.0.0"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: "<proxy_host>",
                port: parseInt("<proxy_port>")
            },
            bypassList: ["localhost"]
        }
    };

    chrome.proxy.settings.set({
        value: config,
        scope: "regular"
    }, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "<proxy_username>",
                password: "<proxy_password>"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
        callbackFn, {
            urls: ["<all_urls>"]
        },
        ['blocking']
    );
    """

proxy = ChromeProxy(
    host="43.159.28.126",
    port=2333,
    username="u66cd4bf7547005a8-zone-custom-region-br-asn-AS52748",
    password="u66cd4bf7547005a8"
)
extension_path = proxy.create_extension()

options = uc.ChromeOptions()
options.add_argument(f"--load-extension={extension_path}")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.binary_location = "/usr/bin/google-chrome"  # Substitua pelo caminho real, se necessário

driver = uc.Chrome(options=options)
driver.get("https://2ip.io/")
time.sleep(5)
# Tirar uma captura de tela da página carregada
screenshot_path0 = '/var/www/html/SistemaWebCaps/CapsExpressWeb/public/scripts/google_screenshot0.png'
driver.save_screenshot(screenshot_path0)
print(f"Captura de tela salva em: {screenshot_path0}")
time.sleep(5)
