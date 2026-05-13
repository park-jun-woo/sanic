# ff:func feature=http type=parser control=sequence
# ff:what Resolves client address from proxy headers

from sanic.headers._resolve_proxied_addr import _resolve_proxied_addr


def _resolve_addr(headers, config):
    real_ip_header = config.REAL_IP_HEADER
    proxies_count = config.PROXIES_COUNT
    addr = real_ip_header and headers.getone(real_ip_header, None)
    if not addr and proxies_count:
        addr = _resolve_proxied_addr(headers, config, proxies_count)
    return addr
