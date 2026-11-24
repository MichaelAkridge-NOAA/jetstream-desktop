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

Changes to app files build Windows, macOS and Linux on GitHub Actions. On an app-changing push to `main`, Actions increments the desktop patch version in `desktop/src-tauri/tauri.conf.json`, synchronizes the other version files and records commit subjects in `desktop/CHANGELOG.md`. After all three builds succeed, it creates a draft release from that exact commit. Review the generated notes and publish the draft for users and update checks. Existing tags and releases are never overwritten; manually pushed tags also trigger draft-release builds. Actions needs write access to the repository and permission to push to `main`; pull the automated version commit before making more changes. The macOS DMG targets the runner's native architecture; it is not a universal build.

The update check uses GitHub's unauthenticated latest-release API. It cannot see a private repository or draft and prerelease builds; the repository and a stable desktop release must be publicly accessible before updates can be discovered. The original repository owns standalone Python package publishing.

Run the UI tests with `npm run test:ui` in `desktop`, Rust tests with `cargo test` in `desktop/transfer`, and Python tests with `pytest` from the repository root. See the [desktop build instructions](https://github.com/MichaelAkridge-NOAA/jetstream-desktop/blob/main/desktop/README.md#run-from-source-development) for prerequisites and sidecar setup.

## This site

The site is in `website/` (MkDocs Material). Once GitHub Pages is configured to use GitHub Actions, changes on the default branch deploy through the Pages workflow:

```bash
pip install mkdocs-material
mkdocs serve -f website/mkdocs.yml
```
