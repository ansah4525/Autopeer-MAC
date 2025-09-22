import re

class FakeFriendsChecker_real:
    def __init__(self):
        self.issues_found = 0

        # Define fake friends and their suggested alternatives
        self.fake_friends = {
            "a lot": "Typically does not appear in formal writing. Use 'many' instead.",
            "I believe": "Writers should rely on evidence. Use 'argue,' 'suggest,' or 'highlight' instead.",
            "in my opinion": "Avoid expressions of personal opinion; present evidence and reasoned argument instead.",
            "I think": "Impersonal language is preferred. Use 'argue,' 'suggest,' or similar evidence-based verbs.",
            "think": "Impersonal language is preferred. Use 'argue,' 'suggest,' or similar evidence-based verbs.",
            "done": "Use more precise verbs like 'conducted' or 'performed.'",
            "due to": "Use 'because of' or 'caused by' instead. Avoid overuse and ambiguity.",
            "different": "Often redundant or vague. Consider 'various' or 'many' instead.",
            "different than": "Use 'different from' in formal writing.",
            "huge": "Too vague and dramatic. Use 'significant,' 'important,' or 'essential' instead.",
            "prove": "Writers should not claim to 'prove'—use 'suggest' or 'support' instead.",
            "proves": "Use 'suggests' or 'supports' instead.",
            "proved": "Use 'suggested' or 'demonstrated' instead.",
            "proving": "Use 'suggesting' or 'demonstrating' instead.",
            "proven": "Use 'suggested,' 'shown,' or 'demonstrated' instead.",
            "disprove": "Prefer 'refute' or 'fail to support.'",
            "disproves": "Use 'challenges' or 'fails to support' instead.",
            "disproved": "Use 'refuted' or 'challenged' instead.",
            "disproven": "Use 'refuted' or 'not supported' instead.",
            "mention": "Avoid vague verbs. Use 'write,' 'argue,' or 'suggest' instead.",
            "mentioned": "Use 'wrote,' 'argued,' or 'discussed' instead.",
            "mentions": "Use 'writes,' 'suggests,' or 'discusses' instead.",
            "says": "Avoid. Use 'writes,' 'argues,' or 'claims' instead.",
            "states": "Use 'writes' or 'argues' depending on the context.",
            "stated": "Use 'wrote,' 'argued,' or 'claimed' instead.",
            "showcase": "Avoid this term in formal writing.",
            "showcased": "Avoid this term in formal writing.",
            "showcases": "Avoid this term in formal writing.",
            "talk about": "Use 'discuss' or 'explain' instead.",
            "talks about": "Use 'discusses' or 'writes about' instead.",
            "several": "'Several' means around seven; avoid if you mean 'many' or 'various.'",
            "utilize": "Use 'use' unless referring to an unusual or innovative function.",
            "utilizes": "Use 'uses' instead.",
            "utilizing": "Use 'using' instead.",
            "you": "Avoid second-person; rephrase using passive voice or 'we' where suitable.",
            "hence": "Avoid archaic terms; use more modern alternatives like 'thus' or 'therefore.'",
            "proper": "Use 'appropriate' or 'suitable' instead.",
            "properly": "Use 'appropriately' or a more specific term instead.",
            "opinion": "Avoid presenting arguments as opinions. Use evidence instead.",
            "very": "Usually unnecessary. Replace with a stronger adjective or remove entirely."
        }

    def analyze_text(self, text):
        all_paragraphs = text.split("\n")
        gatherall = ""
        sentence_markers = 1
        flagged_sentences = []

        for paragraph in all_paragraphs:
            if not paragraph.strip():
                continue

            for phrase, suggestion in self.fake_friends.items():
                pattern = rf'\b{re.escape(phrase)}\b'
                matches = list(re.finditer(pattern, paragraph, re.IGNORECASE))
                
                for match in matches:
                    self.issues_found += 1
                    start, end = match.span()
                    flagged_phrase = paragraph[start:end]

                    # Highlight phrase red
                    highlighted = (
                        paragraph[:start] 
                        + f"<span style='color:red'>{flagged_phrase}</span>" 
                        + paragraph[end:]
                    )

                    # Prevent duplicate overwrites
                    paragraph = highlighted

                    flagged_sentences.append(
                        f"{sentence_markers}. Detected: <span style='color:red'>{flagged_phrase}</span><br>"
                        f"&nbsp;&nbsp;&nbsp;→ In sentence: {highlighted}<br>"
                        f"&nbsp;&nbsp;&nbsp;→ Suggestion: {suggestion}<br><br>"
                    )
                    sentence_markers += 1

        if flagged_sentences:
            return {
                "issues_found_counter": self.issues_found,
                "issues_para": (
                    "<b>^Auto-Peer: Fake Friends Detected^</b><br><br>"
                    + "<br><br>".join(flagged_sentences)
                    + "<br><br>Click ‘Explanations’ on the Auto-Peer menu if you need further information."
                )
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
