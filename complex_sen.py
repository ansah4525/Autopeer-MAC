import re
from typing import Dict, List

class OverlyComplexSentenceChecker:
    def __init__(self):
        self.bad_words = ["and", "but", "which", "that", "because"]
        self.prep_which = ["in which", "of which", "at which", "to which", "that which"]
        self.num_sentence = 1
        self.issues_found = 0

    def analyze_text(self, text: str, custom_no_sent=3) -> Dict[str, str]:
        text = text.replace(" . ", ". ")
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        flagged_all = []

        for para in paragraphs:
            sentences = [s.strip() for s in para.split(". ")]
            for i, sentence in enumerate(sentences):
                if len(sentence) <= 5:
                    continue

                # Clean trailing period
                if sentence.endswith("."):
                    sentence = sentence[:-1]

                # Skip first sentence if it contains certain punctuation
                if i == 0:
                    if any(sym in sentence for sym in ["“", "”", "(", ")", "[", "]", "?", ";", ":"]):
                        continue

                # Counters
                and_count = len(re.findall(r"\band\b", sentence))
                but_count = len(re.findall(r"\bbut\b", sentence))
                that_count = len(re.findall(r"\bthat\b", sentence))
                because_count = len(re.findall(r"\bbecause\b", sentence))

                # Count "which" excluding preposition+which forms
                which_count = len(re.findall(r"\bwhich\b", sentence))
                for prep in self.prep_which:
                    which_count -= len(re.findall(rf"\b{prep}\b", sentence))

                flagged = False
                flagged_sentence = sentence

                # C1: Flag 2+ "which"
                if which_count > 1:
                    flagged = True
                    flagged_sentence = re.sub(
                        r"\bwhich\b",
                        r"<span style='color:red'>which</span>",
                        flagged_sentence,
                    )
                    flagged_all.append(
                        f"{self.num_sentence}. {flagged_sentence}.<br>   → The word <b>which</b> is repeated in this sentence."
                    )
                    self.num_sentence += 1

                # C2: Flag 3+ "that"
                if that_count > 2:
                    flagged = True
                    flagged_sentence = re.sub(
                        r"\bthat\b",
                        r"<span style='color:red'>that</span>",
                        flagged_sentence,
                    )
                    flagged_all.append(
                        f"{self.num_sentence}. {flagged_sentence}.<br>   → The word <b>that</b> is repeated in this sentence."
                    )
                    self.num_sentence += 1

                # C3: Flag 4+ "and"
                if and_count > 3:
                    flagged = True
                    flagged_sentence = re.sub(
                        r"\band\b",
                        r"<span style='color:red'>and</span>",
                        flagged_sentence,
                    )
                    flagged_all.append(
                        f"{self.num_sentence}. {flagged_sentence}.<br>   → The word <b>and</b> is repeated in this sentence."
                    )
                    self.num_sentence += 1

                # Additional: 2+ "but" or 2+ "because"
                if but_count > 1:
                    flagged = True
                    flagged_sentence = re.sub(
                        r"\bbut\b",
                        r"<span style='color:red'>but</span>",
                        flagged_sentence,
                    )
                    flagged_all.append(
                        f"{self.num_sentence}. {flagged_sentence}.<br>   → The word <b>but</b> is repeated in this sentence."
                    )
                    self.num_sentence += 1

                if because_count > 1:
                    flagged = True
                    flagged_sentence = re.sub(
                        r"\bbecause\b",
                        r"<span style='color:red'>because</span>",
                        flagged_sentence,
                    )
                    flagged_all.append(
                        f"{self.num_sentence}. {flagged_sentence}.<br>   → The word <b>because</b> is repeated in this sentence."
                    )
                    self.num_sentence += 1

                # C4: 4 or more different types among that/which/and/but/because
                types_present = sum([
                    1 if and_count > 0 else 0,
                    1 if but_count > 0 else 0,
                    1 if which_count > 0 else 0,
                    1 if that_count > 0 else 0,
                    1 if because_count > 0 else 0,
                ])
                if types_present > 3:
                    flagged = True
                    flagged_all.append(
                        f"{self.num_sentence}. {sentence}.<br>   → This sentence contains many linking/complex words, which may lead to a wandering structure that is hard to process."
                    )
                    self.num_sentence += 1

                if flagged:
                    self.issues_found += 1

        if flagged_all:
            return {
                "issues_found_counter": self.issues_found,
                "issues_para": (
                    "<b>^Auto-Peer: Overly-Complex Sentences^</b><br><br>"
                    + "<br><br>".join(flagged_all)
                    + "<br><br>Click ‘Explanations’ on the Auto-Peer menu if you need further information."
                ),
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
