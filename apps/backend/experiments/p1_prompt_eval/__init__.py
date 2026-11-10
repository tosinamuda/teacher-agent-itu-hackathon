"""P1 prompt-version evaluation harness: frozen dataset, versioned runs, manual compare.

The scientific loop for ANY change to the personalisation prompt (signature
docstring, field names, mapper rendering):

1. ``dataset.py``   — freeze real focal cases (base sections + enriched learner
                      states) from the dev DB into ``eval_set.json`` ONCE; runs
                      stay comparable even as the DB moves on.
2. ``runner.py``    — run the CURRENT production prompt (or a candidate via
                      ``--variant module:SignatureClass``) over the frozen set;
                      outputs land under ``runs/<label>/`` with the rendered
                      prompts captured. The label is a hash of the signature's
                      instructions — git is the history, the hash is the id.
3. ``compare.py``   — blinded side-by-side markdown per case between two run
                      labels (Candidate A/B order derived per case; key.json
                      holds the de-blinding map). A human reads and judges.

Nothing here touches production behaviour; the runner exercises the REAL
builder + mapper + personaliser + validator path.
"""
