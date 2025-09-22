import re
from typing import Dict

class ContractionsCheckerXojoExact:
    def __init__(self, custom_min_sentences: int = 3):
        self.custom_min_sentences = custom_min_sentences
        self.num_sentence = 0
        self.abbrv_list = [
            "’t", "’m", "’ll", "’re", "’ve", "he’s", "she’s", "it’s",
            "couldn’t", "shouldn’t", "could’ve", "would’ve", "that’s", "’d", "doesn’t"
        ]

    def analyze_text(self, text: str) -> Dict[str, str]:
        working_text = text.strip()
        working_text = working_text.replace(" . ", ". ").replace("#", "’")
        paragraphs = working_text.splitlines()
        gather_all = ""
        sentence_counter = 1

        for para in paragraphs:
            sentences = para.split(". ")
            if len(sentences) < self.custom_min_sentences:
                continue

            flagged_sentences = ""
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence or len(sentence) <= 5:
                    continue
                if sentence.endswith("."):
                    sentence = sentence[:-1]

                found = False
                for abbrv in self.abbrv_list:
                    if f"{abbrv} " in sentence or f"{abbrv}," in sentence or sentence.endswith(abbrv):
                        # Replace contraction with red-highlighted version
                        sentence = sentence.replace(abbrv, f"<span style='color:red'>{abbrv}</span>")
                        found = True
                        break

                if found:
                    flagged_sentences += f"{sentence_counter}. {sentence}.<br><br>"
                    self.num_sentence += 1
                    sentence_counter += 1

            if flagged_sentences:
                gather_all += flagged_sentences

        if gather_all:
            explanation = (
                "This check flags informal contractions such as <span style='color:red'>he’s</span> "
                "or <span style='color:red'>shouldn’t</span> in longer paragraphs.<br><br>"
                "Academic style typically avoids contractions; revise to full forms for formal tone.<br><br>"
                "Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>"
            )
            return {
                "issues_found_counter": self.num_sentence,
                "issues_para": (
                    "<b>^Auto-Peer: Contractions^</b><br><br>" +
                    gather_all + explanation
                )
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
