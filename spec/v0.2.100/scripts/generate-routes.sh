#!/usr/bin/env sh
# Generate every consumer's route file from routes/registry.yaml (T0 "names once"; the pattern of
# scripts/generate-types.sh). The Rust goes through the PINNED rustfmt (the conductor's toolchain,
# rust-toolchain.toml 1.96.0), so the conductor's `cargo fmt --check` passes with no skip.
#
#   scripts/generate-routes.sh                      every output: generated/ + routes/RETIRE-LIST.md
#   scripts/generate-routes.sh --conductor <dir> [--registry <file>]
#                                                   the conductor's two Rust files only, in <dir>
#
# The conductor's CI runs the second form from its vendored copy (spec/v<VERSION>/) and fails on
# any difference to the committed files.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
RUSTFMT=${RUSTFMT:-rustfmt}
PIN='(ac68faa20c 2026-05-25)'   # rustfmt of Rust 1.96.0
v=$("$RUSTFMT" --version)
case "$v" in *"$PIN"*) ;; *) echo "generate-routes: rustfmt is '$v', the pin is 1.96.0's $PIN (set RUSTFMT)" >&2; exit 1;; esac

if [ "${1:-}" = "--conductor" ]; then
  dir=$2; registry=${4:-$here/../routes/registry.yaml}
  [ "${3:-}" = "" ] || [ "$3" = "--registry" ] || { echo "usage: $0 --conductor <dir> [--registry <file>]" >&2; exit 2; }
  python3 -B "$here/generate-routes.py" --registry "$registry" --conductor "$dir"
  "$RUSTFMT" --edition 2021 "$dir/crates/access/src/generated/doors.rs" "$dir/crates/routes/src/generated/routes.rs"
  exit 0
fi

cd "$here/.."
python3 -B scripts/generate-routes.py --registry routes/registry.yaml --out generated --retire-list routes/RETIRE-LIST.md
"$RUSTFMT" --edition 2021 generated/conductor/crates/access/src/generated/doors.rs \
  generated/conductor/crates/routes/src/generated/routes.rs \
  generated/cli/crates/aristo-core/src/conductor/paths.rs
echo "generated generated/{conductor,dashboard,cli,plugin} and routes/RETIRE-LIST.md from routes/registry.yaml"
