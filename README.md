Auto-Peer: Academic Writing Feedback Tool

Auto-Peer is a Python-based text analysis tool designed to provide automated feedback on academic writing. It mimics aspects of peer review by scanning essays, reports, or papers for common stylistic, structural, and grammatical issues. The system highlights problematic text directly, explains why it may be an issue, and suggests possible improvements — all in an easy-to-read, HTML-formatted output.

✨ Features

Sentence & Paragraph Checks

Detects long sentences that may reduce clarity.

Flags paragraphs that are too short or too long, helping maintain balanced structure.

Highlights weak or repetitive paragraph endings.

Word Choice & Grammar Issues

Identifies misuse of may vs. might and which vs. that.

Flags fake friends (problematic or informal words in academic writing).

Catches unclear pronouns (it, they, this, these).

Detects excessive numbers/figures written as digits instead of words.

Stylistic Issues

Marks lonely transitionals (e.g., However,, Therefore,) when they appear weak at the start of a paragraph.

Highlights sentence starter problems (And, But, So, etc. when followed by a comma).

Finds overused symbols (colons, semicolons, ampersands).

Reference & Citation Checks

Detects paragraphs lacking references across consecutive sections.

Flags problematic reference placement, such as a single citation dumped at the end of a paragraph.

Explanatory Output

Each issue is reported with red highlights for problematic words or structures.

Entire paragraphs or sentences are bolded for context.

Includes concise explanations with suggestions for revision.

🔧 Technology Stack

Python

Regex for pattern detection

spaCy (en_core_web_sm) for advanced NLP checks

HTML-formatted output for integration with GUIs (e.g., PyQt)

🚀 Use Cases

Students polishing academic essays, research papers, or theses.

Educators offering automated writing feedback.

Researchers running quick style and citation checks before submission.

Developers integrating writing diagnostics into text-editing applications.
