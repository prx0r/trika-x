# Run the formal Trika checks

Read the [Sanskrit foundation review](SANSKRIT-FOUNDATION-REVIEW-2026-11-06.md)
before using these models in translation, essays or teaching. The 36-total
model previously hid compensating classification errors; its old run records
do not validate the corrected source-to-model mapping.

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
[peer review](../docs/log/PEER-REVIEW-2026-11-06.md).

The 2026-11-06 review used the official Lean 4.34.1 Linux release, Lean commit
`5045d0056413266e57c625dcd7c365b10e377c52`; the downloaded archive had SHA-256
`47bf4bbd78f70c2e9670598ab7124d92b6efb7330ff33e5fbb4030f6fd72e4e4`.
The archive is not vendored here. A `--version` match is not by itself binary
attestation, and the hand-written mutants still require semantic diff review.

The `treeka-research-index/2` graph records direct registry references without
claiming the referenced passages are formalized; `formalized: null` means
unknown. Matched node source/ledger bytes and queue membership are checked;
their interpretation and source authority remain unverified. The practice pathway
assembler currently emits study-only items; no review flag in an input file
can authorize a practice. Cross-repository chain tests are optional and report
skips if `IPVV_CHECKOUT` and `TRANSLATION_WORK` are unavailable.

The committed graph inputs were rebuilt from a complete, clean translation-work
checkout at `e05e640e192a2ea5a317ba76b0f802f4f54e98cc` and pushing pointers
from ipvv `c2cb6b35272bfbd7824063b2fd769f388197495e`. To regenerate, supply
those full checkouts (not the sparse six-work CI checkout):

```sh
python3 formal-trika/tools/build_source_map.py --tw "$TW" --out /tmp/trika-source-map.json
python3 formal-trika/tools/argmap_nodes.py --tw "$TW"
python3 formal-trika/tools/crux_queue.py --pushing "$IPVV/site/data/pushing"
python3 formal-trika/tools/treeka.py --tw "$TW" --sourcemap /tmp/trika-source-map.json
```

Nodes with foreign, conflicting, reversed or ambiguous locators remain
`UNKNOWN`. Byte hashes bind the candidate join to inputs; they do not validate
the Sanskrit or the argmap. The queue's pushing paths are relative to the
supplied pushing directory.

Static axiom hygiene (no Lean needed):
```sh
python3 formal-trika/tools/axiom_audit.py --check
```
rejects `sorry`/`sorryAx`, custom `axiom` declarations, `native_decide`
(`trustCompiler`/`ofReduceBool`). The dynamic half (`#print axioms` =
`[propext, Classical.choice, Quot.sound]` per theorem) still needs a Lean box.

Mechanical mutation sweep (SOTA `jubnzv/Mutate.lean`, Lean box only):
```sh
MUTATE_LEAN=../Mutate.lean/Mutate.lean \
  python3 formal-trika/tools/mutate_sweep.py
```
Hand-written `Broken*.lean` twins stay the preregistered controls; the sweep
is additional — `survived` = coverage gap (add an invariant), `stillborn` =
ill-typed (skip), equivalent mutants recorded explicitly. Fails closed when
Lean or Mutate.lean is absent.
