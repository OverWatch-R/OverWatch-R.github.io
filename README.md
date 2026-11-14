# overwatch repo

A lightweight Debian/APT repository and package browser for Sileo and Zebra.

Enable GitHub Pages in Settings > Pages using branch `main` and folder `/(root)`. The site URL is `https://overwatch-r.github.io/`.

Allow GitHub Actions to write repository contents in Settings > Actions > General.

Put authorized `.deb` files under `pool/` and push to `main`. The workflow generates APT indexes and `repo/packages.json` automatically. Add `Rootful`, `Rootless`, or `RootHide` to package Description or Tag metadata for the website filters. These labels do not make incompatible packages compatible.

Add this source to Sileo or Zebra: `https://overwatch-r.github.io/`

This starter repository is unsigned. Configure APT signing before treating it as a trusted public distribution. Only distribute packages you own or have permission to redistribute. GitHub Pages is static hosting and has bandwidth and file-size limits.
