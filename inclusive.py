import re

class inclu_sent:
    def __init__(self):
        self.inclusive_terms_dict = {
            'actress': 'actor', 'addict': 'someone struggling with addiction', 'alcoholic': 'someone with alcoholism',
            'bipolar person': 'someone with bipolar disorder', 'businessman': 'businessperson', 'chairman': 'chairperson',
            'common man': 'average person', 'congressman': 'legislator', 'diabetic': 'person with diabetes',
            'disabled person': 'person with a disability', 'distressed neighborhood': 'neighborhood with fewer opportunities',
            "Down's syndrome person": 'person with Down syndrome', 'drug lord': 'person who sells drugs',
            'the elderly': 'older adults', 'foreigners': 'immigrants', 'freshman': 'first-year student',
            'homeless people': 'people experiencing homelessness', 'inner city': 'urban areas', 'layman': 'layperson',
            'maiden name': 'family name', 'mailman': 'mail carrier', 'mankind': 'humanity', 'man-made': 'synthetic',
            'manpower': 'workforce', 'mentally ill': 'person with DSM diagnosis', 'office girls': 'office staff',
            'policeman': 'police officer', 'recovering drug addict': 'in recovery', 'retarded': 'mentally disabled',
            'salesman': 'salesperson', 'sex-change': 'gender-affirming surgery', 'S/he': 'they', 'spokesman': 'spokesperson',
            'stewardess': 'flight attendant', 'substance abuse': 'substance use disorder', 'transgendered': 'transgender person',
            'weatherman': 'weather reporter', 'wheelchair-bound': 'person who uses a wheelchair'
        }

    def analyze_text(self, text):
        """Analyze the text for inclusive terms."""
        paragraphs = text.split('\n')
        flagged_text = []
        issues_found = 0

        # Add Auto-Peer heading
        flagged_text.append("<b>^Auto-Peer: Inclusive Terms^</b><br><br>")

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue  # Skip empty paragraphs

            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph)
            has_issues = False
            paragraph_issues = []

            for sentence in sentences:
                for term, recommendation in self.inclusive_terms_dict.items():
                    if term in sentence:
                        if not has_issues:
                            has_issues = True
                            flagged_text.append("<b>The Paragraph:</b><br>")
                            flagged_text.append(paragraph + "<br><br>")
                        
                        issues_found += 1
                        highlighted_sentence = sentence.replace(
                            term, f"<span style='color:red'>{term}</span>"
                        )
                        paragraph_issues.append(f"{issues_found}. {highlighted_sentence}<br>")
                        paragraph_issues.append(
                            f"&nbsp;&nbsp;&nbsp;→ The word found: <span style='color:red'>{term}</span><br>"
                            f"&nbsp;&nbsp;&nbsp;→ Suggested replacement: {recommendation}<br><br>"
                        )

            if has_issues:
                flagged_text.extend(paragraph_issues)

        # Add closing line
        flagged_text.append("Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>")

        return {
            "issues_found_counter": issues_found,
            "issues_para": "".join(flagged_text)
        }
