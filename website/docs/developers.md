# Developers

JetStream Desktop is open source: [github.com/MichaelAkridge-NOAA/jetstream-desktop](https://github.com/MichaelAkridge-NOAA/jetstream-desktop).

- **The desktop app** (`desktop/`): Tauri 2 shell (`src-tauri/`), Svelte 5 interface (`app/`), and the Rust engine (`transfer/`). [Build instructions](https://github.com/MichaelAkridge-NOAA/jetstream-desktop/blob/main/desktop/README.md#run-from-source-development).
- **The engine's command line** (`jetstream-transfer`): sync, compare, receipts, catalogs, speed check and more. [Engine README](https://github.com/MichaelAkridge-NOAA/jetstream-desktop/blob/main/desktop/transfer/README.md).
- **The Python package** (`jetstream/`): the bundled local server and classic web app. The standalone package is maintained in the [original repository](https://github.com/MichaelAkridge-NOAA/jetstream).

## Building

```bash
python desktop/scripts/build_desktop.py           # installers + portable zip, for this OS
python desktop/scripts/build_desktop.py --portable-only
```

Changes to app files build Windows, macOS and Linux on GitHub Actions; tags like `desktop-v0.2.1` make a draft release with notes from `desktop/CHANGELOG.md`. A maintainer must publish the draft as a stable release for the app's update check to see it. Keep the latest stable release a desktop release tagged `desktop-v*`. The macOS DMG targets the runner's native architecture; it is not a universal build.

The update check uses GitHub's unauthenticated latest-release API. It cannot see a private repository or draft and prerelease builds; the repository and a stable desktop release must be publicly accessible before updates can be discovered. The original repository owns standalone Python package publishing.

Run the UI tests with `npm run test:ui` in `desktop`, Rust tests with `cargo test` in `desktop/transfer`, and Python tests with `pytest` from the repository root. See the [desktop build instructions](https://github.com/MichaelAkridge-NOAA/jetstream-desktop/blob/main/desktop/README.md#run-from-source-development) for prerequisites and sidecar setup.

## This site

The site is in `website/` (MkDocs Material). Once GitHub Pages is configured to use GitHub Actions, changes on the default branch deploy through the Pages workflow:

```bash
pip install mkdocs-material
mkdocs serve -f website/mkdocs.yml
```
