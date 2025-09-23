import re

class MayVsMightChecker:
    def __init__(self):
        self.paragraph_counter = 0
        self.might_counter = 0

    def analyze_text(self, text):
        """Analyze the text to find possible incorrect uses of 'might' (used instead of 'may')."""

        # First tag correct usage of 'might have' (temporarily ignore them)
        text = re.sub(r'\bmight have\b', "~might_have~", text, flags=re.IGNORECASE)

        # Then tag standalone 'might' (not followed by 'have')
        text = re.sub(r'\bmight\b(?!\s+have)', "~might~", text, flags=re.IGNORECASE)

        paragraphs = text.split('\n')
        gather_all = []
        self.might_counter = 0

        # Heading
        gather_all.append("<b>Auto-Peer – May vs Might Issue</b><br><br>")
        gather_all.append("The following paragraphs may have a <b>'May vs Might'</b> issue:<br><br>")

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            if "~might~" in paragraph:
                self.might_counter += 1
                # Highlight "might"
                highlighted = paragraph.replace("~might~", "<span style='color:red'>might</span>").replace("~", "")
                gather_all.append(f"{self.might_counter}. <b>{highlighted}</b><br><br>")

        # Replace placeholders back
        result_text = "".join(gather_all).replace("~might_have~", "might have")

        if self.might_counter:
            return {
                "issues_found_counter": self.might_counter,
                "issues_para": (
                    result_text
                    + "Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>"
                )
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues found."
            }
