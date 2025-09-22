import re

class SentenceAnalyzer:
    def __init__(self):
        self.bummer_words = ['and', 'but', 'because', 'that', 'which']
        self.max_length = 30
        self.max_bummer_word_count = 3

    def highlight_bummer_words(self, sentence):
        """Highlight bummer words in red in the sentence."""
        for word in self.bummer_words:
            sentence = re.sub(
                rf'\b{word}\b',
                f"<span style='color:red'>{word}</span>",
                sentence,
                flags=re.IGNORECASE
            )
        return sentence

    def clean_text(self, sentence):
        """Remove words inside quotation marks and parentheses."""
        # Remove content inside quotation marks
        sentence = re.sub(r'".*?"', '', sentence)
        # Remove content inside parentheses
        sentence = re.sub(r'\(.*?\)', '', sentence)
        return sentence

    def analyze_text(self, text):
        """Analyze the text for sentence length and conjunction usage."""
        paragraphs = text.split('\n')
        flagged_sentences = []
        sentence_count = 0
        issues_found_counter = 0  # Initialize the issues counter

        flagged_sentences.append("<b>^Auto-Peer: Sentence Length / Conjunction Issues^</b><br><br>")

        for paragraph in paragraphs:
            sentences = re.split(
                r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(?=\s?[A-Z0-9])',
                paragraph
            )  # Better sentence splitting
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue  # Skip empty sentences

                # Clean the sentence by removing content inside quotation marks and parentheses
                cleaned_sentence = self.clean_text(sentence)

                words = cleaned_sentence.split()
                word_count = len(words)
                bummer_word_count = sum(sentence.lower().count(word) for word in self.bummer_words)

                highlighted_sentence = self.highlight_bummer_words(sentence)

                if word_count > self.max_length:
                    issues_found_counter += 1
                    sentence_count += 1
                    flagged_sentences.append(
                        f"{issues_found_counter}. Long sentence "
                        f"({word_count} words):<br>{highlighted_sentence}<br><br>"
                    )

                if bummer_word_count > self.max_bummer_word_count:
                    issues_found_counter += 1
                    sentence_count += 1
                    flagged_sentences.append(
                        f"{issues_found_counter}. Excessive conjunctions detected:<br>{highlighted_sentence}<br><br>"
                    )

        flagged_sentences.append(
            "Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br>"
        )

        results = {
            "flagged_sentence_count": sentence_count,
            "issues_found_counter": issues_found_counter,
            "flagged_sentences": "".join(flagged_sentences)
        }

        return results
