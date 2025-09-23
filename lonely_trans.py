import re

class LonelyTransitionalsChecker:
    def __init__(self):
        self.paragraph_counter = 0
        self.lonely_counter = 0

    def analyze_text(self, text):
        """Analyze the text to find lonely transitionals at the start of paragraphs and provide explanations."""

        # Clean the input text by removing extra spaces
        text = re.sub(r'\s+', ' ', text).strip()

        paragraphs = text.split('\n\n')
        gather_all = []
        gather_all.append("<b>Auto-Peer: Lonely Transitionals Issue</b><br><br>")
        gather_all.append("The following paragraphs might be causing a <b>'Lonely Transitionals'</b> issue:<br><br>")

        # List of lonely transitionals to flag
        lonely_transitionals = [
            "Accordingly", "Additionally", "Also", "As a result", "Besides",
            "By contrast", "Consequently", "Conversely", "Especially",
            "For example", "For instance", "Furthermore", "Hence", "However",
            "In addition", "In contrast", "Indeed", "In particular", "Particularly",
            "Likewise", "Namely", "Otherwise", "Similarly", "Thereby", "Therefore", "Thus",
            "Moreover"
        ]

        # Process each paragraph
        for paragraph in paragraphs:
            self.paragraph_counter += 1  # Count each paragraph
            paragraph = paragraph.strip()

            # Check if the paragraph starts with a lonely transitional followed by a comma
            match = re.match(r'^(' + '|'.join(lonely_transitionals) + r'),\s', paragraph)

            if match:
                transitional = match.group(1)
                self.lonely_counter += 1

                # Highlight the transitional
                highlighted = paragraph.replace(
                    transitional, f"<span style='color:red'>{transitional}</span>", 1
                )

                gather_all.append(f"<b>{self.lonely_counter}. {highlighted}</b><br><br>")

        # Reconstruct the output
        gather_all.append("Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>")
        result_text = "".join(gather_all)

        # Format the result
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
