"""One model call, described before it is sent.

A generator picks a contract and builds its inputs, then hands both to DSPy. Splitting
that decision out means the same object can be sent or rendered, so a snapshot of the
prompt cannot describe a call the generator would not make.

What DSPy renders is not the contract the generator names: ``ChainOfThought`` wraps it in
an extended signature carrying a ``reasoning`` output, and that extended signature is what
reaches the model. Reading ``signature`` here rather than the contract class is the
difference between snapshotting the prompt and snapshotting the intent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import dspy


@dataclass(frozen=True)
class PreparedCall:
    """The predictor a generator will invoke, and the inputs it will pass it."""

    contract: type[dspy.Signature]
    predictor: dspy.Module
    inputs: dict[str, object]

    @property
    def signature(self) -> type[dspy.Signature]:
        """The signature DSPy renders, extended fields and all.

        ``ChainOfThought`` builds this one at runtime and it reports itself as
        ``StringSignature``, so ``contract`` is what names the call in a report.
        """
        return cast("type[dspy.Signature]", self.predictor.predict.signature)

    def messages(self) -> list[dict[str, str]]:
        """The exact chat messages this call sends, without sending them.

        ``ChatAdapter`` is what serves these calls: nothing configures an adapter, and
        DSPy's default is ChatAdapter. It falls back to ``JSONAdapter`` only after a parse
        failure, so a rendered prompt describes the first attempt.
        """
        return cast(
            "list[dict[str, str]]",
            dspy.ChatAdapter().format(
                self.signature, demos=self.predictor.predict.demos, inputs=self.inputs
            ),
        )
