 # Audience Sensitivity, Content Compliance & Format Preference Analysis
## France Top 50 Playlist — Atlantic Recording Corporation

**Dataset:** France Top 50 daily playlist snapshots, 18-May-2024 to 27-Nov-2025 (555 days, 27,800 track-days, 325 unique artists).

## 1. Data Validation & Preparation
- Days per snapshot: median = 50 entries/day.
- `duration_ms` converted to minutes (mean 3.09 min, median 3.00 min).
- `album_type` had a rare third label, "compilation" (9 rows), folded into "album."
- `is_explicit` is a clean boolean with no invalid values.

## 2. Explicit Content Sensitivity
- 56.3% of all chart appearances are explicit; 43.7% are clean.
- Explicit share rises to 62.4% in the Top 10, falling to 57.7% in Top 25.
- Clean tracks outperform explicit ones on popularity: mean 80.9 (clean) vs 73.3 (explicit).
- Weighted by rank position, explicit content still leads: 57.4% vs 42.6% of total chart weight.
- Explicit presence is concentrated in a small set of artists (Werenoi, SDM, PLK, Jul, Favé, Tiakola, Ninho).

## 3. Release Format Preference
- Album tracks: 52.9%, Single tracks: 47.1% of chart share.
- Singles outperform album tracks individually: mean popularity 80.7 vs 73.0.
- Format share is stable across rank tiers (~51% single in Top 10/25, 47% in Top 50).

## 4. Album Structure Impact
- Correlation between album size and popularity: -0.34 (moderate dilution).
- EPs (2-5 tracks) score highest (82.6), followed by singles (80.8), small albums (74.5), large albums (70.9), mega-releases (70.7).
- Correlation with rank position is weak (+0.11) — album size affects score more than placement.

## 5. Song Duration Preference
- 63.6% of tracks fall in the 2.5–3.5 minute band; only 1.1% exceed 4.5 minutes.
- Duration correlates weakly with popularity (+0.06) and rank (+0.02).
- The 3.5–4.5 min "long" bucket scores best (79.3); very long tracks (4.5m+) score worst (68.9).

## 6. Content Attribute Concentration
The top of the French Top 50 skews toward explicit, single-format, ~3-minute tracks from a concentrated set of rap/drill artists. The highest-scoring individual tracks skew toward clean, single/EP-format releases from broader pop/international artists.

## 7. KPI Summary

| KPI | Value |
|---|---|
| Explicit Content Share | 56.3% (62.4% in Top 10) |
| Clean Content Dominance Ratio | 0.78 : 1 |
| Single vs Album Track Ratio | 0.89 : 1 |
| Average Song Duration | 3.09 min |
| Album Size Impact Index | -0.34 |
| Content Acceptance Score (clean, rank-weighted) | 42.6% |

## 8. Recommendations
1. **Explicit strategy**: Pair explicit lead singles with clean radio edits to capture both chart presence and individual popularity.
2. **Format strategy**: Favor single/EP-led rollouts over front-loading large albums.
3. **Duration**: Stay near the 3-minute norm; avoid tracks over 4.5 minutes.
4. **Artist concentration risk**: Diversify explicit-genre roster exposure.