# Run the formal Trika checks

From a fresh checkout, install [elan](https://github.com/leanprover/elan) and
allow it to install the version pinned in `../lean-toolchain` (Lean 4.34.1).
Python 3 and a POSIX shell are required. No `/root/...` checkout layout, source
volume, PDF, database, model credentials or `lake` dependencies are needed for
these tests. If Lean is installed outside PATH, set `LEAN` to its executable.

```sh
lean --version
python3 -m unittest discover -s formal-trika/tests -v
sh formal-trika/control/run.sh
sh formal-trika/recognition/run.sh
python3 formal-trika/tools/emit_keys.py > /tmp/trika-inventory.json
```

The source/evidence reports also require a clean checkout of translation-work
at the revision in `bridge/passages.snapshot.json` (use `TRANSLATION_WORK` or
pass its path explicitly):

```sh
python3 formal-trika/tools/bridge_resolve.py --check --tw ../translation-work
python3 formal-trika/tools/evidence_check.py --root ../translation-work
python3 formal-trika/tools/treeka_formal.py --tw ../translation-work
```

These commands reject missing or changed ledgers rather than reporting empty
coverage. Treeka additionally requires that the source work directories are
clean and at the pinned Git revision. CI checks out that revision and runs
the same reports. Direct references in `EVIDENCE.json` are curated links,
not proof that a Sanskrit passage entails the associated theorem; work-level
references do not count as passage coverage. See [the bridge guide](bridge/README.md)
for regenerating the snapshot and the unresolved witness boundary.

The runners fail if Lean is unavailable or not 4.34.1. They compile positive
files with warnings treated as errors and require each hand-written mutant to
fail specifically because the named, unchanged `by decide` proposition is
false. The control runner produces ignored `.olean` build files locally.

The inventory is **not** a machine-checked key: it is labeled `NOT_RUN`, its
source references are not pinned, and it must not feed publication gates.
Compiler results are restricted to the definitions and statements in these
files. They do not establish source truth, independent review or rights. For
the proposed source-to-essay integration and remaining blockers, see the
[peer review](../PEER-REVIEW-2026-11-06.md).

The 2026-11-06 review used the official Lean 4.34.1 Linux release, Lean commit
`5045d0056413266e57c625dcd7c365b10e377c52`; the downloaded archive had SHA-256
`47bf4bbd78f70c2e9670598ab7124d92b6efb7330ff33e5fbb4030f6fd72e4e4`.
The archive is not vendored here. A `--version` match is not by itself binary
attestation, and the hand-written mutants still require semantic diff review.
