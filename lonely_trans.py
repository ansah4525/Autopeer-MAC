import re

class LonelyTransitionalsChecker:
    def __init__(self):
        self.paragraph_counter = 0
        self.lonely_counter = 0

    def analyze_text(self, text):
        """Find lonely transitionals at the start of sentences (not whole paragraphs)."""

        # Normalize line breaks and strip spaces
        text = text.strip()
        paragraphs = re.split(r'\n+', text)  # split on one or more newlines

        gather_all = []
        gather_all.append("<b>Auto-Peer: Lonely Transitionals Issue</b><br><br>")
        gather_all.append("The following sentences might be causing a <b>'Lonely Transitionals'</b> issue:<br><br>")

        lonely_transitionals = [
            "Accordingly", "Additionally", "Also", "As a result", "Besides",
            "By contrast", "Consequently", "Conversely", "Especially",
            "For example", "For instance", "Furthermore", "Hence", "However",
            "In addition", "In contrast", "Indeed", "In particular", "Particularly",
            "Likewise", "Namely", "Otherwise", "Similarly", "Thereby", "Therefore", "Thus",
            "Moreover"
        ]

        # Regex pattern: transitional at start of a sentence, followed by comma
        pattern = r'^(' + '|'.join(lonely_transitionals) + r'),\s'

        for paragraph in paragraphs:
            self.paragraph_counter += 1
            paragraph = paragraph.strip()

            # Split paragraph into sentences
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)

            for sent in sentences:
                if re.match(pattern, sent):
                    transitional = re.match(pattern, sent).group(1)
                    self.lonely_counter += 1

                    highlighted = sent.replace(
                        transitional, f"<span style='color:red'>{transitional}</span>", 1
                    )

                    gather_all.append(f"<b>{self.lonely_counter}. {highlighted}</b><br><br>")

        gather_all.append("Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>")
        result_text = "".join(gather_all)

        if self.lonely_counter > 0:
            return {
                "issues_found_counter": self.lonely_counter,
                "issues_para": result_text
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues found."
            }
