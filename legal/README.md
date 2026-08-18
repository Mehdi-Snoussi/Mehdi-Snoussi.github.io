# App Legal Center

Privacy policies + terms of service for the six apps published on Google Play, hosted under
`/legal/` on the `Mehdi-Snoussi.github.io` GitHub Pages site (the portfolio stays at the root).
Plain static HTML — no build step.

- Landing page: <https://mehdi-snoussi.github.io/legal/>
- `app-ads.txt` lives at the **site root** (`/app-ads.txt`, not under `/legal/`) so AdMob can find it.
- Branch: `master` (this repo's default).

## Editing
Each page is self-contained: its CSS lives in an inline `<style>` block in the file itself, and
each app's pages are designed in that app's own palette, typography and motifs. There is no
shared stylesheet any more — the old `style.css` was removed on 18 August 2026. Edit a file
directly; the two pages for one app share the same tokens, so change both together.

The legal text is frozen. Redesigns must preserve every sentence, table row, list item, date
and external link verbatim — the URLs below are referenced by live Play Console listings.

## Play Console URLs
Paste each app's privacy URL into **App content → Privacy policy** and reference it in **Data safety**.
Set each app's **developer website** in the store listing to `https://mehdi-snoussi.github.io` so
`app-ads.txt` resolves at the domain root.

| App | Package | Privacy | Terms |
|---|---|---|---|
| Dhikr | `com.carthage.dhikr` | `https://mehdi-snoussi.github.io/legal/dhikr/privacy.html` | `https://mehdi-snoussi.github.io/legal/dhikr/terms.html` |
| SortFlow | `com.sortflow.sortflow` | `https://mehdi-snoussi.github.io/legal/sortflow/privacy.html` | `https://mehdi-snoussi.github.io/legal/sortflow/terms.html` |
| AI Mystic | `com.carthage.aimystic` | `https://mehdi-snoussi.github.io/legal/aimystic/privacy.html` | `https://mehdi-snoussi.github.io/legal/aimystic/terms.html` |
| Cascade | `com.carthage.cascade` | `https://mehdi-snoussi.github.io/legal/cascade/privacy.html` | `https://mehdi-snoussi.github.io/legal/cascade/terms.html` |
| Zellia | `com.carthage.zellia` | `https://mehdi-snoussi.github.io/legal/zellia/privacy.html` | `https://mehdi-snoussi.github.io/legal/zellia/terms.html` |
| Relic Revival | `com.carthage.relicrevival` | `https://mehdi-snoussi.github.io/legal/relicrevival/privacy.html` | `https://mehdi-snoussi.github.io/legal/relicrevival/terms.html` |

Thirteen unpublished side apps (breedlens, creepid, cutout, leafsnap, mangaverse, mathcam,
mycar, pawpulse, pixelup, scrollia, snapcal, thock, wallio) had pages here until 18 August 2026.
They were removed because none of them is on Play and nothing linked to them. If any of those
ships later, restore its folder from git history and give it its own design.

Contact for all apps: apps.contact.supports@gmail.com
