PASSIVE_WAF_SIGNATURES = {
    "Cloudflare": ["cf-ray", "__cf", "cloudflare"],
    "Akamai": ["akamai"],
    "AWS WAF": ["x-amzn", "aws"],
    "Sucuri": ["sucuri"],
    "Imperva": ["incapsula"],
    "Fastly": ["fastly"]
}

def passive_waf(headers):
    detected = []

    for waf, sigs in PASSIVE_WAF_SIGNATURES.items():
        for header in headers:
            for sig in sigs:
                if sig.lower() in header.lower():
                    detected.append(waf)

    return list(set(detected))


async def active_waf_probe(session, url):
    payloads = [
        "' OR 1=1 --",
        "<script>alert(1)</script>",
        "../../../../etc/passwd"
    ]

    for payload in payloads:
        try:
            async with session.get(f"{url}?test={payload}") as r:
                text = await r.text()
                if r.status in [403, 406, 429] or "blocked" in text.lower():
                    return True
        except:
            pass

    return False
