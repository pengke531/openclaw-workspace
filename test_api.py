import urllib.request
import urllib.error
import json

url = "http://www.claudecodeserver.top/api/v1/messages"
key = "sk_4f99b0f81b70afdb62137239037f7e562e77fbda002d4d3ae3881615aef71d25"

data = json.dumps({
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 20,
    "messages": [{"role": "user", "content": "say hi"}]
}).encode()

tests = [
    ("x-api-key (sk_)", {"x-api-key": key}),
    ("Bearer sk_", {"Authorization": f"Bearer {key}"}),
]

for name, extra_headers in tests:
    print(f"=== {name} ===")
    headers = {
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
        "User-Agent": "claude-code/2.1.80",
        "Accept": "application/json"
    }
    headers.update(extra_headers)
    
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"OK: {resp.status}")
            print(resp.read().decode()[:300])
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.reason}")
        body = e.read().decode()[:200]
        print(f"Body: {body}")
    except Exception as ex:
        print(f"ERR: {ex}")
    print()
