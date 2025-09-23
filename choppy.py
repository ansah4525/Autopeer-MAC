import re
from typing import Dict

class ChoppySentenceChecker:
    def __init__(self):
        self.issues_found = 0
        self.flagged = []

    def analyze_text(self, text: str, custom_no_sent: int = 10) -> Dict[str, str]:
        """
        Logic:
        - Uses word count (< custom_no_sent) to flag choppy sentences.
        - Skips first/last sentences of paragraphs with <3 sentences.
        - Uses word-boundary checks for valid_words to avoid false positives.
        - Returns flagged paragraphs when issues_found > 0.
        - Highlights the choppy sentence in red, bolds the full paragraph.
        """
        self.issues_found = 0
        self.flagged = []
        sentence_markers = 1

        valid_words = [
            "also", "this", "these", "that", "those", "and", "but", "so", "because", 
            "which", "as", "since", "yet", "still", "already"
        ]
        punct_tokens = {",", ";", ":", "!", "?", "”", "“", "(", "["}

        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

        for paragraph in paragraphs:
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            if len(sentences) < 3:
                continue

            for sentence in sentences[1:-1]:
                words = [w.strip(".,;:()[]\"'") for w in sentence.split() if w.strip()]
                if len(words) < custom_no_sent:
                    lower_sent = sentence.lower()
                    contains_valid = any(re.search(r'\b' + re.escape(w) + r'\b', lower_sent) for w in valid_words)
                    contains_punct = any(p in sentence for p in punct_tokens)

                    if contains_valid or contains_punct:
                        continue

                    # It's choppy -> record it
                    self.issues_found += 1
                    red_text = f"<span style='color:red'>{sentence.strip()}</span>"
                    highlighted_para = paragraph.replace(sentence, red_text)
                    # Bold the entire paragraph, with only choppy sentence in red
                    self.flagged.append(f"{sentence_markers}. <b>{highlighted_para}</b><br>")
                    sentence_markers += 1

        if self.flagged and self.issues_found > 0:
            return {
                "issues_found_counter": self.issues_found,
                "issues_para": (
                    "<b>Auto-Peer: Choppy Sentences</b><br><br>"
                    + "<br><br>".join(self.flagged)
                    + "<br><br>Click ‘Explanations’ on the Auto-Peer menu if you need further information."
                ),
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
