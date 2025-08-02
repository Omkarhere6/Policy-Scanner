from scanner.http_scanner import HTTPScanner

class ScannerEngine:
    def __init__(self, url, policies):
        self.url = url
        self.policies = policies
        self.http_scanner = HTTPScanner(url)

    def run(self):
        results = []
        for policy in self.policies:
            name = policy['name']
            if policy['type'] == 'header':
                result = self.http_scanner.check_header(policy['field'], policy['required'])
            elif policy['type'] == 'cookie' and policy['field'] == 'Secure':
                result = self.http_scanner.check_cookie_secure()
            else:
                result = False
            results.append({'policy': name, 'status': 'PASS' if result else 'FAIL'})
        return results
