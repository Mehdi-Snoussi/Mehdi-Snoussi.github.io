# The legal pages

Privacy policies and terms of service for the eight apps on Google Play, served under `/legal/`
on the `Mehdi-Snoussi.github.io` GitHub Pages site (the portfolio stays at the root).

- The list of all eight: <https://mehdi-snoussi.github.io/legal/>
- `app-ads.txt` lives at the **site root** (`/app-ads.txt`, not under `/legal/`) so AdMob can find it.
- Branch: `master` (this repo's default).

## How the pages are made

The pages in `legal/<app>/` are written by a script. Do not edit them by hand: change the
source in `legal/_src/` and build again.

```bash
py -I legal/_src/build.py            # every page, the list, and the copies kept in the app repos
py -I legal/_src/build.py dhikr      # one app
py -I legal/_src/build.py --fonts    # cut the fonts again (needs fonttools and brotli)
```

| In `legal/_src/` | What it is |
|---|---|
| `build.py` | The builder. `UPDATED` near its top is the "last changed" date on every page: set it on the day the pages go live |
| `base.css` | How every page reads: measure, tables that turn into rows on a phone, print |
| `hub.py` | The list at `/legal/` |
| `<app>/app.json` | Store title, package, date in force, pages, fonts |
| `<app>/privacy.txt`, `terms.txt` | The words, in plain text (the marks are explained at the top of `build.py`) |
| `<app>/theme.css`, `head.html` | That app's look: its own colours, its own fonts, one thing taken from the app |

Rules the pages keep:

- **The words come from the code.** A sentence says what the app does today. When an app
  changes what it does with data, change its `privacy.txt` in the same piece of work.
- **Each app has its own words.** No paragraph is pasted from one app to the next.
- **No request to another site.** Fonts are the apps' own, cut to Latin and served from
  `legal/fonts/` (`OFL.txt` there holds their licences). No analytics, and no script except the
  few lines that light Blue Hour's sky for the reader's clock.
- **The URLs never change.** Play Console and the apps link to them.
- The builder refuses long dashes, middle-dot strings and a short list of stock phrases.

Five app repos keep a copy of their privacy policy at `store/PRIVACY_POLICY.md` (AI Mystic, Blue
Hour, Cascade, Mini Me, Zellia). The builder writes those copies too.

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
| Blue Hour | `com.carthage.bluehour` | `https://mehdi-snoussi.github.io/legal/bluehour/privacy.html` | `https://mehdi-snoussi.github.io/legal/bluehour/terms.html` |
| Mini Me | `com.carthage.minime` | `https://mehdi-snoussi.github.io/legal/minime/privacy.html` | `https://mehdi-snoussi.github.io/legal/minime/terms.html` |

Mini Me also has `https://mehdi-snoussi.github.io/legal/minime/delete-account.html`, the page Play
Console's Data safety form asks for under account deletion.

Thirteen unpublished side apps (breedlens, creepid, cutout, leafsnap, mangaverse, mathcam,
mycar, pawpulse, pixelup, scrollia, snapcal, thock, wallio) had pages here until 18 August 2026.
They were removed because none of them is on Play and nothing linked to them. If any of those
ships later, restore its folder from git history and give it its own source in `_src/`.

Contact for all apps: apps.contact.supports@gmail.com
