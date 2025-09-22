import re
from typing import Dict

class ChoppySentenceChecker:
    def __init__(self):
        self.issues_found = 0
        self.flagged = []

    def analyze_text(self, text: str, custom_no_sent: int = 10) -> Dict[str, str]:
        """
        Analyze text for choppy sentences (short sentences that may weaken flow).
        Flags sentences shorter than a specified word count.
        """
        self.issues_found = 0
        self.flagged = []
        sentence_markers = 1

        valid_words = [
            "also", "this", "these", "that", "those", "and", "but", "so", "because", 
            "which", "as", "since", "yet", "still", "already", ",", ";", ":", "!", 
            "?", "”", "“", "(", "["
        ]

        # Split text into paragraphs
        all_paragraphs = text.split("\n")

        # Filter valid paragraphs (with at least 2 sentences and not empty)
        all_paragraphs = [
            p for p in all_paragraphs if len(p.split(".")) > 1 and p.strip()
        ]

        for paragraph in all_paragraphs:
            sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())

            # Skip paragraphs with less than 3 sentences
            if len(sentences) > 2:
                # Ignore the first and last sentence of each paragraph
                for sentence in sentences[1:-1]:
                    if len(sentence) > custom_no_sent:
                        words = sentence.split()

                        if len(words) < 10:  # Flag short sentences
                            error_found = True
                            for word in valid_words:
                                if word in sentence:
                                    error_found = False
                                    break

                            if error_found:
                                self.issues_found += 1
                                # Highlight sentence in red
                                red_text = (
                                    f"<span style='color:red'>{sentence.strip()}</span>."
                                )
                                self.flagged.append(
                                    f"{sentence_markers}. {red_text}<br>   → Reason: Sentence is choppy (too short)"
                                )
                                sentence_markers += 1

        if self.flagged and self.issues_found > 2:
            return {
                "issues_found_counter": self.issues_found,
                "issues_para": (
                    "<b>^Auto-Peer: Choppy Sentences^</b><br><br>"
                    + "<br><br>".join(self.flagged)
                    + "<br><br>Click ‘Explanations’ on the Auto-Peer menu if you need further information."
                ),
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
