import re

class DoubledTransitionalsChecker:
    def __init__(self, custom_no_sent=5):
        self.paragraph_counter = 0
        self.sentence_counter = 0
        self.issues_found_counter = 0
        self.custom_no_sent = custom_no_sent
        self.transitionals = [
            "More specifically", "Accordingly", "This is because", "According", "Especially", 
            "Finally", "In the meantime", "So then", "Afterward", "Afterwards", "For example", 
            "In this case", "In that case", "Soon", "Also", "For instance", "Incidentally", 
            "Subsequently", "As a result", "For the most part", "Including", "Such as", "As such", 
            "Furthermore", "Lastly", "As a rule", "Generally", "Later", "Thereby", "As an example", 
            "Hence", "Likewise", "Therefore", "Before", "Here", "Namely", "Thus", "Besides", 
            "However", "Next", "To begin with", "Beyond", "In addition", "Additionally", "Opposite", 
            "To summarize", "By the way", "That is", "In brief", "Ordinarily", "Compared to", 
            "Compared with", "In comparison", "Otherwise", "Together", "Consequently", 
            "In conclusion", "Over there", "Under", "Conversely", "In particular", "Particularly", 
            "Usually", "Coupled with", "In short", "Regularly", "Wherefore", "On the contrary"
        ]
        
    def analyze_text(self, text):
        """Analyze the text to find doubled transitionals starting at the beginning of sentences."""
        
        paragraphs = text.split('\n')
        gather_all = []
        gather_all.append("<b>^Auto-Peer: Double Transitionals Issue^</b><br><br>")

        # Process each paragraph
        for paragraph in paragraphs:
            self.paragraph_counter += 1
            sentences = re.split(r'(?<=\.)\s+', paragraph.strip())
            transitional_count = {}

            # Look for transitionals at the start of sentences
            for i, sentence in enumerate(sentences):
                for transitional in self.transitionals:
                    if re.match(rf'^{re.escape(transitional)},', sentence.strip(), re.IGNORECASE):
                        transitional_lower = transitional.lower()
                        transitional_count[transitional_lower] = transitional_count.get(transitional_lower, 0) + 1

            # If doubled transitionals are found
            doubled_transitional_count = {t: count for t, count in transitional_count.items() if count > 1}
            if doubled_transitional_count:
                if len(sentences) > self.custom_no_sent:  # Check if paragraph has enough sentences
                    self.sentence_counter += len(sentences)
                    self.issues_found_counter += len(doubled_transitional_count)

                    flagged_sentences = []
                    for i, sentence in enumerate(sentences):
                        flagged_sentence = sentence
                        for transitional in doubled_transitional_count:
                            flagged_sentence = re.sub(
                                rf'\b{re.escape(transitional)}\b',
                                f"<span style='color:red'>{transitional}</span>",
                                flagged_sentence,
                                flags=re.IGNORECASE
                            )
                        flagged_sentences.append(f"{i+1}. {flagged_sentence}")

                    transitional_list = ", ".join([f"<span style='color:red'>{t}</span>" for t in doubled_transitional_count])
                    gather_all.append(
                        f"<b>^Auto-Peer: Doubled Transitional^</b> in Paragraph {self.paragraph_counter}<br><br>"
                        f"The repeated transitionals in this paragraph include: {transitional_list}<br><br>"
                        + "<br><br>".join(flagged_sentences)
                    )
        
        gather_all.append("Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>")
        result_text = "<br><br>".join(gather_all)

        if self.issues_found_counter > 0:
            return {
                "issues_found_counter": self.issues_found_counter,
                "issues_para": result_text
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues found."
            }
