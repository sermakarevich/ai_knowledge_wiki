# 07a: Sample-size (power) table

Two-proportion, unpaired, baseline p0=0.5. n = items per arm.

| delta | alpha 0.05 / power 0.8 | alpha 0.05 / power 0.9 | alpha 0.01 / power 0.8 | alpha 0.01 / power 0.9 |
|---|---|---|---|---|
| 0.05 | 1565 | 2095 | 2329 | 2966 |
| 0.1 | 388 | 519 | 577 | 735 |
| 0.2 | 93 | 124 | 139 | 177 |

Paired (McNemar) size, p_discordant=0.30 (discordant proportion q under the alternative):

| delta | n pairs (alpha .05, power .80) |
|---|---|
| 0.05 | 942 |
| 0.1 | 236 |
| 0.2 | 59 |

_n observed in this tutorial = 60 tickets / 100-150 pairs. Detecting a 10-point pass-rate change needs ~388 items per arm unpaired (alpha .05, power .80) vs ~93 for a 20-point change; pairing the same items cuts the 10-point requirement to ~236 pairs._
