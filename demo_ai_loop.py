"""
demo_ai_loop.py -- how an AI coding assistant uses a parser as a validator.

The "LLM" below is SIMULATED (a fixed list of candidate outputs), so the demo
runs offline. The point is the control loop used by real tools:

    generate code -> tokenizer (DFA) -> parser (CFG) -> OK?  accept
                                                     -> error? feed message back, regenerate
"""

from checker import check

# Pretend the model returns these drafts in order, improving after each error message.
SIMULATED_DRAFTS = [
    "i = 0\nwhile i < 3\n  i = i + 1\nend",          # forgot 'do'
    "i = 0\nwhile i < 3 do\n  i = i + 1\n",          # forgot 'end'
    "i = 0\nwhile i < 3 do\n  i = i + 1\nend",       # correct
]


def generate(task, feedback, attempt):
    return SIMULATED_DRAFTS[min(attempt, len(SIMULATED_DRAFTS) - 1)]


def main():
    task = "count i from 0 to 3"
    feedback = None
    for attempt in range(5):
        code = generate(task, feedback, attempt)
        ok, report = check(code, name=f"Draft {attempt + 1}")
        print(report, "\n")
        if ok:
            print("Validator accepted the code -> show it to the user.")
            return
        feedback = report  # sent back to the model in the next prompt
    print("Giving up after 5 attempts.")


if __name__ == "__main__":
    main()
