"""Generation log domain: a DB-persisted log of every LLM generation.

Each LM call made anywhere in the app is recorded (cross-cuttingly, via a DSPy
callback or a harness) to the ``generation_events`` table together with the app
context that was active when it ran. The rows give token usage and the research
record of what each call was sent and answered. Recording is off unless
``CONFIG.log_model_calls`` is true.
"""
