import re

class CounterArgumentCheckerXojoExact:
    def __init__(self, min_sentences=3):
        self.listArr = [
            "Critics argue",
            "Critics may argue",
            "Many people argue",
            "One problem with",
            "Opponents argue that",
            "Other people argue",
            "People argue that",
            "People may argue that",
            "Proponents of ... argue",
            "Some argue",
            "Some argue against",
            "Some critics argue",
            "Some may argue",
            "Some opponents",
            "Some people argue that",
            "Some people may argue that",
            "Some people say",
            "Some people say that",
            "On the other hand,",
            "Despite ... some argue",
            "Opponents of ... argue"
        ]
        self.custom_min_sentences = min_sentences
        self.issues_found_counter = 0
        self.sentence_number = 1

    def analyze_text(self, text):
        working_text = text.strip().replace(" . ", ". ")
        all_paragraphs = working_text.splitlines()
        gather_all = ""

        for para in all_paragraphs:
            found_one = False
            found_two = False
            all_sentences = para.split(". ")
            if len(all_sentences) < self.custom_min_sentences:
                continue

            for phrase in self.listArr:
                if "..." in phrase:
                    first, second = phrase.split("...")
                    if first in para and second in para:
                        found_two = True
                        break
                else:
                    if phrase in para:
                        found_one = True
                        break

            if not found_one and not found_two:
                continue

            # Only analyze the first sentence
            first_sentence = all_sentences[0]
            if len(first_sentence) <= 5:
                continue

            if found_two:
                for phrase in self.listArr:
                    if "..." in phrase:
                        first, second = phrase.split("...")
                        if first in first_sentence and second in first_sentence:
                            highlighted = (
                                first_sentence.replace(
                                    first, f"<span style='color:red'>{first}</span>"
                                ).replace(
                                    second, f"<span style='color:red'>{second}</span>"
                                )
                            )
                            gather_all += f"{self.sentence_number}. {highlighted}.<br><br>"
                            self.issues_found_counter += 1
                            self.sentence_number += 1
                            break
            else:
                for phrase in self.listArr:
                    if phrase in first_sentence:
                        highlighted = first_sentence.replace(
                            phrase, f"<span style='color:red'>{phrase}</span>"
                        )
                        gather_all += f"{self.sentence_number}. {highlighted}.<br><br>"
                        self.issues_found_counter += 1
                        self.sentence_number += 1
                        break

        if self.issues_found_counter > 0:
            explanation = (
                "Possible counter-arguments were found and highlighted.<br><br>"
                "These help ensure argumentative balance and critical thinking.<br><br>"
                "Click ‘Explanations’ on the Auto-Peer menu for further information.<br><br>"
            )
            return {
                "issues_found_counter": self.issues_found_counter,
                "issues_para": (
                    "<b>^Auto-Peer: Counter Argument^</b><br><br>"
                    "Possible counter arguments found:<br><br>"
                    + gather_all
                    + explanation
                )
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": (
                    "Auto-Peer could not detect any 'obvious' signs of counter-arguments.<br><br>"
                    "This does not mean none are present. Counter-arguments often begin with phrases like:<br><br>"
                    "<span style='color:red'>Critics argue</span>, "
                    "<span style='color:red'>On the other hand</span>, "
                    "<span style='color:red'>Despite ... some argue</span>, etc.<br><br>"
                )
            }
