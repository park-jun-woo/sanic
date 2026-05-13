# ff:func feature=http type=parser control=sequence
# ff:what Resolves client address from X-Forwarded-For proxy chain


def _resolve_proxied_addr(headers, config, proxies_count):
    assert proxies_count > 0
    try:
        forwarded_for = headers.getall(config.FORWARDED_FOR_HEADER)
        proxies = [
            p
            for p in (p.strip() for h in forwarded_for for p in h.split(","))
            if p
        ]
        return proxies[-proxies_count]
    except (KeyError, IndexError):
        return None
