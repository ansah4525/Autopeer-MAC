import re
from typing import Dict


class TextAnalyzer:
    def __init__(self):
        self.starters = {
            "Also": "Move 'also' from the start of the sentence (e.g., \"Waste management is also a problem in ... \")",
            "And": "'And' joins sentences (e.g., \"Waste management is a problem in many countries, and it is also an opportunity for development specialists.\")",
            "But": "'But' joins sentences (e.g., \"Waste management is a problem in many countries, but it can also be seen as an opportunity for development specialists.\")",
            "Or": "'Or' joins sentences (e.g., \"Waste management can be seen as a problem in many countries, or it can also be seen as an opportunity for development specialists.\")",
            "Nor": "'Nor' joins sentences (e.g., \"Waste management is neither a problem for many countries, nor is it an opportunity for development specialists.\")",
            "So": "'So' joins sentences (e.g., \"Waste management is a problem in many countries, so development specialists need to come up with a solution.\")",
            "Yet": "'Yet' joins sentences (e.g., \"Waste management is a problem in many countries, yet some people see it as an opportunity for development specialists.\")",
            "Well": "This word is often used in speech, but no word is necessary when writing.",
            "Although": "'Although' can be misleading as an opener. Consider revising or restructuring the sentence."
        }

    def analyze_text(self, workingtext: str, explanation_boolean: bool = False) -> Dict[str, str]:
        issuesfoundcounter = 0
        result_text = "<b>^Auto-Peer: Sentence Starter Issues^</b><br><br>"

        allparagraphs = workingtext.split("\n")

        for paragraph in allparagraphs:
            paragraph_flagged = False
            flagged_sentences = []
            allsentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())

            for sentence in allsentences:
                sentence = sentence.strip()
                for starter in self.starters:
                    pattern = rf"^[“\"]?{starter}\b[,]?"
                    if re.match(pattern, sentence, flags=re.IGNORECASE):
                        paragraph_flagged = True
                        issuesfoundcounter += 1
                        explanation = self.starters[starter]
                        # Highlight the starter word in red
                        highlighted_sentence = re.sub(
                            rf"^{starter}",
                            f"<span style='color:red'>{starter}</span>",
                            sentence,
                            flags=re.IGNORECASE
                        )
                        flagged_sentences.append(f"{issuesfoundcounter}. {highlighted_sentence}<br>→ {explanation}<br><br>")
                        break

            if paragraph_flagged:
                result_text += "The following paragraph has a <b>'Sentence Starter'</b> issue:<br><br>"
                result_text += f"{paragraph}<br><br>"
                result_text += "<b>'Sentence Starter'</b> issues from the paragraph above:<br><br>"
                result_text += "".join(flagged_sentences)
                result_text += "<br>"

        if issuesfoundcounter > 0:
            result_text += (
                "Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br>"
            )
        else:
            result_text = "No issues identified."

        return {
            "issues_para": result_text,
            "issues_found_counter": issuesfoundcounter
        }
