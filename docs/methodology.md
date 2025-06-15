# Methodology

This document outlines how Agentic Index discovers repositories and calculates their scores.

<a id="scoring-formula"></a>
## Scoring Formula

```
Score = 0.30*log2(stars + 1)
      + 0.25*recency_factor
      + 0.20*issue_health
      + 0.15*doc_completeness
      + 0.07*license_freedom
      + 0.03*ecosystem_integration
```

Each component captures a different signal: community adoption, recent activity, maintenance health, documentation quality, licensing freedom, and how well the project fits in the wider ecosystem. Weights are reviewed quarterly and may be adjusted as the landscape evolves.

## Formula History

| Version | Formula | Notes |
|---------|---------|-------|
| v1      | `Score = 0.30*log2(stars+1) + 0.25*recency_factor + 0.20*issue_health + 0.15*doc_completeness + 0.07*license_freedom + 0.03*ecosystem_integration` | Initial release. |

