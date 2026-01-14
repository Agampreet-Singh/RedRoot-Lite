def detect_js_frameworks(html):
    signatures = {
        "React": ["react", "__REACT_DEVTOOLS_GLOBAL_HOOK__"],
        "Angular": ["angular", "ng-version"],
        "Vue": ["vue", "__vue__"],
        "jQuery": ["jquery"],
        "Next.js": ["__NEXT_DATA__"],
        "Nuxt": ["__NUXT__"],
        "Svelte": ["svelte"]
    }

    detected = []
    lower = html.lower()

    for name, sigs in signatures.items():
        for sig in sigs:
            if sig.lower() in lower:
                detected.append(name)
                break

    return list(set(detected))
