def detect_server_headers(response):
    interesting = [
        "Server",
        "X-Powered-By",
        "X-AspNet-Version",
        "X-Generator"
    ]

    found = {}
    for h in interesting:
        if h in response.headers:
            found[h] = response.headers[h]

    return found
