import re

class SymbolIssueChecker:
    def __init__(self):
        self.transitionals = [":", ";", "&"]
        self.ignored_phrases = ['"', '(', ' therefore,', ' however,']

    def analyze_text(self, text):
        """
        Analyze text for overuse of transitional symbols like colons, semicolons, and ampersands.
        Flags paragraphs containing 3+ occurrences of any one of these symbols.
        """
        # Reset counters per run
        issue_found_counter = 0
        symbols_exist = False

        cleaned_text = re.sub(r'\s*\.\s*', '. ', text.strip())
        paragraphs = cleaned_text.splitlines()
        gather_all = ["<b>Auto-Peer: Symbols</b><br><br>"]

        for idx, para in enumerate(paragraphs, start=1):
            para = para.strip()
            if not para:
                continue

            found_one = False
            marked_para = para

            for sym in self.transitionals:
                matches = [m.start() for m in re.finditer(re.escape(sym + " "), para)]
                if len(matches) >= 3:
                    # Highlight the symbol in red
                    marked_para = re.sub(
                        re.escape(sym),
                        f"<span style='color:red'>{sym}</span>",
                        marked_para
                    )
                    found_one = True

            if not found_one:
                continue

            # Only flag if symbols exist
            if "color:red" in marked_para:
                symbols_exist = True
                issue_found_counter += 1
                gather_all.append(
                    f"<u>Paragraph {idx}</u>:<br>{marked_para}<br><br>"
                )

        if symbols_exist:
            explanation = (
                "This issue flags overuse of symbols such as colons (:), semicolons (;), or ampersands (&).<br><br>"
                "Using multiple symbols in a single paragraph may confuse readers or indicate overly complex sentence structures.<br><br>"
                "Try breaking up long thoughts into simpler sentences.<br><br>"
                "Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br>"
            )
            return {
                "issues_found_counter": issue_found_counter,
                "issues_para": "<br>".join(gather_all) + "<br>" + explanation
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
