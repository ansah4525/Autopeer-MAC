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
        """Analyze text for doubled transitionals and highlight the paragraph."""
        
        paragraphs = text.split('\n')
        gather_all = []
        gather_all.append("<b>Auto-Peer: Double Transitionals Issue</b><br><br>")

        for paragraph in paragraphs:
            self.paragraph_counter += 1
            sentences = re.split(r'(?<=\.)\s+', paragraph.strip())
            transitional_count = {}

            # Count transitionals at start of sentences
            for sentence in sentences:
                for transitional in self.transitionals:
                    if re.match(rf'^{re.escape(transitional)},', sentence.strip(), re.IGNORECASE):
                        transitional_lower = transitional.lower()
                        transitional_count[transitional_lower] = transitional_count.get(transitional_lower, 0) + 1

            doubled_transitional_count = {t: count for t, count in transitional_count.items() if count > 1}

            if doubled_transitional_count and len(sentences) > self.custom_no_sent:
                self.sentence_counter += len(sentences)
                self.issues_found_counter += len(doubled_transitional_count)

                # Highlight repeated transitionals in red
                highlighted_paragraph = paragraph
                for transitional in doubled_transitional_count:
                    highlighted_paragraph = re.sub(
                        rf'\b{re.escape(transitional)}\b',
                        f"<span style='color:red'>{transitional}</span>",
                        highlighted_paragraph,
                        flags=re.IGNORECASE
                    )

                # Bold the entire paragraph
                highlighted_paragraph = f"<b>{highlighted_paragraph}</b>"

                transitional_list = ", ".join([f"<span style='color:red'>{t}</span>" for t in doubled_transitional_count])
                gather_all.append(
                    f"Paragraph {self.paragraph_counter} flagged for repeated transitionals:<br>"
                    f"The repeated transitionals include: {transitional_list}<br><br>"
                    f"{highlighted_paragraph}<br><br>"
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
