"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults"  # (180 tokens)
PART_A_XML_ANSWER      = "The Albanach"          # (251 tokens)
PART_A_SANDWICH_ANSWER = "The Albanach"          # (289 tokens)

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True   # True or False
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
The model correctly answered all three conditions,
with the plain condition being the most efficient in terms of tokens.
The XML and sandwich conditions were slightly less efficient,
but still correct.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Haymarket Vaults" # (213 tokens)
PART_B_XML_ANSWER      = "The Albanach" # (302 tokens)
PART_B_SANDWICH_ANSWER = "The Albanach" # (340 tokens)

PART_B_PLAIN_CORRECT    = True
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
The addition of the distractor did not change the results but it made the model less efficient, causing
it to use more tokens to answer the question.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True   # True or False

PART_C_PLAIN_ANSWER    = "Haymarket Vaults" # (214 tokens)
PART_C_XML_ANSWER      = "The Haymarket Vaults" # (316 tokens)
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults" # (357 tokens)

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
    The small model was able to answer the question correctly, but it was less efficient than the main model, consuming more tokens.
    The plain condition was the most efficient, followed by the XML condition, and the sandwich condition was the least efficient.
    Smaller models are less efficient at answering questions compared to larger models, but they are still able to answer the question correctly.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Distractions can cause model to be less efficient at answering questions and it can cause our costs to increase, better to be plain and simple as
in all scenarios plain is the most efficient, then XML and finally sandwich. Smaller models doen't always mean more efficient, weaker models are more susceptible to distractions.
"""
