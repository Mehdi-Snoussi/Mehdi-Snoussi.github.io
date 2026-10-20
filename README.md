# mehdi-snoussi.github.io

Mehdi Snoussi's site, served by GitHub Pages from `master`: the portfolio, the
apps page for social bios, and the privacy policies and terms of Carthage
Studio's eight apps on Google Play. Plain static HTML, no build step: every
page carries its own CSS and script.

| Path | What it is |
|---|---|
| `/` (`index.html`) | Portfolio: services, the shelf of eight apps (each with its screens, version, Play, privacy and terms links), client work, FAQ, about, contact |
| `/apps/` | One column of the eight apps with their Play links, for the TikTok and Instagram bios; `?src=tiktok\|instagram\|youtube` tags the Play links so installs show their source in Play Console |
| `/tt/`, `/ig/` | Short links for bios: redirect to `/apps/` with the platform tag |
| `/legal/` | The legal centre: each app's privacy policy and terms, in that app's own design (see `legal/README.md`) |
| `/app-ads.txt` | AdMob's seller file; it must stay at the domain root |

## The apps

| App | Package | Shelf panel | Legal |
|---|---|---|---|
| Dhikr | `com.carthage.dhikr` | `#panel-dhikr` | `legal/dhikr/` |
| SortFlow | `com.sortflow.sortflow` | `#panel-sortflow` | `legal/sortflow/` |
| AI Mystic | `com.carthage.aimystic` | `#panel-aimystic` | `legal/aimystic/` |
| Cascade | `com.carthage.cascade` | `#panel-cascade` | `legal/cascade/` |
| Zellia | `com.carthage.zellia` | `#panel-zellia` | `legal/zellia/` |
| Relic Revival | `com.carthage.relicrevival` | `#panel-relicrevival` | `legal/relicrevival/` |
| Blue Hour | `com.carthage.bluehour` | `#panel-bluehour` | `legal/bluehour/` |
| Mini Me | `com.carthage.minime` | `#panel-minime` | `legal/minime/` |

## Assets
`assets/apps/<app>.webp` is each app's store icon; `assets/apps/<app>/1-5.webp`
are its five screens (540x1200, 960x540 for Blue Hour's car screen) and
`t1-t5.webp` their thumbnails (132x293, 128x72). They are the apps' own screens,
captured from the app, never mock-ups. Mini Me's come from its store renderer:
`flutter test test/store/store_shots_test.dart --dart-define=SITE=true` in the
`minime` repo writes `build/site/`.

## Adding an app
A shelf button and a panel in `index.html` (version from the app's
`pubspec.yaml`), a row in `apps/index.html`, a card in `legal/index.html`, and
its `legal/<app>/` pages; then update the counts ("eight apps") in all four.
