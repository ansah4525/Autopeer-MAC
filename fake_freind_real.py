import re

class FakeFriendsChecker_real:
    def __init__(self):
        self.issues_found = 0

        # Define fake friends
        self.fake_friends = [
            "a lot", "I believe", "in my opinion", "I think", "done", "due to",
            "different", "different than", "huge", "prove", "proves", "proved", "proving",
            "proven", "disprove", "disproves", "disproved", "disproven", "mention",
            "mentioned", "mentions", "says", "states", "stated", "showcase", "showcased",
            "showcases", "talk about", "talks about", "several", "utilize", "utilizes",
            "utilizing", "you", "hence", "proper", "properly", "opinion", "very"
        ]

    def analyze_text(self, text):
        all_paragraphs = text.split("\n")
        gatherall = ""
        paragraph_number = 1
        flagged_paragraphs = []

        for paragraph in all_paragraphs:
            if not paragraph.strip():
                continue

            paragraph_lower = paragraph.lower()
            found_any = False

            for phrase in self.fake_friends:
                pattern = rf'\b{re.escape(phrase)}\b'
                matches = list(re.finditer(pattern, paragraph_lower, re.IGNORECASE))

                if matches:
                    found_any = True
                    # Highlight all occurrences in red
                    for match in matches:
                        start, end = match.span()
                        flagged_phrase = paragraph[start:end]
                        paragraph = paragraph[:start] + f"<span style='color:red'>{flagged_phrase}</span>" + paragraph[end:]
                        paragraph_lower = paragraph.lower()  # update lower for further matches

            if found_any:
                self.issues_found += 1
                # Bold the whole paragraph
                highlighted_para = f"<b>{paragraph}</b>"
                flagged_paragraphs.append(f"{paragraph_number}. {highlighted_para}")
                paragraph_number += 1

        if flagged_paragraphs:
            return {
                "issues_found_counter": self.issues_found,
                "issues_para": (
                    "<b>Auto-Peer: Fake Friends Detected</b><br><br>"
                    + "<br><br>".join(flagged_paragraphs)
                    + "<br><br>Click ‘Explanations’ on the Auto-Peer menu if you need further information."
                )
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
