[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Illustrative Examples: Recommended Methods That Pass Tests Despite Low CodeBLEU
**In one sentence:** Fig. 4 shows recommended methods (e.g., `removeListener` and `translateAllPositive`) that pass unit tests despite differing textually from the oracle targets, which the authors frame as part of a "quite impressive" result of successfully generating more than 110 such methods, with only ~15% of instances failing via parsing errors (~100 methods) or empty recommendations (~30 methods).
## Key points
- Fig. 4 presents a recommended method that passes the unit tests yet reports a low CodeBLEU score of 0.45 compared to the oracle (target) method.
- The `removeListener(IChemObjectListener col)` oracle null-checks `chemObjectListeners`, fetches `lazyChemObjectListeners()`, and removes `col` only if `listeners.contains(col)`; the passing recommendation keeps the null-check but simplifies the body to `lazyChemObjectListeners().remove(col)`.
- The `translateAllPositive(IAtomContainer atomCon)` oracle initializes `minX`/`minY` with `Double.MAX_VALUE`, iterates 2D atom points with an `Iterator`/`while` loop, logs via `logger.debug`, and delegates to `translate2D(atomCon, minX * -1, minY * -1)`.
- The passing `translateAllPositive` recommendation instead initializes minima with `Double.POSITIVE_INFINITY`, uses `for (IAtom atom : atomCon.atoms())` loops with `Math.min`, handles both 2D (`getPoint2d`) and 3D (`getPoint3d`, including `minZ`) coordinates, and shifts points inline via `atom.setPoint2d(new Point2d(...))`.
- The authors state: "Thus, we consider the successful generation of more than 110 of these methods a quite impressive result for a code recommender."
- The remaining ~15% of instances resulted either in a parsing error (~100 methods) or in an empty recommendation (~30 methods).
- The box plot in the middle part of Fig. 2 depicts the results connected to these generation outcomes.
---
## Fig. 4 examples: target vs. recommended methods
| Method | Oracle (target) mechanism | Recommended (passing) mechanism |
|---|---|---|
| `public void removeListener(IChemObjectListener col)` | `if (chemObjectListeners == null) { return; }`, then `List<IChemObjectListener> listeners = lazyChemObjectListeners(); if (listeners.contains(col)) { listeners.remove(col); }` | `if (chemObjectListeners == null) { return; }`, then `lazyChemObjectListeners().remove(col);` — marked PASS |
| `public static void translateAllPositive(IAtomContainer atomCon)` | `double minX = Double.MAX_VALUE; double minY = Double.MAX_VALUE;` with `Iterator<IAtom> atoms` + `while (atoms.hasNext())` over `getPoint2d()` only, then `logger.debug("Translating: minx=" + minX + ", minY=" + minY); translate2D(atomCon, minX * -1, minY * -1);` | `double minX = Double.POSITIVE_INFINITY; double minY = Double.POSITIVE_INFINITY; double minZ = Double.POSITIVE_INFINITY;` with `for (IAtom atom : atomCon.atoms())`, `Math.min` over `getPoint2d()` and `getPoint3d()`, then inline `atom.setPoint2d(new Point2d(atom.getPoint2d().x - minX, atom.getPoint2d().y - minY))` — marked PASS |

Verbatim caption from the chunk:

> "Fig. 4. Example of recommended method that passes the unit tests but reports a low CodeBLEU score compared to the oracle (i.e., target method)."

Exact reported score in the chunk: **CodeBLEU: 0.45**.

## Generation outcome counts
- Successful generation of more than 110 methods — described verbatim as "a quite impressive result for a code recommender."
- Remaining ~15% of instances: parsing error (~100 methods) or empty recommendation (~30 methods).
- The box plot in the middle part of Fig. 2 depicts these results.

**Covers:** Illustrative target vs recommended method examples (Fig. 4: `removeListener` and `translateAllPositive`; CodeBLEU 0.45 PASS case; >110 successes, ~15% failures as ~100 parsing errors + ~30 empty recommendations; Fig. 2 middle box plot)
