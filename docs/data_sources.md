# Data sources

All inputs are public. Earth Engine datasets are read directly in the notebooks; the others are downloaded by the notebooks, except the Relative Wealth Index, which is downloaded by hand.

| Dataset | Used for | Access |
| --- | --- | --- |
| NASA Black Marble VNP46A2 (daily, BRDF- and moonlight-corrected, 500 m) | Outage labels: band `DNB_BRDF_Corrected_NTL`, quality from `Mandatory_Quality_Flag` and `QF_Cloud_Mask` | Earth Engine `NASA/VIIRS/002/VNP46A2` |
| GHSL built-up surface, R2023A, epoch 2020 | Built-up mask for labels; built-up share | Earth Engine `JRC/GHSL/P2023A/GHS_BUILT_S` |
| GHSL population, R2023A, epoch 2020 | Population density | Earth Engine `JRC/GHSL/P2023A/GHS_POP` |
| SRTM 1 arc-second | Elevation | Earth Engine `USGS/SRTMGL1_003` |
| GPM IMERG Final V07 | Rainfall from 1 day before to 2 days after landfall | Earth Engine `NASA/GPM_L3/IMERG_V07` |
| AlphaEarth Foundations annual embeddings (64 dimensions) | Satellite embeddings, year before landfall, built-up pixels only | Earth Engine `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` |
| IBTrACS v04r01, West Pacific basin | Storm tracks, maximum wind, radius of maximum wind | [NOAA NCEI](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/) |
| geoBoundaries gbOpen, Philippines ADM3 and ADM2 | Municipal and provincial boundaries | [geoBoundaries API](https://www.geoboundaries.org/), with a GitHub mirror as fallback |
| Meta Relative Wealth Index, Philippines | Wealth terciles for the equity analysis | [Humanitarian Data Exchange](https://data.humdata.org/dataset/relative-wealth-index) (manual download) |
| List of electric distribution utilities in the Philippines | Utility type, customer count and municipalities served (152 utilities) | [Wikipedia](https://en.wikipedia.org/wiki/List_of_electric_distribution_utilities_in_the_Philippines) |

## Notes

- Black Marble dates are UTC days. The overpass for date D falls at about 01:30 Philippine time on D + 1, so the notebooks shift every image by 25.5 hours before comparing it with landfall.
- Nights with more than 80% lunar illumination are dropped: under a bright moon, the lunar correction can push radiance close to zero and create false outages.
- The utility list is an unofficial compilation. No official GIS layer of distribution-utility service areas was found from the National Electrification Administration or the Energy Regulatory Commission.
