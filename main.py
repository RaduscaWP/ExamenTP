from urllib.parse import urlsplit

from checker import (
    SITES,
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check,
)


if __name__ == "__main__":
    host = urlsplit(SITES[0]).hostname

    print("Partea 1, build_url fara /:", build_url(host, "login"))
    print("Partea 1, build_url cu /:", build_url(host, "/login"))
    print("Partea 1, is_https, HTTPS:", is_https(SITES[0]))
    print("Partea 1, is_https, HTTP:", is_https(SITES[9]))

    for url in [SITES[0], SITES[6], SITES[9]]:
        print("\nPartea 2, show_response:", url)
        show_response(url)

    for url in SITES:
        print("\nPartea 3, check_site:", url, check_site(url))

    print("\nPartea 4, scan_sites:")
    scan_sites()

    print("\nPartea 5 - verificarea anteturilor")
    print("Pagina obisnuita:", check_headers(SITES[0]))
    print("Pagina cu doua anteturi:", check_headers(SITES[10]))
    print("Antet scris cu litere mici:", check_headers(SITES[11]))
    print("Site inexistent:", check_headers(SITES[9]))

    print("\nPartea 6 - incercari repetate")
    print("Status 200:", retry_check(SITES[3]))
    print("Status 404, se opreste dupa prima cerere:", retry_check(SITES[6]))
    print("Status 500, incearca de trei ori:", retry_check(SITES[7]))
    print("Status 500, doar doua incercari:", retry_check(SITES[7], attempts=2))
    print("Site inexistent:", retry_check(SITES[9]))
    print("Status 200 sau 500:", retry_check(SITES[12]))
