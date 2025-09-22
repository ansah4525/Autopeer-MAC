import re

class FakeFriendsChecker:
    def __init__(self):
        # Define a dictionary for fake friends and their explanations
        self.fake_friends_dict = {
            'a lot': 'many',
            'believe': "Use alternatives such as 'argue,' 'suggest,' 'highlight,' 'find,' 'discuss,' 'point out,' 'show,' or 'posit,' instead of 'believe.'",
            'I believe': "Use alternatives such as 'argue,' 'suggest,' 'highlight,' 'find,' 'discuss,' 'point out,' 'show,' or 'posit,' instead of 'I believe.'",
            'done': "Use 'conducted' instead of 'done' for more precise language.",
            'due to': "Replace 'due to' with 'because of' or 'caused by.'",
            'huge': "Avoid using 'huge' and use a more specific word.",
            'prove': "Use 'suggest' instead of 'prove' when discussing research findings.",
            'says': "Avoid 'says' in formal writing; use 'writes,' 'argues,' 'suggests,' or similar words.",
            'talks about': "Replace 'talks about' with 'discusses,' 'writes,' or similar terms.",
            'utilize': "Use 'use' instead of 'utilize' unless specifying an unexpected use.",
            'you': "Replace 'you' with 'we' or avoid second-person entirely in formal writing.",
            'hence': "This is an older term; consider revising to modern language. Typically, 'hence' should not appear in papers more than once.",
            'proper': "Use 'appropriate' or 'suitable' instead of 'proper.'",
            'properly': "Replace 'properly' with 'appropriately' or a more precise term.",
            'different': "Replace 'different' with 'various' or 'many' where appropriate.",
            'different than': "Replace 'different than' with 'different from.'",
            'mentions': "Avoid 'mentions' and use 'writes,' 'argues,' 'suggests,' or similar terms.",
            'opinion': "Avoid 'opinion' in formal writing; present evidence instead.",
            'very': "Avoid 'very' and use more specific language.",
            'proves': "Researchers collect evidence, and 'evidence' tends to 'suggest,' not 'prove.' In an argument paper, your task is NOT to 'prove' but to 'persuade.' Better to not use this.",
        }

    def analyze_text(self, text):
        """Analyze the text for transitional sentence starters."""
        paragraphs = text.split('\n')
        flagged_text = []
        issues_found = 0

        transitional_starters = [
            "and,", "but,", "so,", "yet,", "or,", "for,", "nor,", "also,"
        ]
        explanations = {
            "and,": "Use 'and' to join sentences, not to start them.",
            "but,": "Use 'but' to join sentences, not to start them.",
            "so,": "Use 'so' to join sentences, not to start them.",
            "yet,": "Use 'yet' to join sentences, not to start them.",
            "or,": "Use 'or' to join sentences, not to start them.",
            "for,": "Use 'for' to join sentences, not to start them.",
            "nor,": "Use 'nor' to join sentences, not to start them.",
            "also,": "Not a good transitional for the start of a sentence, but very good in the middle of a sentence."
        }

        flagged_text.append("<b>^Auto-Peer: Fake Transitionals^</b><br><br>")
        flagged_text.append("The following paragraph has a possible <b>'Transitional Sentence Starter'</b> issue:<br><br>")
        flagged_text.append(text + "<br><br>")
        flagged_text.append("<b>'Transitional Sentence Starter' issues detected from the paragraph above:</b><br><br>")

        issue_number = 1

        for paragraph in paragraphs:
            sentences = re.split(r'\.\s', paragraph)
            for sentence in sentences:
                sentence = sentence.strip()
                for starter in transitional_starters:
                    if sentence.lower().startswith(starter):
                        issues_found += 1
                        capitalized_starter = starter.capitalize()
                        highlighted_sentence = (
                            f"<span style='color:red'>{capitalized_starter}</span>{sentence[len(starter):]}."
                        )
                        flagged_text.append(f"{issue_number}. {highlighted_sentence}<br>")
                        flagged_text.append(
                            f"&nbsp;&nbsp;&nbsp;→ <span style='color:red'>{capitalized_starter}</span>: {explanations[starter]}<br><br>"
                        )
                        issue_number += 1

        flagged_text.append("Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>")
        return {
            "issues_found_counter": issues_found,
            "flagged_text": "".join(flagged_text)
        }
