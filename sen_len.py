import re

class SentenceAnalyzer:
    def __init__(self):
        self.max_length = 30  # max words per sentence

    def clean_text(self, sentence):
        """Remove words inside quotation marks and parentheses."""
        sentence = re.sub(r'".*?"', '', sentence)  # remove content inside quotes
        sentence = re.sub(r'\(.*?\)', '', sentence)  # remove content inside parentheses
        return sentence

    def analyze_text(self, text):
        """Analyze the text for long sentences."""
        paragraphs = text.split('\n')
        flagged_sentences = []
        issues_found_counter = 0

        flagged_sentences.append("<b>Auto-Peer: Sentence Length Issues</b><br><br>")

        for paragraph in paragraphs:
            sentences = re.split(
                r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(?=\s?[A-Z0-9])',
                paragraph
            )  # better sentence splitting
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue  # skip empty sentences

                cleaned_sentence = self.clean_text(sentence)
                word_count = len(cleaned_sentence.split())

                if word_count > self.max_length:
                    issues_found_counter += 1
                    # highlight the sentence in bold
                    flagged_sentences.append(
                        f"{issues_found_counter}. <b>{sentence}</b> ({word_count} words)<br><br>"
                    )

        flagged_sentences.append(
            "Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>"
        )

        results = {
            "issues_found_counter": issues_found_counter,
            "issues_para": "".join(flagged_sentences)
        }

        return results
