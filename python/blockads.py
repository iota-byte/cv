from mitmproxy import http
from mitmproxy import ctx

# List of blocked domains
BLOCKED_DOMAINS = {"example.com", "anotherdomain.com"}

def request(flow: http.HTTPFlow) -> None:
    if flow.request.host in BLOCKED_DOMAINS:
        ctx.log.info(f"Blocking request to {flow.request.host}")
        # Block the request with a 403 response
        flow.response = http.Response.make(
            403,  # HTTP status code
            b"Blocked by proxy",
            {"Content-Type": "text/plain"}
        )
