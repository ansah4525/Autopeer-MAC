import re

class WhichVsThatChecker:
    def __init__(self):
        self.safe_which_phrases = [
            "beyond which", "over which", "under which", "until which", "with whom", "to which", "for which",
            "through which", "of which", "about which", "from which", "by which", "one which", "at which",
            "down which", "in which", "on which", "upon which", "with which", "into which"
        ]

    def analyze_text(self, text):
        """
        Flags overuse of 'which' where 'that' may be preferable.
        - Excludes prepositional uses ('in which', 'by which', etc.)
        - Removes comma+which constructions
        - Skips short paragraphs (< 3 sentences)
        - Ignores 'which' inside quotation marks
        """
        issues_found_counter = 0
        sentence_number = 1
        cleaned_text = text.strip()

        # Remove safe prepositional phrases
        for phrase in self.safe_which_phrases:
            cleaned_text = cleaned_text.replace(f" {phrase} ", " ")

        # Remove comma-which variants
        for pattern in [", which ", ",” which ", '," which ', ",' which "]:
            cleaned_text = cleaned_text.replace(pattern, " ")

        paragraphs = cleaned_text.splitlines()
        gather_all = []

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            sentences = re.split(r'\.\s+', para)
            if len(sentences) < 3:  # skip very short paragraphs
                continue  

            paragraph_flagged = False
            para_sentences = []

            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                if sentence.endswith("."):
                    sentence = sentence[:-1]

                # Look for "which" not excluded
                matches = [m.start() for m in re.finditer(r"\bwhich\b", sentence)]
                for idx in matches:
                    # Skip if inside quotes
                    quote_positions = [m.start() for m in re.finditer(r'"', sentence)]
                    if len(quote_positions) >= 2 and quote_positions[0] < idx < quote_positions[1]:
                        continue

                    # Highlight the 'which'
                    highlighted = re.sub(
                        r"\bwhich\b",
                        "<span style='color:red'>which</span>",
                        sentence,
                        count=1
                    )

                    para_sentences.append(f"{sentence_number}. {highlighted}.<br><br>")
                    issues_found_counter += 1
                    sentence_number += 1
                    paragraph_flagged = True
                    break  # one flag per sentence

            if paragraph_flagged:
                gather_all.append(f"<b>{para}</b><br><br>")  # bold paragraph
                gather_all.extend(para_sentences)

        if issues_found_counter > 0:
            explanation = (
                
                "Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br>"
            )
            return {
                "issues_found_counter": issues_found_counter,
                "issues_para": "<b>Auto-Peer: THAT vs comma-WHICH</b><br><br>" +
                               "".join(gather_all) + explanation
            }
        else:
            return {"issues_found_counter": 0, "issues_para": "No issues identified."}
