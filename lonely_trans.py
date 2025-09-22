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
        gather_all.append("<b>^Auto-Peer: Lonely Transitionals Issue^</b><br><br>")

        # List of lonely transitionals to flag
        lonely_transitionals = [
            "Accordingly", "Additionally", "Also", "As a result", "Besides",
            "By contrast", "Consequently", "Conversely", "Especially",
            "For example", "For instance", "Furthermore", "Hence", "However",
            "In addition", "In contrast", "Indeed", "In particular", "Particularly",
            "Likewise", "Namely", "Otherwise", "Similarly", "Thereby", "Therefore", "Thus",
            "Moreover"
        ]

        # Explanations for the transitionals
        explanations = {
            "Accordingly": "Following the procedure described above ...",
            "Additionally": "In addition to the problem of waste management ...",
            "Also": "Deforestation is also a problem in Africa ...",
            "As a result": "As a result of deforestation ...",
            "Besides": "In addition to the problem of waste management ...",
            "By contrast": "In contrast to the problem of waste management ...",
            "Consequently": "As a consequence of the problem of deforestation ...",
            "Conversely": "In contrast to the problem of waste management ...",
            "Especially": "A good example of effective solar energy production can be found in ...",
            "For example": "An example of effective solar energy production can be found in ...",
            "For instance": "An example of effective solar energy production can be found in ...",
            "Furthermore": "In addition to the problem of waste management ...",
            "Hence": "As a result of this deforestation, ...",
            "However": "In contrast to the problem of waste management ...",
            "In addition": "In addition to the problem of waste management ...",
            "In contrast": "In contrast to the problem of waste management ...",
            "Indeed": "To be added...",
            "In particular": "A good example of effective solar energy production can be found in ...",
            "Particularly": "A good example of effective solar energy production can be found in ...",
            "Likewise": "Similar to the problem of deforestation, ...",
            "Namely": "A specific example of the issue of deforestation is ...",
            "Otherwise": "If this problem with deforestation is not resolved, ...",
            "Similarly": "Similar to the problem of deforestation, ...",
            "Thereby": "Through this use of genetic engineering ...",
            "Therefore": "As a result of this deforestation, ...",
            "Thus": "As a result of this deforestation, ..."
        }

        # Process each paragraph
        for paragraph in paragraphs:
            self.paragraph_counter += 1  # Count each paragraph
            paragraph = paragraph.strip()

            # Check if the paragraph starts with a lonely transitional followed by a comma
            match = re.match(r'^(' + '|'.join(lonely_transitionals) + r'),\s', paragraph)

            if match:
                transitional = match.group(1)
                self.lonely_counter += 1
                explanation = explanations.get(transitional, "No specific explanation provided.")

                # Highlight the transitional
                highlighted = paragraph.replace(
                    transitional, f"<span style='color:red'>{transitional}</span>", 1
                )

                gather_all.append(
                    f"{self.lonely_counter}. {highlighted}<br>"
                    f"&nbsp;&nbsp;&nbsp;→ <b>Explanation:</b> {explanation}<br><br>"
                )

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
