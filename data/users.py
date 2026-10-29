"""Public SauceDemo demo accounts (all share the same published password)."""

DEMO_PASSWORD = "secret_sauce"

# Accounts that can log in. They differ in how the app behaves afterwards.
ACCEPTED_USERS = (
    "standard_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user",
)

LOCKED_OUT_USER = "locked_out_user"
