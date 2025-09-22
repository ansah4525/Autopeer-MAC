import re

class TopicSentenceChecker:
    def __init__(self):
        self.issues_found = 0

    def analyze_text(self, text):
        """Analyze the text for shorter-longer violations in topic sentences."""
        paragraphs = text.split('\n')
        flagged_text = []

        for idx, paragraph in enumerate(paragraphs, start=1):
            sentences = re.split(r'\.\s', paragraph.strip())

            # Analyze only if there are more than 3 sentences
            if len(sentences) > 3:
                first_three_sentences = sentences[:3]
                valid_issue = True

                # Exclusion conditions for the first sentence
                first_sentence = first_three_sentences[0]
                if (
                    first_sentence.count('"') >= 2 or
                    ("(" in first_sentence and ")" in first_sentence) or
                    ("[" in first_sentence and "]" in first_sentence) or
                    any(char in first_sentence for char in ['?', ';', ':'])
                ):
                    valid_issue = False

                if valid_issue:
                    word_counts = [len(sentence.split()) for sentence in first_three_sentences]

                    # Rule: first sentence longer than second by 50%
                    if word_counts[0] > word_counts[1] * 1.5:
                        self.issues_found += 1
                        flagged_text.append(
                            f"<b>Auto-Peer: Topic Sentence Issues</b><br><br>"
                            f"<u>Paragraph {idx}</u>:<br>{paragraph.strip()}<br><br>"
                            f"<b>Sentence 1:</b> {first_three_sentences[0]} "
                            f"(Word Count: {word_counts[0]})<br><br>"
                            f"<b>Sentence 2:</b> {first_three_sentences[1]} "
                            f"(Word Count: {word_counts[1]})<br><br>"
                            f"<b>Sentence 3:</b> {first_three_sentences[2]} "
                            f"(Word Count: {word_counts[2]})<br><br>"
                            f"→ <i>Shorter-Longer Violation Found: The topic sentence is disproportionately long compared to the following sentences.</i><br><br>"
                        )

        if self.issues_found > 0:
            explanation = (
                "This check highlights topic sentence issues where the first sentence is disproportionately long.<br>"
                "An overly long topic sentence can weaken clarity and coherence.<br><br>"
                "Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br>"
            )
            return {
                "issues_found_counter": self.issues_found,
                "issues_para": "<br>".join(flagged_text) + "<br>" + explanation
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
