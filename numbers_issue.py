import re

class NumbersIssueChecker:
    def __init__(self):
        self.issue_counter = 0
        # Units or symbols where digits are OK (don’t flag)
        self.allowed_units = [
            "percent", "%", "dollars?", "euros?", "pounds?", "rupees?", "AED", "USD", "GBP", "EUR", "INR", "SAR"
        ]

    def analyze_text(self, text):
        flagged_sentences = []
        paragraphs = text.split('\n')
        self.issue_counter = 0

        flagged_sentences.append("<b>^Auto-Peer – Numbers/Figures Issue^</b><br><br>")
        flagged_sentences.append("The following sentences may contain a number/figure issue.<br><br>")

        # Regex: match small numbers 1–9 followed by a space and a word (like "3 apples")
        # Excludes decimals, versions, and units.
        pattern = re.compile(
            rf"""
            (?<![\w\.\$€£¥])     # Not part of a word/decimal/currency
            \b([1-9])\s+         # Single digit 1–9 followed by space
            (?!({"|".join(self.allowed_units)}))  # Not followed by allowed units
            ([A-Za-z]+)          # A normal word after the digit
            """,
            re.VERBOSE | re.IGNORECASE
        )

        for paragraph in paragraphs:
            sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
            for sentence in sentences:
                if not sentence:
                    continue

                matches = list(pattern.finditer(sentence))
                if matches:
                    self.issue_counter += 1
                    highlighted = sentence
                    # Highlight only the matched digit + noun
                    for m in reversed(matches):  # reverse so indexes don’t shift
                        span_text = f"{m.group(1)} {m.group(3)}"
                        highlighted = (
                            highlighted[:m.start()] +
                            f"<span style='color:red'>{span_text}</span>" +
                            highlighted[m.end():]
                        )
                    flagged_sentences.append(
                        f"{self.issue_counter}. {highlighted}<br>"
                        f"&nbsp;&nbsp;&nbsp;→ Consider writing out small numbers as words (e.g., 'three apples').<br><br>"
                    )

        if self.issue_counter == 0:
            return {
                "issues_found_counter": 0,
                "issues_para": "No number/figure issues found."
            }

        return {
            "issues_found_counter": self.issue_counter,
            "issues_para": "".join(flagged_sentences) +
                           "Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>"
        }
