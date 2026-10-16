# The vendored conductor route registry

`v0.2.100/` holds FOUR files of `CampanileSkyForge/aretta-conductor-spec` tag `v0.2.100` (tag object 80054d8f →
commit b5a818ddf568baea79e4488dc81060be3e1efa3b), byte for byte (git blobs 9abf7eb5, f1e8a32d, 72265d0b and
6fc4f8cb checked against the tag's tree): `routes/registry.yaml` (the route registry: one row per conductor route,
with its id, method, path and callers) and the generator that renders it, `scripts/generate-routes.sh`,
`scripts/generate-routes.py` and `scripts/registry_vocab.py`. They are never edited here; a new version is a new
directory.

`crates/aristo-core/src/conductor/paths.rs` is what this generator writes for the CLI (the registry rows with
`callers: cli`). `scripts/check-conductor-paths.sh` regenerates it from this copy with the pinned rustfmt
(Rust 1.96.0's) and fails on any difference; CI runs it.

`v0.2.100.sha256` lists the four files' sha256 (`sha256sum` format, paths relative to `v0.2.100/`). The test
`conductor::tests::the_vendored_spec_matches_its_sha256_list` holds the copy to it, so a local edit is caught.

To move to a newer spec: vendor its four files as a new `v<VERSION>/` with its `.sha256`, point
`scripts/check-conductor-paths.sh` and the lock test at it, regenerate `paths.rs`, and delete the old directory.
