import re

class MayVsMightChecker:
    def __init__(self):
        self.paragraph_counter = 0
        self.sentence_counter = 0
        self.might_counter = 0

    def analyze_text(self, text):
        """Analyze the text to find incorrect uses of 'might' (used instead of 'may')."""

        # First tag correct usage of 'might have' (temporarily ignore them)
        text = re.sub(r'\bmight have\b', "~might_have~", text, flags=re.IGNORECASE)

        # Then tag standalone 'might' (not followed by 'have')
        text = re.sub(r'\bmight\b(?!\s+have)', "~might~", text, flags=re.IGNORECASE)

        paragraphs = text.split('\n')
        gather_all = []
        self.might_counter = 0
        gather_all.append("<b>^Auto-Peer – May vs Might Issue^</b><br><br>")

        for paragraph in paragraphs:
            sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
            flagged_sentences = []
            self.paragraph_counter += 1

            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue

                self.sentence_counter += 1

                if "~might~" in sentence:
                    self.might_counter += 1
                    highlighted = sentence.replace(
                        "~might~",
                        "<span style='color:red'>might</span>"
                    ).replace("~", "")
                    flagged_sentences.append(
                        f"{self.might_counter}. {highlighted}<br>"
                        f"&nbsp;&nbsp;&nbsp;→ Suggestion: Use <b>'may'</b> for present or future context.<br><br>"
                    )

            if flagged_sentences:
                gather_all.extend(flagged_sentences)

        # Replace placeholders back
        result_text = "".join(gather_all).replace("~might_have~", "might have")

        if self.might_counter:
            return {
                "issues_found_counter": self.might_counter,
                "issues_para": (
                    result_text
                    + "<br><br>Click ‘Explanations’ on the Auto-Peer menu if you need further information."
                )
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues found."
            }
