import aiohttp
from .headers import detect_server_headers
from .js_frameworks import detect_js_frameworks
from .cms import detect_cms
from .waf import passive_waf, active_waf_probe

async def scan(url):
    results = {}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=15) as response:
            html = await response.text()
            headers = response.headers

        results["server_headers"] = detect_server_headers(response)
        results["js_frameworks"] = detect_js_frameworks(html)
        results["cms"] = detect_cms(url)
        results["waf_passive"] = passive_waf(headers)
        results["waf_active"] = await active_waf_probe(session, url)

    return results
