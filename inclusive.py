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
        """Analyze the text for inclusive terms and highlight paragraphs with issues."""
        paragraphs = text.split('\n')
        flagged_text = []
        issues_found = 0
        paragraph_number = 1

        # Add Auto-Peer heading
        flagged_text.append("<b>Auto-Peer: Inclusive Terms Detected</b><br><br>")
        flagged_text.append("The following paragraphs have inclusive term issues:<br><br>")

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue  # Skip empty paragraphs

            has_issue = False
            highlighted_para = paragraph

            for term in self.inclusive_terms_dict.keys():
                if term in paragraph:
                    # Highlight the term in red
                    highlighted_para = highlighted_para.replace(term, f"<span style='color:red'>{term}</span>")
                    has_issue = True

            if has_issue:
                # Bold the entire paragraph and add it to the flagged list
                flagged_text.append(f"{paragraph_number}. <b>{highlighted_para}</b><br><br>")
                paragraph_number += 1
                issues_found += 1

        # Add closing line
        flagged_text.append("Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>")

        return {
            "issues_found_counter": issues_found,
            "issues_para": "".join(flagged_text)
        }
