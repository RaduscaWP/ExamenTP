import requests


SITES = [
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    return "https://" + host.rstrip("/") + "/" + path.lstrip("/")


def is_https(url):
    return url.startswith("https://")


def show_response(url):
    result = check_site(url)
    print("Status:", result["status"])
    print("Content-Type:", result.get("content_type", "unknown"))
    if "error" in result:
        print("Eroare:", result["error"])


def check_site(url):
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", "unknown"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }
    except requests.exceptions.Timeout:
        return {"status": None, "error": "Timpul de asteptare a expirat."}
    except requests.exceptions.RequestException:
        return {"status": None, "error": "Cererea nu a putut fi efectuata."}


def scan_sites():
    results = []
    for url in SITES:
        result = check_site(url)
        results.append((url, result))

    successful = []
    for url, result in results:
        if result["status"] == 200:
            successful.append((url, result))

    successful.sort(key=lambda site: site[1]["length"], reverse=True)
    for url, result in successful:
        print(url, "-> 200,", result["length"], "octeti")

    failed = len(results) - len(successful)
    print("Reusite:", len(successful), "| Esuate:", failed)


def check_headers(url):
    try:
        response = requests.get(url, timeout=5)

        present = []
        missing = []
        for header in SECURITY_HEADERS:
            if header in response.headers:
                present.append(header)
            else:
                missing.append(header)

        score = len(present) * 100 // len(SECURITY_HEADERS)
        return {
            "present": present,
            "missing": missing,
            "score": score,
        }
    except requests.exceptions.Timeout:
        return {"status": None, "error": "Timpul de asteptare a expirat."}
    except requests.exceptions.RequestException:
        return {"status": None, "error": "Cererea nu a putut fi efectuata."}


def retry_check(url, attempts=3):
    status = None
    count = 0
    error = None

    for _ in range(attempts):
        count += 1
        try:
            response = requests.get(url, timeout=5)
            status = response.status_code
            if status < 500:
                break
        except requests.exceptions.Timeout:
            error = "Timpul de asteptare a expirat."
        except requests.exceptions.RequestException:
            error = "Cererea nu a putut fi efectuata."

    result = {"status": status, "attempts": count}
    if status is None and error is not None:
        result["error"] = error
    return result


if __name__ == "__main__":
    print("Partea 4 - verificarea site-urilor")
    scan_sites()

    print("\nPartea 5 - verificarea anteturilor")
    print("Pagina obisnuita:", check_headers(SITES[0]))
    print("Doua anteturi:", check_headers(SITES[10]))
    print("Antet cu litere mici:", check_headers(SITES[11]))
    print("Site inexistent:", check_headers(SITES[9]))

    print("\nPartea 6 - incercari repetate")
    print("Status 200:", retry_check(SITES[3]))
    print("Status 404:", retry_check(SITES[6]))
    print("Status 500, trei incercari:", retry_check(SITES[7]))
    print("Status 500, doua incercari:", retry_check(SITES[7], attempts=2))
    print("Site inexistent:", retry_check(SITES[9]))
    print("Status aleatoriu:", retry_check(SITES[12]))
