"""Custom exception hierarchy for the Agentic Index scraper."""


class ScraperError(Exception):
    """Base exception for scraper errors."""

class APIError(ScraperError):
    """API request failed."""

class RateLimitError(ScraperError):
    """GitHub API rate limit exceeded."""

class InvalidRepoError(ScraperError):
    """Repository data failed validation."""
