import re

class MissingReferenceChecker:
    def __init__(self, min_paragraph_length=10, min_words=10, min_sentences=2, min_total_words=100):
        self.min_paragraph_length = min_paragraph_length
        self.min_words = min_words
        self.min_sentences = min_sentences
        self.min_total_words = min_total_words

    def is_valid_paragraph(self, paragraph):
        paragraph = paragraph.strip()
        if len(paragraph) < self.min_paragraph_length:
            return False
        if len(paragraph.split()) < self.min_words:
            return False
        if len(re.split(r'\.\s+', paragraph)) < self.min_sentences:
            return False
        if paragraph.strip() in ["", " "]:
            return False
        return True

    def contains_reference(self, paragraph):
        return "(" in paragraph

    def analyze_text(self, text):
        cleaned_text = re.sub(r'\s+', ' ', text.strip())
        word_count = len(cleaned_text.split())

        if word_count < self.min_total_words:
            return {
                "issues_found_counter": 0,
                "issues_para": f"Essay too short for this check (requires {self.min_total_words}+ words)."
            }

        if re.search(r'\[\d+\]', cleaned_text):
            return {
                "issues_found_counter": 0,
                "issues_para": "Detected IEEE-style references — check skipped."
            }

        # Collect valid paragraphs
        raw_paragraphs = re.split(r'(?:\n\s*\n|\n)', text.strip())
        true_paragraphs = [p for p in raw_paragraphs if self.is_valid_paragraph(p)]

        flagged_pairs = []
        count = 0

        for i in range(len(true_paragraphs) - 1):
            p1 = true_paragraphs[i]
            p2 = true_paragraphs[i + 1]
            if not self.contains_reference(p1) and not self.contains_reference(p2):
                count += 1
                flagged_pairs.append(
                    f"{count}. <span style='color:red'>Paragraph 1:</span><br><b>{p1.strip()}</b><br><br>"
                    f"<span style='color:red'>Paragraph 2:</span><br><b>{p2.strip()}</b><br><br>"
                )

        if flagged_pairs:
            explanation = (
                "The following consecutive paragraphs may lack references. "
                "This could indicate weak or missing sourcing.<br><br>"
                "Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>"
            )
            return {
                "issues_found_counter": count,
                "issues_para": "<b>Auto-Peer: Missing References</b><br><br>" + "".join(flagged_pairs) + explanation
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
