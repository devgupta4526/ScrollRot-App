# 21 — Art, animation, sound and font asset checklist

## All assets must be original or legally licensed

| Asset | Destination | Needed by | State |
|---|---|---|---|
| App logo and adaptive icon | `res/mipmap*`, `res/drawable` | M1 | PLANNED / source starter has early vector icon |
| Rotty mascot SVG/vector source | art source folder outside app, vector if appropriate | M1 | PLANNED |
| 5 mascot animation JSONs | `assets/lottie/` | M1/M2 | NOT INCLUDED |
| 3 onboarding illustrations | `res/drawable/` or JSON | M1 | NOT INCLUDED |
| Confetti/streak animations | `assets/lottie/` | M5 | NOT INCLUDED |
| Licensed font and license text | `res/font/` and `licenses/` | M1 | NOT INCLUDED |
| Notification art / optional sounds | `res/drawable` / `res/raw` | M6 | NOT INCLUDED |
| Play listing screenshots/banner | release assets outside APK | M8 | NOT INCLUDED |

## Mascot art direction

An original abstract violet/lime spiral creature with big expressive eyes; avoid close mimicry of competitor's brain mascot. Ensure all moods keep a consistent silhouette and proportions. Produce static fallback vector poses so reduced-motion and disabled-Lottie cases remain complete.

## Required license register entry

For each imported asset record: filename, creator/vendor, source URL, license type, whether redistribution in a paid app is allowed, credit obligations, download date. Do not package fonts/art from search results without appropriate usage rights.

## Asset acceptance

Consistent art style, scalable across densities, enough contrast, no flicker, small size, safe fallback if Lottie JSON invalid; visuals must not contain claims about brain injury or diagnosis.
