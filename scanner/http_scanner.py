import requests
from bs4 import BeautifulSoup

class HTTPScanner:
    def __init__(self, url):
        self.url = url
        try:
            self.response = requests.get(url, timeout=10)
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            self.response = None

    def check_header(self, field, required):
        if not self.response:
            return False

        value = self.response.headers.get(field)
        if field.lower() == "content-security-policy" and not value:
            # Try checking HTML meta tag
            return self.check_meta_csp() if required else True
        return bool(value) if required else True

    def check_meta_csp(self):
        """Look for CSP meta tag if header not found."""
        try:
            soup = BeautifulSoup(self.response.text, "html.parser")
            csp_meta = soup.find("meta", attrs={"http-equiv": "Content-Security-Policy"})
            return csp_meta is not None
        except Exception as e:
            print(f"Error parsing HTML for meta CSP: {e}")
            return False

    def check_cookie_secure(self):
        if not self.response:
            return False
        cookies = self.response.cookies
        if not cookies:
            return None  # No cookies to check
        return all(cookie.secure for cookie in cookies)
