import re

class FakeFriendsChecker:
    def __init__(self):
        # Transitional sentence starters considered problematic
        self.transitional_starters = [
            "and,", "but,", "so,", "yet,", "or,", "for,", "nor,", "also,"
        ]

    def analyze_text(self, text):
        """Analyze the text for transitional sentence starters at the beginning of sentences."""
        paragraphs = text.split('\n')
        flagged_text = []
        issues_found = 0
        paragraph_number = 1

        # Intro line
        flagged_text.append("The following paragraph has a possible <b>'Transitional Sentence Starter'</b> issue:<br><br>")

        for paragraph in paragraphs:
            if not paragraph.strip():
                continue

            sentences = re.split(r'(?<=\.)\s+', paragraph.strip())
            found_any = False

            # Highlight transitionals if found
            for starter in self.transitional_starters:
                for i, sentence in enumerate(sentences):
                    if sentence.lower().startswith(starter):
                        found_any = True
                        issues_found += 1
                        # Highlight the starter in red
                        sentences[i] = (
                            f"<span style='color:red'>{starter.capitalize()}</span>{sentence[len(starter):]}"
                        )

            if found_any:
                # Reconstruct and bold the entire paragraph
                highlighted_para = " ".join(sentences)
                flagged_text.append(f"{paragraph_number}. <b>{highlighted_para}</b><br><br>")
                paragraph_number += 1

        if issues_found > 0:
            return {
                "issues_found_counter": issues_found,
                "flagged_text": (
                    "<b>Auto-Peer: Fake Transitionals Detected</b><br><br>"
                    + "".join(flagged_text)
                    + "Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>"
                )
            }
        else:
            return {
                "issues_found_counter": 0,
                "flagged_text": "No issues identified."
            }
