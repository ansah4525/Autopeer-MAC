import re

class ReferencePositioningChecker:
    def __init__(self, min_sentences=2, min_word_count=100):
        self.min_sentences = min_sentences
        self.min_word_count = min_word_count
        self.sent_counter = 0

    def analyze_text(self, text):
        """
        Analyze paragraphs for problematic reference placement.
        Flags paragraphs with only one citation at the end in APA style: (Author, Year).
        """
        self.sent_counter = 0
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        word_count = len(cleaned_text.split())

        # Early exits
        if word_count < self.min_word_count:
            return {
                "issues_found_counter": 0,
                "issues_para": f"Essay too short for this check (requires {self.min_word_count}+ words)."
            }

        if re.search(r"\[\d+\]", cleaned_text):  # IEEE style detection
            return {
                "issues_found_counter": 0,
                "issues_para": "Detected IEEE-style references — check skipped."
            }

        if "(" not in cleaned_text:
            return {
                "issues_found_counter": 0,
                "issues_para": "No parenthetical references found — check skipped."
            }

        paragraphs = re.split(r'\n\s*\n', text.strip())
        flagged_paragraphs = []

        for para in paragraphs:
            para = para.strip()
            sentences = re.split(r'(?<=[.!?])\s+', para)

            if len(sentences) < self.min_sentences:
                continue

            # Count total closing parentheses in paragraph
            if para.count(")") != 1:
                continue  # Skip if there are 0 or more than 1

            # Check if last or second-to-last sentence ends with APA-style reference
            last_sentences = sentences[-2:] if len(sentences) >= 2 else sentences

            for s in last_sentences:
                s = s.strip()
                if re.search(r'\([^)]+\)\.$', s) and "|" not in s:
                    self.sent_counter += 1
                    # Highlight the reference in red inside the whole paragraph (bolded)
                    highlighted_para = re.sub(
                        r'(\([^)]+\))',
                        r"<span style='color:red'>\1</span>",
                        para
                    )
                    flagged_paragraphs.append(
                        f"{self.sent_counter}. <b>{highlighted_para}</b><br><br>"
                    )
                    break

        if self.sent_counter > 0:
            explanation = (
                "If a paragraph has only one reference and that reference occurs at the very end, "
                "it may suggest <b>improper sourcing</b>.<br>"
                "Often, students place a single reference at the end to cover multiple claims, which can weaken credibility.<br>"
                "Sources should ideally be introduced early and used more precisely.<br><br>"
                "Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>"
            )
            issues_text = "".join(flagged_paragraphs)
            return {
                "issues_found_counter": self.sent_counter,
                "issues_para": (
                    "<b>Auto-Peer: Problematic Reference Positioning</b><br><br>"
                    + issues_text
                    + explanation
                )
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
