import base64, json, sys, urllib.request
img, out = sys.argv[1], sys.argv[2]
b64 = base64.b64encode(open(img, "rb").read()).decode()
req = urllib.request.Request(
    "http://127.0.0.1:11435/api/generate",
    json.dumps({
        "model": "qwen3.8:27b",
        "prompt": ("Describe this figure for a technical summary: what it shows, axes, "
                   "trends, and the takeaway. Treat exact numbers as approximate."),
        "images": [b64], "stream": False,
    }).encode(),
    {"Content-Type": "application/json"},
)
open(out, "w").write(json.loads(urllib.request.urlopen(req).read())["response"])
