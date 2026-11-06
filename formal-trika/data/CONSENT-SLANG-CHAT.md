# Slang-into-chat consent gate (E1)

1. Slang files are RENDERINGS, never sources. Answers cite T-tier spans;
   slang supplies the voice.
2. Loading any slang file into chat context requires an explicit
   per-session grant (owner, or scholar for their own sessions),
   recorded as {file, sha256, granted_by, at}. No grant, no load.
3. Revocation = immediate context drop (no stale reads).
4. Slang must never soften gated content: requires-diksha units stay
   STUDY-with-conditions in every register, including slang.
5. Manifest is pointers (path+sha), never copies — one truth, no drift.
