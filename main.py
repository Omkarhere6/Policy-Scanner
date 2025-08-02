from scanner.policy_loader import PolicyLoader
from scanner.scanner_engine import ScannerEngine
import json
import os
from urllib.parse import urlparse

if __name__ == '__main__':
    url = input("Enter URL to scan (e.g. https://example.com): ")
    loader = PolicyLoader('policies/base_policies.yaml')
    policies = loader.load_policies()

    engine = ScannerEngine(url, policies)
    results = engine.run()

    print("\nScan Report:")
    for r in results:
        print(f"{r['policy']}: {r['status']}")

    parsed_url = urlparse(url)
    server_name = parsed_url.hostname.replace('.', '_')
    os.makedirs('reports', exist_ok=True)
    report_path = f'reports/report_{server_name}.json'

    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nReport saved to {report_path}")