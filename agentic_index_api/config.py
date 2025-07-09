from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration for the API server loaded from environment variables."""

    API_KEY: str
    IP_WHITELIST: str

    @property
    def whitelist(self) -> set[str]:
        """Return ``IP_WHITELIST`` as a normalized set of addresses."""
        return {ip.strip() for ip in self.IP_WHITELIST.split(",") if ip.strip()}

    class Config:
        case_sensitive = True
        env_prefix = ""
