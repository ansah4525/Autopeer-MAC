import re

class ParagraphLengthChecker:
    def __init__(self):
        self.max_sentences_in_paragraph = 15
        self.min_sentences_for_valid_paragraph = 3
        self.max_sentences_for_valid_paragraph = 11
        self.paragraph_counter = 0
        self.long_paragraph_counter = 0

    def analyze_text(self, text):
        """Analyze the text for paragraph length and structure."""
        paragraphs = text.split('\n')
        flagged_text = []
        issues_found = 0

        flagged_text.append("<b>^Auto-Peer: Paragraph Length Issues^</b><br><br>")

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            sentences = re.split(r'\.\s', paragraph)
            sentence_count = len([s for s in sentences if s.strip()])  # count only non-empty sentences

            # Case 1: Paragraph with more than 11 but <= 15 sentences
            if sentence_count > self.max_sentences_for_valid_paragraph and sentence_count <= self.max_sentences_in_paragraph:
                issues_found += 1
                flagged_text.append(
                    f"<b>Paragraph with <span style='color:red'>{sentence_count}</span> sentences flagged:</b><br>"
                    f"{paragraph}<br><br>"
                )

            # Case 2: Very long paragraph (> 15 sentences)
            elif sentence_count > self.max_sentences_in_paragraph:
                issues_found += 1
                self.long_paragraph_counter += 1
                flagged_text.append(
                    f"<b>Long paragraph with <span style='color:red'>{sentence_count}</span> sentences flagged:</b><br>"
                    f"{paragraph}<br><br>"
                )

            # Track valid paragraphs
            if sentence_count >= self.min_sentences_for_valid_paragraph:
                self.paragraph_counter += 1

        flagged_text.append("Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>")

        if issues_found:
            return {
                "issues_found_counter": issues_found,
                "issues_para": "".join(flagged_text)
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }


# Example Usage
# text = """..."""
# checker = ParagraphLengthChecker()
# result = checker.analyze_text(text)
# print(result["issues_para"])
