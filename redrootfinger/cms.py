import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from Wappalyzer import Wappalyzer, WebPage

def detect_cms(url):
    try:
        wappalyzer = Wappalyzer.latest()
        webpage = WebPage.new_from_url(url)

        technologies = wappalyzer.analyze_with_versions(webpage)

        cms_found = {}

        for tech, data in technologies.items():
            categories = data.get("categories", [])
            if any("cms" in c.lower() for c in categories):
                cms_found[tech] = data.get("versions", [])

        return cms_found

    except Exception as e:
        return {"error": str(e)}
