"""The bound on how often a durable job re-runs a generation that is cut short every time."""

# Three claims tolerate a transient crash or deployment during work while still
# preventing one generation that always dies from being run again forever.
MAX_TASK_DELIVERIES = 3
