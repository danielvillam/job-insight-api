"""Configuracion compartida de rate limiting."""

from slowapi import Limiter

from app.core.settings import settings


def _client_ip(request) -> str:
	"""Resuelve la IP del cliente para rate limiting."""
	if settings.rate_limit_trust_proxy_headers:
		forwarded = request.headers.get("x-forwarded-for")
		if forwarded:
			first_ip = forwarded.split(",")[0].strip()
			if first_ip:
				return first_ip

	if request.client and request.client.host:
		return request.client.host
	return "unknown"


limiter = Limiter(key_func=_client_ip)
