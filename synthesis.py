import re

class SynthesisCheckerXojoExact:
    def __init__(self, custom_min_sentences=3):
        self.synthesiscounter = 0
        self.custom_min_sentences = custom_min_sentences
        # Covers 1900–2029 + n.d.
        self.year_pattern = re.compile(r"\b(19[0-9]{2}|20[0-2][0-9]|n\.d\.)\b")

    def analyze_text(self, text):
        self.synthesiscounter = 0  # Reset counter each run
        working_text = text.strip()
        words = working_text.split()
        word_count = len(words)

        # === Step 1: Early exits — essay too short, IEEE style, or no parentheses ===
        if word_count < 1000 or "[1]" in working_text or "(" not in working_text:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }

        # === Step 2: Paragraph and sentence checking ===
        paragraphs = working_text.splitlines()
        result_paragraphs = []

        for idx, para in enumerate(paragraphs, start=1):
            para = para.strip()
            if not para:
                continue

            sentences = para.split(".")
            if len(sentences) < self.custom_min_sentences:
                continue

            years_found = self.year_pattern.findall(para)
            if len(set(years_found)) > 1:  # At least 2 different years
                self.synthesiscounter += 1

                # Highlight the years in red
                marked_para = para
                for year in set(years_found):
                    marked_para = re.sub(
                        re.escape(year),
                        f"<span style='color:red'>{year}</span>",
                        marked_para
                    )

                result_paragraphs.append(
                    f"{self.synthesiscounter}. <u>Paragraph {idx}</u>:<br>{marked_para}<br><br>"
                )

        # === Step 3: Construct result ===
        if self.synthesiscounter > 0 and self.synthesiscounter < 4:
            joined_result = "<br>".join(result_paragraphs)
            explanation = (
                "Synthesis Issue: Most papers above 1000 words include multiple paragraphs demonstrating synthesis.<br><br>"
                "If Auto-Peer detected any synthesis-like paragraphs (multiple distinct years/references), they are provided below.<br><br>"
                "Click ‘Explanations’ on the Auto-Peer menu if you need further information."
            )
            return {
                "issues_found_counter": self.synthesiscounter,
                "issues_para": f"<b>Auto-Peer: Synthesis</b><br><br>{joined_result}{explanation}"
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
