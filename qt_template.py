import sys
import pyttsx3
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
#check
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QApplication, QMenuBar, QTextEdit
# from PyQt5.QtGui import QTextCursor

#add the python file and the name of class used 
from sentence_starter import TextAnalyzer
from inclusive import inclu_sent
from sen_len import SentenceAnalyzer
from fake_friend import FakeFriendsChecker
from para_length import ParagraphLengthChecker
from might import MayVsMightChecker
from double_tran import DoubledTransitionalsChecker
from lonely_trans import LonelyTransitionalsChecker
from topic_s import TopicSentenceChecker
from choppy import ChoppySentenceChecker
from fake_freind_real import FakeFriendsChecker_real
from numbers_issue import NumbersIssueChecker
from prob_ref import ReferencePositioningChecker
from missing_ref import MissingReferenceChecker
from symbols import SymbolIssueChecker
from that_which import WhichVsThatChecker
from contractions import ContractionsCheckerXojoExact
from counter import CounterArgumentCheckerXojoExact
from pronoun import PronounCohesionCheckerXojoExact
from unclear_this import UnclearThisIssueChecker
from synthesis import SynthesisCheckerXojoExact
from para_end import ParagraphEndingChecker
from complex_sen import OverlyComplexSentenceChecker

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
                             QPushButton, QComboBox, QMessageBox, QAction, QMenu)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import os
from openai import OpenAI
from gptcheck import GPTChatDialog
from evaluator import EvaluatorWindow
import sys, os


class mainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.is_dark_mode = False
        self.text_edit = QTextEdit(self)

        self.setWindowTitle("Auto Peer 2024")
        #self.setWindowIcon(qtg.QIcon("./face2.jpeg"))
        

        def resource_path(relative_path):
            """ Get absolute path to resource (for dev and PyInstaller exe) """
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath("."), relative_path)

        icon_path = resource_path("logologotype.jpg")
        self.setWindowIcon(qtg.QIcon(icon_path))



        # Create a menu bar
        menubar = self.menuBar()

        # Create File menu and add actions
        file_menu = menubar.addMenu('File')
        file_menu.addAction('Open')
      
        file_menu.addAction('Exit')

        # Create Edit menu and add actions
        edit_menu = menubar.addMenu('Edit')
        edit_menu.addAction('Cut')
        edit_menu.addAction('Copy')
        edit_menu.addAction('Paste')

    #     # Create View menu and add actions
    #     view_menu = menubar.addMenu('Analyze')
    #    # Initialize the menu bar
    #     menubar = self.menuBar()

        # 'Analyze' menu
        view_menu = menubar.addMenu('Analyze')

        # 'Analyze Everything' action
        analyze_every = QAction('Analyze Everything!', self)
        analyze_every.triggered.connect(self.open_result_window_single)
        view_menu.addAction(analyze_every)

        issue_counter = QAction('View Total Number of Issues', self)
        issue_counter.triggered.connect(lambda: self.open_result_window_single(100))
        view_menu.addAction(issue_counter)

        # 'Paragraph Level Issues' submenu
        paragraph_menu = QMenu('Paragraph Level Issues', self)
        view_menu.addMenu(paragraph_menu)

        # Add actions to 'Paragraph Level Issues' submenu
        paragraph_length = QAction('Paragraph Length', self)
        paragraph_length.triggered.connect(lambda: self.open_result_window_single(1))
        paragraph_menu.addAction(paragraph_length)

        paragraph_end = QAction('Paragraph Endings', self)
        paragraph_end.triggered.connect(lambda: self.open_result_window_single(22))
        paragraph_menu.addAction(paragraph_end)

        #Add lonely and doubvled transitionals to paragraph level
        # Add actions to 'Paragraph Level Issues' submenu
        double_trans = QAction('Double Transitionals', self)
        double_trans.triggered.connect(lambda: self.open_result_window_single(7))
        paragraph_menu.addAction(double_trans)

        lonely_trans = QAction('Lonely Transitionals', self)
        lonely_trans.triggered.connect(lambda: self.open_result_window_single(8))
        paragraph_menu.addAction(lonely_trans)

        topic_s = QAction('Topic Sentences', self)
        topic_s.triggered.connect(lambda: self.open_result_window_single(9))
        paragraph_menu.addAction(topic_s)

        # 'Sentence Level Issues' submenu
        sentence_menu = QMenu('Sentence Level Issues', self)
        view_menu.addMenu(sentence_menu)

        # Add actions to 'Sentence Level Issues' submenu
        sentence_length = QAction('Sentence Length', self)
        sentence_length.triggered.connect(lambda: self.open_result_window_single(2))
        sentence_menu.addAction(sentence_length)

        over_complex = QAction('Overly Complex Sentences', self)
        over_complex.triggered.connect(lambda: self.open_result_window_single(23))
        sentence_menu.addAction(over_complex)

        sentence_starters = QAction('Sentence Starters', self)
        sentence_starters.triggered.connect(lambda: self.open_result_window_single(3))
        sentence_menu.addAction(sentence_starters)

        choppy = QAction('Choppy Sentences', self)
        choppy.triggered.connect(lambda: self.open_result_window_single(10))
        sentence_menu.addAction(choppy)

        # 'Wording Issues' submenu
        wording_menu = QMenu('Wording Issues', self)
        view_menu.addMenu(wording_menu)
 
        # Add actions to 'Wording Issues' submenu
        fake_friends = QAction('Fake Transitionals', self)
        fake_friends.triggered.connect(lambda: self.open_result_window_single(4))
        wording_menu.addAction(fake_friends)

        unthis = QAction('Unclear This Issue', self)
        unthis.triggered.connect(lambda: self.open_result_window_single(21))
        wording_menu.addAction(unthis)

        pronoun1 = QAction('Pronoun Cohesion', self)
        pronoun1.triggered.connect(lambda: self.open_result_window_single(20))
        wording_menu.addAction(pronoun1)
         # Add actions to 'Wording Issues' submenu
        contr = QAction('Contractions', self)
        contr.triggered.connect(lambda: self.open_result_window_single(18))
        wording_menu.addAction(contr)

        
        # Add actions to 'Wording Issues' submenu
        commawhich = QAction('That vs COMMA which', self)
        commawhich.triggered.connect(lambda: self.open_result_window_single(16))
        wording_menu.addAction(commawhich)

        # Add actions to 'Wording Issues' submenu
        fake_friends_real = QAction('Fake Friends', self)
        fake_friends_real.triggered.connect(lambda: self.open_result_window_single(11))
        wording_menu.addAction(fake_friends_real)

        inclusive_terms = QAction('Inclusive Terms', self)
        inclusive_terms.triggered.connect(lambda: self.open_result_window_single(5))
        wording_menu.addAction(inclusive_terms)

        may= QAction('MAY VS MIGHT HAVE', self)
        may.triggered.connect(lambda: self.open_result_window_single(6))
        wording_menu.addAction(may)

        number=QAction('Numbers Issue', self)
        number.triggered.connect(lambda: self.open_result_window_single(12))
        wording_menu.addAction(number)

        # 'Textual Issues' action
        textual_issues = QMenu('Textual Issues', self)
        #textual_issues.triggered.connect(self.check_textual_issues)
        view_menu.addMenu(textual_issues)

        syn = QAction('Synthesis Issue', self)
        syn.triggered.connect(lambda: self.open_result_window_single(17))
        textual_issues.addAction(syn)

        counter1 = QAction('Counter Arguments', self)
        counter1.triggered.connect(lambda: self.open_result_window_single(19))
        textual_issues.addAction(counter1)

        # 'Punctuational Issues' action
        punctuational_issues = QMenu('Punctuational Issues', self)
        #punctuational_issues.triggered.connect(self.check_punctuational_issues)
        view_menu.addMenu(punctuational_issues) #CHANGE THIS TO ADD MENU WHEN YOU START ADDIN THINGS 

               # Add actions to 'Wording Issues' submenu
        symbols = QAction('Symbols Issue', self)
        symbols.triggered.connect(lambda: self.open_result_window_single(15))
        punctuational_issues.addAction(symbols)

        # 'Referencing Issues' action
        ref_issues = QMenu('Reference Issues', self)
        #textual_issues.triggered.connect(self.check_textual_issues)
        view_menu.addMenu(ref_issues)

        # Add actions to 'Paragraph Level Issues' submenu
        problem_ref = QAction('Problematic Reference', self)
        problem_ref.triggered.connect(lambda: self.open_result_window_single(13))
        ref_issues.addAction(problem_ref)

        # Add actions to 'Paragraph Level Issues' submenu
        missing_ref1 = QAction('Missing Reference', self)
        missing_ref1.triggered.connect(lambda: self.open_result_window_single(14))
        ref_issues.addAction(missing_ref1)


        # 'Final Report' action
        final_report = QAction('Final Report', self)
        #add here later the definition 
        #final_report.triggered.connect(self.generate_final_report)
        view_menu.addAction(final_report)

        # # Connect actions to methods
        # analyze_every.triggered.connect(self.open_result_window)

        #Create options menu 
        option_menu = menubar.addMenu('Options')
        option_menu.addAction('Clear Text')
        option_menu.addAction('Settings')
        option_menu.addAction('Paste')

        # Create accessibility menu 
        accessibility_menu = menubar.addMenu('Accessibility')
        increase_font_action = QAction('Increase Font', self)
        increase_font_action.triggered.connect(self.increase_font_size)
        accessibility_menu.addAction(increase_font_action)
        
        decrease_font_action = QAction('Decrease Font', self)
        decrease_font_action.triggered.connect(self.decrease_font_size)
        accessibility_menu.addAction(decrease_font_action)

        change_theme_action = QAction('Change text box color', self)
        change_theme_action.triggered.connect(self.change_color_theme)
        accessibility_menu.addAction(change_theme_action)

        change_speech_action = QAction('Text to Speech', self)
        change_speech_action.triggered.connect(self.text_to_speech)
        accessibility_menu.addAction(change_speech_action)


        #Create practice menu 

        practice_menu = menubar.addMenu('Practice')
        practice_menu.addAction('In development')

        #Create Explanations menu 
        explanation_menu = menubar.addMenu('Explanations')
        # in your mainWindow.__init__ after you build other menus:
        tools_menu = menubar.addMenu('Tools')

        open_chat = QAction('Open GPT Chat…', self)
        open_chat.triggered.connect(self.open_gpt_chat_dialog)
        tools_menu.addAction(open_chat)


        eval_action = QAction('The Evaluator', self)
        eval_action.triggered.connect(self.open_evaluator)
        tools_menu.addAction(eval_action)

        self._chat_dialog = None
        

        paragraph_action = explanation_menu.addAction('Paragraph length')
        sentence_action = explanation_menu.addAction('Sentence length')
        inclusive_action = explanation_menu.addAction('Inclusive Terms')
        may_action = explanation_menu.addAction('MAY vs MIGHT have issue')
        double_action = explanation_menu.addAction('Double Transitionals')
        fake_trans_action = explanation_menu.addAction('Fake transitionals')
        sen_start_action = explanation_menu.addAction('Sentence Starter')
        lonely_action = explanation_menu.addAction('Lonely Transitionals')
        explain_topic_sentence = explanation_menu.addAction('Topic Sentence')
        choppy_sentence = explanation_menu.addAction('Choppy Sentences')
        fake_friends= explanation_menu.addAction('Fake Friends')
        numberss=explanation_menu.addAction('Numbers Issue')
        pref1=explanation_menu.addAction('Problematic Referencing')
        missing_ref2=explanation_menu.addAction("Missing Referencing")
        symbols_issue=explanation_menu.addAction("Symbols Issue")
        that_which=explanation_menu.addAction("That vs COMMA which issue")
        syn_ex=explanation_menu.addAction("Synthesis Issue")
        cont_ex=explanation_menu.addAction("Contractions")
        counter_ex=explanation_menu.addAction("Counter Arguments")
        pronoun_ex= explanation_menu.addAction("Pronoun Cohesion")
        unthis_ex= explanation_menu.addAction("Unclear This Issue")
        par_end_ex=explanation_menu.addAction("Paragraph Endings")
        over_comp_ex=explanation_menu.addAction("Overly Complex Sentences")

        # Connect actions to methods
        #paragraph_action.triggered.connect(self.explain_paragraph_length)
        sentence_action.triggered.connect(self.explain_sentence_length)
        inclusive_action.triggered.connect(self.explain_inclusive_sentences)
        may_action.triggered.connect(self.explain_may_issue)
        double_action.triggered.connect(self.explain_double_cohesion)
        fake_trans_action.triggered.connect(self.explain_fake_transitionals)
        sen_start_action.triggered.connect(self.explain_sen_start)
        lonely_action.triggered.connect(self.explain_lonely)
        explain_topic_sentence.triggered.connect(self.explain_topic_sentence)

        choppy_sentence.triggered.connect(self.explain_choppy_sentence)
        fake_friends.triggered.connect(self.explain_fake_freinds)
        numberss.triggered.connect(self.explain_num_issue)
        pref1.triggered.connect(self.explain_problematic_ref)
        missing_ref2.triggered.connect(self.explain_missing_ref)
        symbols_issue.triggered.connect(self.explain_symbol)
        that_which.triggered.connect(self.explain_thatwhich)
        syn_ex.triggered.connect(self.explain_synthesis)
        cont_ex.triggered.connect(self.explain_contraction)
        counter_ex.triggered.connect(self.explain_counter)
        pronoun_ex.triggered.connect(self.explain_pronoun)
        unthis_ex.triggered.connect(self.explain_unthis)
        par_end_ex.triggered.connect(self.explain_paraend)
        over_comp_ex.triggered.connect(self.explain_over_ex)

         # Create Help menu and add actions
        help_menu = menubar.addMenu('Help')
        help_menu.addAction('About')

        # Set central widget and layout
        central_widget = qtw.QWidget()
        central_layout = qtw.QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Add horizontal layout for icon and additional text
        h_layout = qtw.QHBoxLayout()

        # Add info icon
        info_icon_label = qtw.QLabel(self)
        info_icon_label.setPixmap(self.style().standardIcon(qtw.QStyle.SP_MessageBoxInformation).pixmap(30, 30))
        h_layout.addWidget(info_icon_label)
        
        # Set zero spacing between icon and text
        h_layout.setSpacing(0)

        # Add QLabel for additional text below menu bar
        additional_label = qtw.QLabel("<h4>Use the 'Explanations' tab on the menu to see information on any writing issue</h4>", self)
        additional_label.setFont(qtg.QFont('Times New Roman', 10))  # Adjust font if needed
        h_layout.addWidget(additional_label)


        # Add the horizontal layout to the central layout
        central_layout.addLayout(h_layout)

        # Create QTextEdit widget for large input box
        self.input_box = qtw.QTextEdit(central_widget, placeholderText="Enter text here")
        self.input_box.setStyleSheet("""
            background-color: lightyellow; 
            border: 2px solid darkblue; 
            border-radius: 10px;
            padding: 10px;
        """)  # Set yellow background color and blue border
        font = qtg.QFont('Times New Roman', 12)
        self.input_box.setFont(font)
        self.input_box.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        # Add input box to central layout with margins and spacing
        central_layout.addWidget(self.input_box)
        central_layout.setContentsMargins(20, 10, 20, 50)  # Adjust margins (left, top, right, bottom)
        central_layout.setSpacing(10)  # Adjust spacing between widgets

        # Make the input box take up more vertical space
        central_layout.setStretch(0, 1)  # Stretch factor for the horizontal layout (icon + additional_label)
        central_layout.setStretch(1, 5)  # Stretch factor for input_box

        # Add the button
        button1 = qtw.QPushButton("Analyze Text!", central_widget)
        button1.setStyleSheet("""
            QPushButton {
                background-color: lightblue;
                border: 2px solid #8f8f91;
                border-radius: 15px;
                font-family: 'Times New Roman';
                font-size: 10pt;
                font-weight: bold;
            }
        """)
        button1.setFixedSize(150, 40)  # Set a fixed size for the button

        # Add the button to central layout and center it
        button_layout = qtw.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button1)
        button_layout.addStretch()
        central_layout.addLayout(button_layout)

        # Connect the button click to open a new window
        button1.clicked.connect(self.open_result_window)

        self.result_window = None  # Initialize the result window attribute
            # Instantiate the TextAnalyzer
        #check add mroe text analyzers
        self.text_analyzer1 = ParagraphLengthChecker()
        self.text_analyzer2=TextAnalyzer()
        self.text_analyzer3=SentenceAnalyzer()
        self.text_analyzer4=FakeFriendsChecker()
        self.text_analyzer5=inclu_sent()
        self.text_analyzer6=MayVsMightChecker()
        self.text_analyzer7=DoubledTransitionalsChecker()
        self.text_analyzer8=LonelyTransitionalsChecker()
        self.text_analyzer9=TopicSentenceChecker()
        self.text_analyzer10=ChoppySentenceChecker()
        self.text_analyzer11=FakeFriendsChecker_real()
        self.text_analyzer12=NumbersIssueChecker()
        self.text_analyzer13=ReferencePositioningChecker()
        self.text_analyzer14=MissingReferenceChecker()
        self.text_analyzer15=SymbolIssueChecker()
        self.text_analyzer16=WhichVsThatChecker()
        self.text_analyzer17=SynthesisCheckerXojoExact()
        self.text_analyzer18=ContractionsCheckerXojoExact()
        self.text_analyzer19=CounterArgumentCheckerXojoExact()
        self.text_analyzer20=PronounCohesionCheckerXojoExact()
        self.text_analyzer21=UnclearThisIssueChecker()
        self.text_analyzer22=ParagraphEndingChecker()
        self.text_analyzer23=OverlyComplexSentenceChecker()


        self.resize(800, 600)  # Adjust window size

        # Create and show the welcome dialog
        self.show_welcome_dialog()

        self.show()




        # in your mainWindow class:
    def open_gpt_chat_dialog(self):
        if self._chat_dialog is None:
            self._chat_dialog = GPTChatDialog(self)
        self._chat_dialog.show()
        self._chat_dialog.raise_()
        self._chat_dialog.activateWindow()

    def open_evaluator(self):
        self.eval_win = EvaluatorWindow()   # create a new instance
        self.eval_win.show()
    
    def increase_font_size(self):
        # Get the current font
        current_font = self.input_box.font()
        
        # Increase the font size by 6 points
        current_font.setPointSize(current_font.pointSize() + 6)
        
        # Apply the font to the entire QTextEdit content using the document
        self.input_box.setFont(current_font)


    def decrease_font_size(self):
        current_font = self.input_box.font()
        
        # Decrease the font size by 4 points
        current_font.setPointSize(current_font.pointSize() - 4)
        
        # Apply the font to the entire QTextEdit content using the document
        self.input_box.setFont(current_font)
    
    # Text to Speech method
    def text_to_speech(self):
    # Initialize the pyttsx3 engine
        engine = pyttsx3.init()
        
        # Get the text from the input box
        text = self.input_box.toPlainText()
        
        # Check if there's text to convert
        if text.strip():
            # Speak the text
            engine.say(text)
            engine.runAndWait()
        else:
            # If there's no text, you can show a warning or just do nothing
            qtw.QMessageBox.warning(self, 'Warning', 'No text to convert to speech.')


    def change_color_theme(self):
        if self.is_dark_mode:
        # Switch to light mode
            self.setStyleSheet("")
            self.input_box.setStyleSheet("""
                background-color: white; 
                border: 2px solid blue; 
                border-radius: 10px;
                color: black;  # Ensure text color is black in light mode
            """)
            self.is_dark_mode = False
        else:
        # Switch to dark mode
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2E2E2E;
                    color: white;  # Ensure text color is white in dark mode
                }
                QLabel, QMenuBar, QMenu, QAction, QPushButton, QTextEdit {
                    color: white;  # Ensure text color is white in dark mode
                }
            """)
            self.input_box.setStyleSheet("""
                background-color: #1E1E1E; 
                border: 2px solid #444;
                border-radius: 10px;
                color: white;  # Ensure text color is white in dark mode
            """)
            self.is_dark_mode = True


    def open_result_window_single(self, issue_number):
        # Method to handle opening result windows for specific issues
        if self.result_window:
            self.result_window.close()
        self.result_window = ResultWindow(issue_number)
        print("entered")
        self.result_window.show()



        

    def show_welcome_dialog(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Welcome")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        welcome_label = qtw.QLabel("WELCOME TO AUTOPEER:)", dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))

        dialog_layout.addWidget(welcome_label)
        
        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(300, 100)  # Adjust dialog size
        dialog.show()
    
    def explain_inclusive_sentences(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Topic Sentence")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
        INCLUSIVE TERMS

        There is a large number of words used in everyday English that are offensive or insensitive to many people.


        Many of these words are still commonly used, but wherever and whenever possible, we should try to use the terms that are deemed more inclusive or sensitive.


        Please review the Inclusive Language Table below and consider if the inclusive term is more appropriate in your writing.


        Inclusive Language Table: Original terms and Inclusive terms

        Actress, actresses   -->  Actor

        Addict   -->  Someone struggling with addiction

        Alcoholic   -->  Someone with alcoholism, someone with an alcohol problem

        Bipolar person   -->  Someone with bipolar disorder

        Businessman, businessmen   -->  Businessperson

        Chairman, chairmen   -->  Chair, chairperson, coordinator, head

        (The) common man   -->  The average person

        Congressman, congresswoman   -->  Legislator, congressional representative

        Diabetic   -->  Person with diabetes

        Disabled person, handicapped, cripple   -->  Person with a disability

        Distressed neighborhood   -->  Neighborhoods with access to fewer opportunities

        Down's syndrome person   -->  Person with Down syndrome

        Drug lord   -->  Person who was arrested for selling drugs

        The elderly   -->  Older adults

        Foreigners   -->  Immigrant, visitors, travelers

        Freshman   -->  First-year student

        Homeless people, the homeless   -->  People experiencing homelessness

        Inner city   -->  Urban areas, Under-resourced

        Layman, laymen   -->  Layperson

        Maiden name   -->  Family name

        Mailman, mailmen   -->  Mail carrier, letter carrier, postal worker

        Mankind   -->  People, human beings, humanity

        Man-made, manmade   -->  Machine-made, synthetic, artificial

        Manpower   -->  Workforce

        Mentally ill   -->  Person with DSM diagnosis

        Office girls   -->  Office Staff

        Policeman, policewoman, policemen, policewomen   -->  Police officer

        Recovering drug addict   -->  In recovery

        Retarded   -->  Mentally disabled

        Salesman, salesmen   -->  Salesperson/ Sales representative

        Sex-change, sex-change operation   -->  Sex reassignment (SRS) or gender affirming surgery

        S/he, he or she, she or he   -->  Use "they" and pluralize preceding noun

        Spokesman, spokesmen   -->  Spokesperson

        Stewardess, stewardesses   -->  Flight attendant

        Substance abuse   -->  Substance use disorder, people living with substance use disorder

        Transgendered   -->  Transgender person

        Weatherman, weathermen   -->  Weather reporter/ forecaster

        Wheelchair-bound   -->  Person who uses a wheelchair


        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensure the dialog stays open until closed

    

    def explain_lonely(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Overly Complex Sentences")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
        “LONELY TRANSITIONALS”

        A ‘lonely transitional’ is a transitional that occurs in a topic sentence at the start of a paragraph.

        Because a topic sentence seeks to introduce a new topic, the information from the previous paragraph is assumed to be complete. As such, if the topic sentence needs to refer to any of the previous paragraph’s information, a ‘full transitional clause’ rather than a simple transitional is required. For example, consider the following topic sentence, which includes a lonely transitional.

        “In addition, criminal gangs have started to take advantage of sun-seeking holiday makers.”

        For the sentence above, the writer has put the burden of recall on the reader. That is, the writer expects the reader to retrieve the information to which the phrase ‘in addition’ refers. However, as this sentence is the start of a new paragraph, the burden lies on the writer to remind the reader of the information. As such, a full transitional clause is required as in the example below.

        “In addition to the problem of over-crowded beaches, criminal gangs have started to take advantage of sun-seeking holiday makers.”

        In the list below, the lonely transitional has been given a ‘full clause transitional’ alternative. 

        Accordingly: "Following the procedure described above ..."

        Additionally: "In addition to the problem of waste management ... "

        Also: "Deforestation is also a problem in Africa ..."

        As a result: "As a result of deforestation ..."

        Besides:  "In addition to the problem of waste management ... "

        By contrast:  "In contrast to the problem of waste management ... "

        Consequently: "As a consequence of the problem of deforestation ..."

        Conversely:   "In contrast to the problem of waste management ... "

        Especially:  "A good example of effective solar energy production can be found in ... "

        For example: "An example of effective solar energy production can be found in ... "

        For instance "An example of effective solar energy production can be found in ... "

        Furthermore: "In addition to the problem of waste management .... "

        Hence: "As a result of this deforestation, ... "

        However:  "In contrast to the problem of waste management ... "

        In addition:  "In addition to the problem of waste management ...."

        In contrast:  "In contrast to the problem of waste management ... "

        In particular:  "A good example of effective solar energy production can be found in ... "

        Particularly: "A good example of effective solar energy production can be found in ... "

        Likewise: "Similar to the problem of deforestation, ... "

        Namely: "A specific example of the issue of deforestation is ... "

        Otherwise: "If this problem with deforestation is not resolved, .... "

        Similarly: "Similar to the problem of deforestation, ... "

        Thereby: "Through this use of genetic engineering ... "

        Therefore: "As a result of this deforestation, ... "

        Thus: "As a result of this deforestation, ... "

        Moreover: More importantly than deforestation, ...
        Second: The first [issue/problem etc.] [is/refers to/concerns etc.] deforestation, ...


        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensure the dialog stays open until closed



    
    def explain_sen_start(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Fake Friends")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
        “SENTENCE STARTER ISSUES”

        A ‘Sentence Starter Issue’ refers to the questionable choice of word used to start a sentence.

        The clauses of a sentence are frequently joined using coordinating conjunctions (e.g., ‘and,’ ‘but’), and subordinating conjunctions (e.g., ‘because,’ ‘although’).
        Although these words do sometimes start sentences, it is never necessary for them to be used in this way, and many instructors actively discourage their use to start sentences.

        There are many other examples of sentence starter issues, including the use of ‘well,’ which is common in speech, but not in writing.

        In the list below, the sentence starter issue has been given an alternative structure.

        Also: Move 'also' from the start of the sentence (e.g., "Waste management is also a problem in ... ")

        And: 'And' joins sentences (e.g., "Waste management is a problem in many countries, and it is also an opportunity for development specialists.")

        Because: 'Because' usually joins sentences (e.g., "Deforestation is taking place in many countries because local people need the land to grow crops.")

        But:  'But' joins sentences (e.g., "Waste management is a problem in many countries, but it can also be seen as an opportunity for development specialists.")

        Or: 'Or' joins sentences (e.g., "Waste management can be seen as a problem is many countries, or it is also be seen as an opportunity for development specialists.")

        Nor:  'Nor' joins sentences (e.g., "Waste management is neither a problem for many countries, nor it is an opportunity for development specialists.")

        So:   'So' joins sentences (e.g., "Waste management is a problem in many countries, so development specialists need to come up with a solution.")

        Yet: 'Yet' joins sentences (e.g., "Waste management is a problem in many countries, yet some people see it as an opportunity for development specialists.")

        Well: This word is often used in speech, but no word is necessary when writing.




        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensure the dialog stays open until closed
    
    def explain_pronoun(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Pronoun Cohesion")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
       “PRONOUN COHESION”

Pronouns are words like "it," "they," "them," "he," "she," "him," and "her."
These words are very convenient, and they are often very useful, but sometimes they can negatively impact the cohesion of writing.
More specifically, when we use words like "it" and "they" at the start of a sentence, it is not obviously clear to what we are referring. After-all, the referent of the "it" and "they" may be buried in the details of the last sentence.
Similarly, it is not obviously clear to what we are referring when we use words like "it" and "them" at the end of a sentence. 
This said, we do use these words if they are around the middle of the sentence.


Consider the examples below. Note that "Version A" is the original, but "Version B" has been tweaked to remove the pronoun and make the sentence that much clearer.


Example 1
A/ One of these misconceptions is that home-schooled students are sheltered from the outside world and are isolated from society. It is important to dispel these misbeliefs to ensure that home-schooled students are treated equally to their peers.

B/ One of these misconceptions is that home-schooled students are sheltered from the outside world and are isolated from society. Dispelling these misbeliefs is important to ensuring that home-schooled students are treated equally to their peers.


Example 2
A/ The money loses value because of negative rates, and the consumers are forced to spend to unlock the value hidden by the liquidity trap. It is similarly difficult to achieve other economic outcomes by solely applying monetarist principles.

B/ The money loses value because of negative rates, and the consumers are forced to spend to unlock the value hidden by the liquidity trap. Other economic outcomes are similarly difficult to achieve by solely applying monetarist principles.


Example 3
A/ The method requires brain signals with their respective frequencies to analyze them.

B/ The method requires brain signals with an analysis of their respective frequencies.


Example 4
A/ Although the discussed arguments have merit, there are many cases of repatriation requests that challenge them.

B/ Although the discussed arguments have merit, there are many challenges to cases of repatriation requests.


Example 5
A/ If adopted in the United States, the model may deter them.

B/ If adopted in the United States, the model may act as a deterrent.


Note that pronouns do not have to be exactly at the beginning of a sentence. Instead, the pronoun may immediately follow a transitional (as in Example 6).


Example 6
A/ As the community becomes more diverse, people tend to lose trust. That is, they act according to what they believe is correct according to local culture.

B/ As the community becomes more diverse, people tend to lose trust. That is, these people act according to what they believe is correct according to the local culture.


Usually, pronouns like "it," and "they/them" are the hardest to process if they are used at sentence initial or sentence ending positions. However, pronouns such as she/her and he/him are also problematic.

If you have used "she" or "he" to start a sentence, try replacing them with phrases such as "the study," "the author," "the writer," or whatever else is most appropriate. You can do something similar if your sentences end with "her" or "him."


Note that the pronouns "I" and "we" are perfectly acceptable to begin sentences. These pronouns always refer to the same people so there is very little chance of misunderstanding.




        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensure the dialog stays open until closed


    def explain_unthis(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Unclear This")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
      “UNCLEAR THIS”

The use of ‘this + noun’ is critical to the cohesion of a paragraph.
‘This + noun’ informs the reader that the information to come relates directly to the information previously presented.
If the noun is missing from the ‘this-phrase’ then the cohesion is seriously undermined.

Consider the sentences below:

1/ “This must not be allowed.”
2/ “This *miscarriage of justice* must not be allowed.” 

3/ “This causes many people to fall ill.”
4/ “This *problem* causes many people to fall ill.” 

5/ “This suggests that working at home can be advantageous.”
6/ “This *finding* suggests that working at home can be advantageous.”

Sentences 2, 4, and 6 are far clearer in meaning because ‘this’ is directly followed by the relevant noun phrase.

Further Information

The word ‘this’ is sometimes a pronoun and sometimes a determiner. 
For example, in the following sentence, ‘this’ is a pronoun: “This must not be allowed.” 
But in the upcoming sentence, ‘this’ is a determiner: “This ‘miscarriage of justice’ must not be allowed.” 
When we use ‘this’ as a pronoun, we are not explicitly saying what ‘this’ is referring to. As such, the reader has to work out what ‘this’ means, and we do not want the reader to have to ‘work things out.’ 
We do not want readers ‘working things out’ because 
a/ the reader might get it wrong! 
b/ we do not want readers using up their valuable cognitive resources.

As such, writers need to tell readers ‘what things are’ by making things very clear. 
Putting a noun after the word ‘this’ makes things clearer.



        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to

    def explain_counter(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Counter Arguments")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
       “COUNTER ARGUMENTS”

Any paper that seeks to persuade an audience needs to consider 1) the alternative positions that
other writers have on the topic, and 2) the problems, issues, and challenges that face the writer’s
position.
These aspects of a paper are generally referred to as ‘counter arguments.’

Counter arguments are a vital part of persuasive papers because they demonstrate the expertise,
objectivity, and honesty and the writer.
That is, all positions worthy of writing about have counter positions, problems, issues, and
challenges.
If writers do not sufficiently acknowledge and discuss these aspects then they weaken their own
arguments through a demonstration of poor research, ignorance, and close-mindedness.

Sections that discuss counter-arguments must be clearly signaled by the writer.
That is, writers often open these sections with language such as “Some critics argue …” or
“Some people disagree ….”.
Language such as this allows readers to process the forthcoming information as a counter
argument rather than as further support for the writer’s own positon.

Writers not only introduce counter-arguments, they also rebut, refute, or acknowledge the
counter-arguments.
Rebutting a counter-argument is an attempt to diminish its significance without actually claiming
the counter-argument is wrong.
Refuting a counter-argument is an attempt to show how the argument itself is flawed.

Writers can often address counter-arguments through the use the strategy called ‘synthesizing.’
In synthesizing, the writer seeks to find a compromise between the writer’s own position and that
of the counter-argument.

Writers can also address counter-arguments through the use the strategy called ‘weighing.’
In weighing, writers acknowledge the importance or merit of the counter-argument; however,
they show that their own side is of more importance.

On some occasions, there simply is no rebuttal or refutation to be made. That is, the counter-
argument is a real issue that simply has to be acknowledged.
All positions worthy of discussion have issues, so simply acknowledging a counter-argument is
not necessarily a weakness in the writer’s paper.

Examples of paragraph opening phrases for Counter Arguments

Critics argue …
Critics may argue …
Many people argue …
One problem with …
Opponents argue that …
Other people argue …
People argue that …
People may argue that …
Proponents of [counter-argument position] argue …
Some argue …
Some argue against …
Some critics argue …
Some may argue …
Some opponents …
Some people argue that …
Some people may argue that …
Some people say …
Some people say that …
On the other hand, …
Despite ... some argue …
Opponents of ... argue …

        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Us


    def explain_paraend(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Paragraph Endings")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
     The **Paragraph Ending Issue** refers to problems in how paragraphs are concluded—often 
     signaling weak cohesion, unclear argument closure, or missed opportunities for synthesis. 
     The algorithm flags final sentences that are poorly structured for endings, such as those starting 
     with outdated terms like *“hence,”* ending with citations or quotes, giving new examples 
     without elaboration, or overusing the same transition word (e.g., *“therefore”*). 
     It also flags texts with 10+ paragraphs that lack any strong concluding transitions, 
     encouraging clearer and more varied paragraph closures.



        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Us

    def explain_over_ex(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Overly Complex Sentence")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
    “OVERLY-COMPLEX SENTENCES”

A sentence is a single coherent thought expressed in words.
It is vital that sentences are coherent so that readers can process them easily.
Complex sentences are not easy to process, and they distract readers.

Sentences are commonly around 15 words long, and although they are often much longer, writers should carefully check whether a sentence is too long through being overly complex.

Words like ‘and,’ ‘but,’ ‘because,’ ‘that,’ and ‘which’ are frequently used within sentences to join ideas. These are good and useful words; however, writers need to be careful not to include too many within the same sentence. If there are too many, the sentence becomes difficult for readers to process.

Sometimes, sentences need to be split up into smaller units. 
Trying to keep most of the sentences a roughly similar length can ease processing for the reader.

Some examples of overly-complex Sentences are provided below. Note how ‘joining’ words have been overused.

1/ The football team Manchester United WHICH plays in the EPL in England spent 100s of millions of dollars on players WHICH they then had to spend millions more on for wages WHICH added up to more than half the club’s total budget.

2/ People are able to sing BECAUSE they use their right side of the brain, WHICH is not a problem BECAUSE THAT is not the area THAT is damaged.

3/ The Roman Empire was powerful because it had a lot of territory, AND it also had great architecture AND it was strong in terms of its economy, AND its army AND navy.


The sentences above can be broken down as in the following examples:


1/ The English football team Manchester United has spent 100s of millions of dollars on players. These players require wages, and wages cost the club millions more. When all these costs are added up, it accounts for more than half the club’s total budget.

2/ People can use the right side of their brain to help them sing. The right side is not damaged, meaning there is no problem for the patient.

3/ The Roman Empire was powerful for many reasons. These reasons include its vast territory, its great architecture, and its strong economy. In addition, the Roman Empire had the military might of its army and navy.






        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Us
    

    def explain_contraction(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Contractions")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
        “CONTRACTIONS”

Contractions are words such as ‘I’m,’ ‘she’ll,’ ‘don’t,’ and ‘mustn’t’ 

Contractions are often used in speaking and informal writing, but not in formal writing

Contractions within quoted works should not be changed





        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Us
    
    def explain_synthesis(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Synthesis Issue")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
      
            
    “SYNTHESIS”

    Most papers above 1000 words have multiple paragraphs demonstrating 'synthesis.' That is, some paragraphs derive their information from multiple sources, and it is this 'multiple sources' that show synthesis of information. Try to make sure you have at least three paragraphs that show synthesis. In your paper, Auto-Peer currently detects X such paragraphs. You may want to check that you have enough synthesis to meet your instructor’s requirements.





        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensure the dialog stays open until closed 

    def explain_choppy_sentence(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Choppy Sentences")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
       A choppy sentence sounds a lot like a topic sentence; however, it appears in the middle of a paragraph. The question then becomes, why would we have a topic sentence in the middle of a paragraph? 

Choppy sentences are short sentences. They also lack any obvious signs of cohesion or referencing.

If you have several examples of these choppy sentences then there is a good chance that at least one of them needs some reconsideration.

To repair choppy sentences, you can consider any of the following:

1/ Does the sentence need a transitional? (e.g., In addition, However, For example etc.) 
2/ Would the sentence sound better if it were joined to the previous sentence or the following sentence? 
3/ Does the sentence need further development? 
4/ Is the sentence actually a new topic and, therefore, should be the start of a new paragraph?
5/ Could the surrounding text be restructured to include the information in this sentence?

Note that some short sentences work perfectly well. You have to decide whether any flagged sentences need reconsidering or whether the sentence sounds perfectly fine as it is.

        




        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensure the dialog stays open until closed 
    
    def explain_fake_transitionals(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Fake Transitionals")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
        ‘Transitionals’ are strongly encouraged in writing.
        Transitionals are generally used at the start of a sentence to indicate the function of the sentence’s information.
        Common example of transitionals are ‘in addition, ‘for instance,’ and ‘more specifically.’

        Although transitionals are strongly encouraged, many words that are often used as transitionals can be problematic.
        Below is a list of these problematic words and the issue relating to their use.

        Hence:
        A somewhat old word
        In modern English, ‘hence’ can sometimes sound sarcastic
        Typically, ‘hence’ does not appear in papers, and certainly no more than once

        Moreover: 
        An often misunderstood word
        It is not a synonym for words such as 'in addition' or ‘furthermore’
        Instead, its meaning is 'more importantly' 
        Use ‘moreover’ very carefully
        Typically, ‘moreover’ does not appear in papers, and certainly no more than once

        Also:
        Not a good transitional for the start of a sentence, but very good in the middle of a sentence
        Use it in the right place

        For, And, Nor, But, Or, Yet, So: 
        These are connectives
        Use them to join sentences, not to start sentences

        On the contrary: 
        An often misunderstood word
        It is not a synonym for 'in contrast' or 'by contrast'
        Instead, its meaning is 'in fact, the exact opposite is true'
        Very unusual in writing
        Typically does not appear in a text at all

        Firstly, Secondly, Thirdly etc.: 
        Used in British English; however, in American English, use ‘First,’ ‘Second,’ ‘Third’ etc.

        To begin with, In summary, In sum, To summarize, In conclusion, To conclude: 
        Often used in High School, but very uncommon in advanced writing 
        Typically not needed because the header conveys whether or not the text is beginning or concluding
        Some can be used in ‘paragraph ending strategies’ but not paragraph beginnings

        Especially, Including, Thereby, Besides, Beyond, Compared to, Otherwise, Together with, Particularly, Coupled with:
        These words cannot be used at the start of a sentence if followed by a comma

        So then, By the way, In a nutshell: 
        Very 'chatty,' 'informal,' 'colloquial' 
        Do not use them



        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensure the dialog stays open until closed

    def explain_double_cohesion(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Pronoun cohesion")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
        “DOUBLED TRANSITIONALS”

        Transitionals are cohesive words that serve the function of forewarning readers as to the function of the sentence.
        Transitionals are words like ‘in addition,’ ‘by contrast,’ and ‘for example.’
        In general, transitionals are encouraged.

        In longer paragraphs, one problem that can occur is ‘doubled transitionals.’
        Doubling the transitional occurs when a writer repeats the same transitional within a paragraph.
        Having the same transitional twice in a paragraph can be distracting for readers.

        It is often possible to modify the wording of a paragraph to avoid having a doubled traditional; however, simply switching one transitional for a synonym is not recommended.
        That is, if the writer has twice used 'for example,' then do not simply change one of them to 'for instance.' 
        Similarly, if the writer has repeated 'in addition,' then do not simply change one of them to 'furthermore.' 

        If the writer has to use the same transitional twice in the same paragraph then there is probably a problem with the structure of the paragraph. That is, the paragraph possibly needs to be divided into at least two paragraphs.

        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
    
   

   
    
    def explain_thatwhich(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("That vs COMMA which issue")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
                
            “USING ‘THAT’ AND ‘COMMA-WHICH’”

            In speech, and even in most writing, the words ‘that’ and ‘which’ can often be used interchangeably. 
            However, in formal writing, there are occasions when ‘that’ and ‘comma-which’ must be distinguished.

            Use of ‘That’
            Restrictive Clause: Computers that provide wrong answers are useless.

            Use of ‘Comma-which’
            Non-Restrictive Clause: We spend so much time playing on computers, which is probably a big mistake.
            Parenthetical Clause: Computers, which are essential these days, provide a great many answers.

            Restrictive Clause: ‘That’
            A ‘restrictive clause’ (i.e., using ‘that’) contains information that is essential for the correct understanding of the sentence. As such, if we remove the clause, the meaning of the sentence changes. For example, consider the following sentence:

            “Computers that provide wrong answers are useless.”

            If the ‘that-clause,’ were to be removed, we would be left with “Computers … are useless.”
            As such, the meaning of the sentence would have changed.

            Below are some further examples where ‘that’ must be used. If we were to remove the ‘that-clause’ from these sentences, the meaning would change.

            1/ Assignments that receive grades must be printed off and handed to the instructor.
            2/ Clothing that is not culturally sensitive cannot be worn in this area.
            3/ The building that is causing the problem needs to be pulled down.

            Non-Restrictive Clause: ‘Comma Which’
            In a ‘non-restrictive clause,’ the word ‘which’ is used. ‘Which’ is always preceded by a comma, hence the name of ‘comma which.’ 

            When a sentence has a clause that can be left out without changing the meaning, we call it a non-restrictive clause. We can imagine a non-restrictive clause as simply being a part of the sentence for which you could use parentheses. For example, consider the sentence below:

            “Computers, which are essential these days, provide a great many answers.”

            If we take out the ‘which-clause,’ we are left with “Computers provide a great many answers.” Removing the clause in this case does not change the underlying meaning of the sentence.

            Below are some further examples where ‘which’ must be used. 

            1/ Assignments, which are common in all classes, must be printed off and handed to the instructor.
            2/ Clothing, which can vary greatly, should be respectful of the local culture.
            3/ The building, which has not been used for 20 years, needs to be pulled down.

            The Importance of the Distinction 
            Sometimes, a sentence can be possible with both ‘that’ and ‘comma-which’; however, the meaning changes depending on which one is used. Consider the examples below:

            A1/ The road that is flooded will be closed for the next few days.
            A2/ The road, which is flooded, will be closed for the next few days.

            B1/ The class that I teach will receive prizes.
            B2/ The class, which I teach, will receive prizes.

            Sentence A1 uses ‘that.’ The implication is that there is more than one road, but only the flooded road will be closed. For sentence A2, we do not know how many roads there are. We could take out ‘which is flooded’ without changing the meaning.

            Sentence B1 also uses ‘that.’ The implication is that there is more than one class, but only the class that I teach will receive prizes. For sentence B2, we do not know how many classes there are. We could take out ‘which I teach’ without changing the meaning.

            Further Considerations
            It is never right to use ‘that’ when ‘comma + which’ is required. As such, the following two sentences are wrong.

            1/ The TV, that my father gave me, is broken.
            2/ My alarm clock, that I meant to fix, didn’t go off this morning.

            There is another form of ‘which,’ that does not take a comma and it cannot be replaced by the word ‘that.’ Examples of this form of ‘which’ are provided below.

            1/ I don’t know which one I like best.
            2/ The letter tells us which person will be giving the interview.
            3/ We all told you which (answers/ones?) are right and which are wrong.

            In these cases, the word ‘which’ is forming an underlying question. As such, the above sentences really mean the following:

            1/ Which one do I like best? I don’t know!
            2/ Which person will be giving the interview? The letter tells us!
            3/ Which are right and which are wrong? We all told you!
        
        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content


    def explain_fake_freinds(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Fake Freinds")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
                “FAKE FRIENDS”

        A great many words are perfectly acceptable in speech but are frowned upon in formal writing.
        Other words can tend to sound a little too much like a high-school paper.
        These ‘fake friends’ should be avoided.

        Below is a list of these problematic words and the issue relating to their use. Some suggestions for alternative words are also provided.

        A lot:
        Typically does not appear in a formal text. Use words such as 'many' instead

        Believe: 
        A writer presenting an argument does so because of reasoned evidence, not simply ‘belief’
        When referring to research, choose words such as 'argue,' 'suggest,' 'highlight,' 'find,' 'discuss,' 'point out,' 'show,' or 'posit.'

        Different: 
        Student-writers very commonly misuse this word.
        In a sentence such as ‘There are many different uses for this system,’ we do not need to include the word ‘different.’ That is, the sentence reads better as ‘There are many uses for this system.’
        Similarly, student-writers often use ‘different’ when they mean ‘various’ or ‘many.’
        For example, rather than write ‘Scholars have provided different interpretations of this law,’ we can consider ‘Scholars have provided various interpretations of this law,’ or ‘Scholars have provided many interpretations of this law.’

        Different than: 
        Most people say ‘different than,’ but in formal writing, we usually prefer ‘different from.’

        Disprove: 
        See ‘prove’

        Done: 
        ‘Done’ is considered a dull word
        Typically, a word such as ‘conducted’ is preferred if referring to experiments

        Due to: 
        In modern English, 'due to' means 'caused by' or 'because of' 
        However, many instructors hold that 'due to' can only mean 'caused by' 
        In either case, 'due to' is an over-used phrase in student writing, and it can frustrate instructors 
        If you mean 'caused by' then just write 'caused by' 
        If you mean 'because of' then just write 'because of' 
        If 'due to' is preceded by 'am/is/are/was/were/been' then it is correct, but it is still a phrase that many instructors do not like

        Huge: 
        A much over-used word by student writers
        'Huge' is vague and overly dramatic 
        Best to avoid it
        Depending on context, words such as ‘significant,’ ‘important,’ and ‘essential’ are better choices

        Mentions: 
        If you are referring to another research paper then try to avoid words like ‘mentions,’ ‘says,’ ‘states,’ ‘talks about,’ or ‘showcases.’  
        Authors 'write,' they do not 'talk about' and they do not 'say.' 
        ''Words like 'states,' ‘mentions,’ and ‘showcases’ are often a problem because they become overused. 
        Instead, use words such as 'writes,' 'argues,' ‘claims,’ 'suggests,' 'finds,' 'highlights,' 'discusses,' 'point outs,' 'shows,' or 'posits.'
        The above suggests words are very similar in meaning, but that does not mean they are ‘the same’ in meaning. Be sure to check carefully which of the verbs is most appropriate for the context of your paper.
        Note that Auto-Peer looks for examples of “mentions that,” “states that,” etc. As such, you may have other examples in your paper without the word ‘that.’ You are advised to also modify those words where appropriate.

        Opinion: 
        Avoid expressions like ‘in my opinion.’ Writers need to present evidence and make arguments. If the writer has evidence then it is not merely an ‘opinion.’

        Prove:
        'Researchers' collect evidence, and 'evidence' tends to 'suggest,' not 'prove.' 
        In an argument paper, your task is not to 'prove' but to 'persuade.' 
        Better to not use this word
        Note that ‘prove’ is acceptable when used in expressions such as ‘This solution has proven to be a great success.’

        Says:
        See ‘mentions’

        Several: 
        An often misunderstood word for student writers
        'Several' means 'about seven' 
        It means 'more than a few' but ‘less than many'

        Showcases:
        See ‘mentions’

        States:
        See ‘mentions’

        Talks about:
        See ‘mentions’

        Think:
        Avoid phrases like ‘I think …’
        The word ‘think’ implies an opinion. Writers ‘argue’ or ‘discuss’ (not just ‘think’) because they have evidence. 

        Utilize: 
        ‘Utilize’ is a much over-used word 
        Most of the time, 'use' is a better choice of words
        We use 'utilize' when we are using something in an unexpected or highly original way. For example, you might 'utilize' discarded plastic bottles to make a boat

        Very:
        Probably an over-used word
        Not everything needs to be “very,” and there are many other words available if necessary

        You: 
        This word is not used in formal writing 
        Typically, use 'we' instead




        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensure the dialog stays open until closed


    def explain_missing_ref(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Missing References")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
                “MISSING REFERENCES”

        A research paper acquires most of its information from the published work of other people.
        That is, a research paper is not an opinion paper, so plenty of references to the opinions and findings of other people are needed.
        While it is not impossible to have paragraphs without any references (especially in the conclusion section), it is wise to check if some claims are in need of references.
        Note that in a draft paper, the writer may not yet have identified the references to be used. If this is the case, many writers will simply enter something like (REF) in the text. By using (REF), the instructor will know that the writer is going to enter a reference at that point as soon as the right reference is located.


        
        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
    def explain_may_issue(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("The unclear `This` Issue")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
        “MAY VS MIGHT HAVE” 

        In everyday speech, it generally doesn’t matter whether we use “might” or “may.” However, in formal writing, many experienced instructors insist on “may” for the present or the future and “might have” for the past. 


        For example, we would generally write “The plan may solve this most serious of issues.”
        However, for the past, we write “The plan might have solved this most serious of issues.”
        Accordingly, we cannot write “The plan might solve this most serious of issues.”


        A great many instructors won’t mind whether you write “may” or “might.” However, no professor will object to you making the distinction clear.


        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensure the dialog stays open until closed

    def explain_num_issue(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("The number issue")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
        
                “NUMBERS ISSUES”

        Numbering is a writing style issue.
        For the numbers 1, 2, 3 …. 9, we are required to write out the full word.
        As such, write one, two, three … nine.
        For numbers greater than nine, we use the figures (e.g., 10, 11, 12 etc.)
        Also note that we keep words together with words, while we keep figures together with figures.
        As such, we write 30%, $100 etc.
        But we would write five percent, two dollars etc.


        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensure the dialog stays open until closed


    def explain_sentence_length(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Sentence length")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
        A sentence is a single coherent thought expressed in words. 

        Sentences are commonly around 15 words long, and although they are often considerably longer, writers should carefully check whether a sentence is too long or too short. 
        When sentences are too long, they are difficult for readers to process. 
        When sentences are too short, they sound ‘choppy’ and seem like the writer is introducing a new topic. 

        Words like ‘and,’ ‘but,’ ‘because,’ ‘that,’ and ‘which’ are frequently used within sentences to join ideas. These are good and useful words; however, writers need to be careful not to include too many of these words within the same sentence. If there are too many, the sentence becomes difficult for readers to process

        Sometimes, sentences need to be split up into smaller units and/or joined with other sentences. Trying to keep most of the sentences roughly a similar length can ease processing for the reader.
        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensure the dialog stays open until closed

    def explain_symbol(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Symbol Issue")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
                “SYMBOLS”

        Semi-Colons:
        This piece of punctuation is frequently used incorrectly. 
        In virtually every single instance, a full stop is a better choice than a semi-colon 

        If following the APA style guide, and you have more than one reference, and those references are within parentheses, then separate the references with a semi-colon; e.g., (Abram et al.,; Giles, 1997; Updike & Smith, 2013).

        You can also use a semi-colon before some transitionals (e.g., 'however.’) You should then also put a comma after the transitional. However, although you can use a semi-colon for ‘however,’ a full stop is still the best option. 
        The basic rule is to simply avoid semi-colons 

        Colons:
        There are a number of times when you can use a colon, but you never actually have to use one. 
        You can use a colon before a list of three or more items. But, even then, your preceding sentence must be complete!
        As a ‘bad’ example > “I want to go to: Paris, Berlin, and London.” 
        As a ‘correct’ example > “I want to go to the following places: Paris, Berlin, and London.” 
        As the ‘best example’ > “I want to go to Paris, Berlin, and London.” 

        Ampersand (&):
        Use only for in-text citations and for references in the ‘reference section’ of the paper. 

        Percent Sign (%): 
        Use only for figures of 10 or greater. For example, '15%' but ' five percent.' 
        Do not put a space before the % symbol. 
        Use % after the figure, never before. 

        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensu

    def explain_topic_sentence(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Topic Sentences")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """  A paragraph is more easily processed when its first sentence is a ‘topic sentence,’ also known as a ‘topic opener.’
        A topic sentence introduces the focal point of the paragraph.
        Topic sentences are usually quite short, relative to other sentences, because they merely introduce; they do not explain or elaborate on ideas.
        As such, first sentences can sometimes be problematic if they include words like ‘which,’ or ‘because.’

        Some paragraphs feature a ‘clarification sentence’ as the second sentence of the paragraph. These sentences often begin with transitionals such as ‘For example,’ ‘That is,’ or ‘More specifically.’
        These clarification sentences are a more detailed version of the ‘topic sentence.’
        Because clarification sentences are more detailed, they are usually longer than topic sentences.

        If the clarification sentence (or second sentence) is actually shorter than the topic sentence (or first sentence) then there is a chance the writer has over-explained the topic sentence and under-explained the clarification sentence.
        Such an issue is referred to as a 'Shorter/Longer Violation.'  
        That is, most good topic openers feature a first sentence that is shorter than the second sentence.  
        If the first sentence is substantially longer than the second sentence, then there may be a problem.

        There is one very important exception to this advice: ‘Bridging topic sentences.’
        ‘Bridging topic sentences’ link the previous paragraph to the current paragraph.
        This form of topic sentences begins with a clause that essentially summarizes the topic of the previous paragraph.
        For example, consider the sentences below, each of which begin with a bridge.

        1/ Although there are many advantages to adopting the RAFP plan, we also need to consider the challenges that such a plan faces.
        2/ Despite the many advantages of adopting the RAFP plan, we also need to consider the challenges that such a plan faces. 
        3/ While there are many advantages to adopting the RAFP plan, we also need to consider the challenges that such a plan faces.
        4/ By contrast to the many successes of RAFP implementation, we also need to acknowledge that some and issues have occurred.
        5/ In addition to the financial challenges of an RAFP implementation, we also need to acknowledge that some environmental concerns have been raised.

        If your first sentence is a bridge (like those in the examples above), then you may have a perfectly acceptable long first sentence. This said, still consider whether your second sentence needs some modification by following the guidance below.

        Writers can usually correct shorter/longer violations by considering the first three sentences together. Consider the example below:

        1. More than 1.6 billion people in the world are either overweight or obese, and the United States has the highest rate of obesity.

        2. America's number one killer is cardiovascular diseases.

        3. This problem can easily be prevented by exercising because exercise not only reduces the risk of health problems and various diseases, but it also has an effect on overall appearance.

        Number of words in Sentence 1 = 23
        Number of words in Sentence 2 = 7
        Number of words in Sentence 3 = 30

        The above example – and most examples - can be changed in three different ways.

        1/ Ask yourself, does the second sentence actually serve as a better topic sentence?  In this example, we would have …

        Sentence 1: America's number one killer is cardiovascular diseases.

        Sentence 2: More than 1.6 billion people in the world are either overweight or obese and the United States has the highest rate of obesity.

        Sentence 3: This problem can easily be prevented by exercising because exercise not only reduces the risk of health problems and various diseases, but it also has an effect on overall appearance.


        2/ Ask yourself, can part of the first sentence connect with the second sentence?  In this example, we could have …

        Sentence 1: More than 1.6 billion people in the world are either overweight or obese.

        Sentence 2: Indeed, the United States has the highest rate of obesity and America's number one killer is cardiovascular diseases.

        Sentence 3: This problem can easily be prevented by exercising because exercise not only reduces the risk of health problems and various diseases, but it also has an effect on overall appearance.


        3/ Ask yourself, can part of the second sentence connect with the third sentence?  In this example, we could have …

        Sentence 1: More than 1.6 billion people in the world are either overweight or obese and the United States has the highest rate of obesity.

        Sentence 2: America's number one killer is cardiovascular diseases, and this problem can easily be prevented by exercising because exercise not only reduces the risk of health problems and various diseases, but it also has an effect on overall appearance.


        



        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensure the dialog stays open until closed
    
    def explain_problematic_ref(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Problematic Referencing Issue")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
            “PROBLEMATIC REFERENCE POSITIONING”

        If a paragraph has only one reference and that one reference occurs at the very end of the paragraph then it could be an indication of a problem.

        Specifically, why would a paragraph have a single reference occurring right at the very end? It often occurs because a student writer has just made a bunch of claims and now wants to attribute all those claims to a single source. However, if all the previous claims really are attributable to this one source then the source seems to be very important. As such, the source should be introduced early within the text, not hidden away in parentheses at the end.

        More likely, the claims of the paragraph probably require multiple sources, but the student-writer is simply trying to hide the fact that appropriate extra sources have not been found.

        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensu
    

    def explain_may_issue(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("The unclear `This` Issue")
        dialog.setWindowModality(qtc.Qt.NonModal)
        dialog_layout = qtw.QVBoxLayout()

        paragraph_text = """
        “MAY VS MIGHT HAVE” 

        In everyday speech, it generally doesn’t matter whether we use “might” or “may.” However, in formal writing, many experienced instructors insist on “may” for the present or the future and “might have” for the past. 


        For example, we would generally write “The plan may solve this most serious of issues.”
        However, for the past, we write “The plan might have solved this most serious of issues.”
        Accordingly, we cannot write “The plan might solve this most serious of issues.”


        A great many instructors won’t mind whether you write “may” or “might.” However, no professor will object to you making the distinction clear.


        """

        welcome_label = qtw.QLabel(paragraph_text, dialog)
        welcome_label.setFont(qtg.QFont('Times New Roman', 12))
        welcome_label.setWordWrap(True)  # Enable word wrap to ensure the text fits within the dialog

        scroll_area = qtw.QScrollArea()
        scroll_area.setWidget(welcome_label)
        scroll_area.setWidgetResizable(True)

        dialog_layout.addWidget(scroll_area)

        close_button = qtw.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)  # Adjust dialog size to better fit the content
        dialog.exec_()  # Use exec_() to ensure the dialog stays open until closed
    

    def open_result_window_single(self, count=0):
        if self.result_window is None:
            self.result_window = ResultWindow()

        input_text = self.input_box.toPlainText()  # Get text from input box

        progress = qtw.QProgressDialog("Analyzing text...", "Cancel", 0, 23, self)
        progress.setWindowTitle("Please wait")
        progress.setWindowModality(qtc.Qt.WindowModal)
        progress.setMinimumDuration(0)  # show immediately

        # Analyze the text
        #check
        #Add result 3 etc make a same consistent dictionary

        # analysis_result1= self.text_analyzer1.analyze_text(input_text)
        # print(analysis_result1)
        # analysis_result2=self.text_analyzer2.analyze_text(input_text)
        # print(analysis_result2)
        # analysis_result3=self.text_analyzer3.analyze_text(input_text)
        # print(analysis_result3)
        # analysis_result4=self.text_analyzer4.analyze_text(input_text)
        # print(analysis_result4)
        # analysis_result5=self.text_analyzer5.analyze_text(input_text)
        # print(analysis_result5)
        # analysis_result={"issues_found_counter" : analysis_result1.get("issues_found_counter", 0)+analysis_result2.get("issues_found_counter", 0)+analysis_result3.get("flagged_sentence_count",0)+analysis_result4.get("issues_found_counter", 0)+analysis_result5.get("issues_found_counter", 0),
        # "issues_para":"The following lines/paras might be causing issues\n"+analysis_result1.get("issues_para", 0)+analysis_result2.get("issues_para", 0)+analysis_result3.get("flagged_sentences",0)+"\n"+ analysis_result4.get("flagged_text", 0) +analysis_result5.get("issues_para", 0)}
       
       
        analysis_result1 = self.text_analyzer1.analyze_text(input_text)
        print(analysis_result1)
        progress.setValue(1)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        analysis_result2 = self.text_analyzer2.analyze_text(input_text)
        progress.setValue(2)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result2)
        analysis_result3 = self.text_analyzer3.analyze_text(input_text)
        progress.setValue(3)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result3)
        analysis_result4 = self.text_analyzer4.analyze_text(input_text)
        progress.setValue(4)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result4)
        analysis_result5 = self.text_analyzer5.analyze_text(input_text)
        progress.setValue(5)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result5)
        analysis_result6 = self.text_analyzer6.analyze_text(input_text)
        progress.setValue(6)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result6)
        analysis_result7 = self.text_analyzer7.analyze_text(input_text)
        progress.setValue(7)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result7)
        analysis_result8 = self.text_analyzer8.analyze_text(input_text)
        progress.setValue(8)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result8)
        analysis_result9=self.text_analyzer9.analyze_text(input_text)
        progress.setValue(9)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result9)
        analysis_result10=self.text_analyzer10.analyze_text(input_text)
        progress.setValue(10)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result10)
        analysis_result11=self.text_analyzer11.analyze_text(input_text)
        progress.setValue(11)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result11)
        analysis_result12=self.text_analyzer12.analyze_text(input_text)
        progress.setValue(12)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result12)
        analysis_result13=self.text_analyzer13.analyze_text(input_text)
        progress.setValue(13)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result13)
        analysis_result14=self.text_analyzer14.analyze_text(input_text)
        progress.setValue(14)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result14)
        analysis_result15=self.text_analyzer15.analyze_text(input_text)
        progress.setValue(15)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result15)
        analysis_result16=self.text_analyzer16.analyze_text(input_text)
        progress.setValue(16)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result16)
        analysis_result17=self.text_analyzer17.analyze_text(input_text)
        progress.setValue(17)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result17)
        analysis_result18=self.text_analyzer18.analyze_text(input_text)
        progress.setValue(18)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result18)
        analysis_result19=self.text_analyzer19.analyze_text(input_text)
        progress.setValue(19)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result19)
        analysis_result20=self.text_analyzer20.analyze_text(input_text)
        progress.setValue(20)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result20)
        analysis_result21=self.text_analyzer21.analyze_text(input_text)
        progress.setValue(21)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result21)
        analysis_result22=self.text_analyzer22.analyze_text(input_text)
        progress.setValue(22)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result22)
        analysis_result23=self.text_analyzer23.analyze_text(input_text)
        progress.setValue(23)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result23)





        progress.setValue(23)

        numbered_issues = []
        counter = 1

        # Add numbered results if they are not null
        if analysis_result1.get("issues_para") and analysis_result1.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result1['issues_para']}\n")
            counter += 1
        if analysis_result2.get("issues_para") and analysis_result2.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result2['issues_para']}\n")
            counter += 1
        if analysis_result3.get("flagged_sentences") and analysis_result3.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result3['flagged_sentences']}\n")
            counter += 1
        if analysis_result4.get("flagged_text") and analysis_result4.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result4['flagged_text']}\n")
            counter += 1
        if analysis_result5.get("issues_para") and analysis_result5.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result5['issues_para']}\n")
            counter += 1
        if analysis_result6.get("issues_para") and analysis_result6.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result6['issues_para']}\n")
            counter += 1
        if analysis_result7.get("issues_para") and analysis_result7.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result7['issues_para']}\n")
            counter += 1
        if analysis_result8.get("issues_para") and analysis_result8.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result8['issues_para']}\n")
            counter += 1
        if analysis_result9.get("issues_para") and analysis_result9.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result9['issues_para']}\n")
            counter += 1
        if analysis_result10.get("issues_para") and analysis_result10.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result10['issues_para']}\n")
            counter += 1
        if analysis_result11.get("issues_para") and analysis_result11.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result11['issues_para']}\n")
            counter +=1 
        if analysis_result12.get("issues_para") and analysis_result12.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result12['issues_para']}\n")
            counter +=1 
        if analysis_result13.get("issues_para") and analysis_result13.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result13['issues_para']}\n")
            counter +=1 
        if analysis_result14.get("issues_para") and analysis_result14.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result14['issues_para']}\n")
            counter +=1 
        if analysis_result15.get("issues_para") and analysis_result15.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result15['issues_para']}\n")
            counter +=1
        if analysis_result16.get("issues_para") and analysis_result16.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result16['issues_para']}\n")
            counter +=1
        if analysis_result17.get("issues_para") and analysis_result17.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result17['issues_para']}\n")
            counter +=1
        if analysis_result18.get("issues_para") and analysis_result18.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result18['issues_para']}\n")
            counter +=1
        if analysis_result19.get("issues_para") and analysis_result19.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result19['issues_para']}\n")
            counter +=1
        if analysis_result20.get("issues_para") and analysis_result20.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result20['issues_para']}\n")
            counter +=1
        if analysis_result21.get("issues_para") and analysis_result21.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result21['issues_para']}\n")
            counter +=1
        if analysis_result22.get("issues_para") and analysis_result22.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result22['issues_para']}\n")
            counter +=1
        if analysis_result23.get("issues_para") and analysis_result23.get("issues_found_counter")>0:
            numbered_issues.append(f"#{counter} {analysis_result23['issues_para']}\n")
            counter +=1
       
       
       


        # Combine the numbered issues into a single string
        final_issues_para = "The following lines/paras might be causing issues:\n" + "\n".join(numbered_issues)

        # Summing the issues found
        total_issues_found = (
            analysis_result1.get("issues_found_counter", 0) +
            analysis_result2.get("issues_found_counter", 0) +
            analysis_result3.get("flagged_sentence_count", 0) +
            analysis_result4.get("issues_found_counter", 0) +
            analysis_result5.get("issues_found_counter", 0) +analysis_result6.get("issues_found_counter", 0)+analysis_result7.get("issues_found_counter", 0)+
            analysis_result8.get("issues_found_counter", 0) + analysis_result9.get("issues_found_counter", 0)+analysis_result10.get("issues_found_counter", 0)+ analysis_result11.get("issues_found_counter", 0)+analysis_result12.get("issues_found_counter" ,0)
        +analysis_result13.get("issues_found_counter", 0)+analysis_result14.get("issues_found_counter", 0 )+analysis_result15.get("issues_found_counter", 0)+ analysis_result16.get("issues_found_counter", 0)
        +analysis_result17.get("issues_found_counter", 0) + analysis_result18.get("issues_found_counter", 0)
        +analysis_result19.get("issues_found_counter", 0) + analysis_result20.get("issues_found_counter", 0) + analysis_result21.get("issues_found_counter", 0) + analysis_result22.get("issues_found_counter", 0) +analysis_result23.get("issues_found_counter", 0))

        #total_issues_found1= analysis_result5.get("issues_found_counter", 0) #para length 

        # Create the final result dictionary
        print(count)
        if count==0:
            analysis_result = {
                "issues_found_counter": total_issues_found,
                "issues_para": final_issues_para
            }
        elif count==1: #para length
            analysis_result = {
                # "issues_found_counter": total_issues_found1,
                "issues_para": analysis_result1.get("issues_para")
            }
        elif count==2:
            analysis_result = {
                # "issues_found_counter": analysis_result3.get("flagged_sentence_count", 0),
                "issues_para": analysis_result3.get("flagged_sentences")
            }
        elif count==3:
            analysis_result = {
                # "issues_found_counter": analysis_result2.get("issues_found_counter", 0),
                "issues_para": analysis_result2.get("issues_para")
            }
        elif count==4:
            analysis_result = {
                # "issues_found_counter": analysis_result4.get("issues_found_counter", 0),
                "issues_para": analysis_result4.get("flagged_text")
            }
        elif count==5:
            analysis_result = {
                # "issues_found_counter": analysis_result1.get("issues_found_counter", 0),
                "issues_para": analysis_result5.get("issues_para")
            }
        elif count==6: #may vs might
            analysis_result = {
                # "issues_found_counter": analysis_result6.get("issues_found_counter", 0),
                "issues_para": analysis_result6.get("issues_para")
            }
        elif count==7: #doubled 
            analysis_result = {
                # "issues_found_counter": analysis_result7.get("issues_found_counter", 0),
                "issues_para": analysis_result7.get("issues_para")
            }
        elif count==8: #lonely
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result8.get("issues_para")
            }
        elif count==9:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result9.get("issues_para")
            }
        elif count==10:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result10.get("issues_para")
            }
        elif count==11:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result11.get("issues_para")
            }
        elif count==12:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result12.get("issues_para")
            }
        elif count==13:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result13.get("issues_para")
            }

        elif count==14:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result14.get("issues_para")
            }
        
        elif count==15:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result15.get("issues_para")
            }
        elif count==16:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result16.get("issues_para")
            }
        elif count==17:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result17.get("issues_para")
            }
        elif count==18:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result18.get("issues_para")
            }
        elif count==19:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result19.get("issues_para")
            }
        elif count==20:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result20.get("issues_para")
            }
        elif count==21:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result21.get("issues_para")
            }
        elif count==22:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result22.get("issues_para")
            }
        elif count==23:#topic sentences
            analysis_result = {
                # "issues_found_counter": analysis_result8.get("issues_found_counter", 0),
                "issues_para": analysis_result23.get("issues_para")
            }
        elif count==100:#for no of issues
            analysis_result ={
                "issues_para":"Total Issues Found: "+ str(total_issues_found)+"\n Check Analysis for detailed Issues!"
            }









            


        # Update the result window with the analysis result
        self.result_window.update_result(analysis_result)

        # # Update the result window with the analysis result
        # self.result_window.update_result(analysis_result)
        
        
        self.result_window.show()
    
    def open_result_window(self, count=0):
        if self.result_window is None:
            self.result_window = ResultWindow()


        input_text = self.input_box.toPlainText()  # Get text from input box
        # --- Progress Dialog ---
        progress = qtw.QProgressDialog("Analyzing text...", "Cancel", 0, 23, self)
        progress.setWindowTitle("Please wait")
        progress.setWindowModality(qtc.Qt.WindowModal)
        progress.setMinimumDuration(0)  # show immediately

        analysis_result1 = self.text_analyzer1.analyze_text(input_text)
        print(analysis_result1)
        progress.setValue(1)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        analysis_result2 = self.text_analyzer2.analyze_text(input_text)
        progress.setValue(2)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result2)
        analysis_result3 = self.text_analyzer3.analyze_text(input_text)
        progress.setValue(3)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result3)
        analysis_result4 = self.text_analyzer4.analyze_text(input_text)
        progress.setValue(4)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result4)
        analysis_result5 = self.text_analyzer5.analyze_text(input_text)
        progress.setValue(5)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result5)
        analysis_result6 = self.text_analyzer6.analyze_text(input_text)
        progress.setValue(6)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result6)
        analysis_result7 = self.text_analyzer7.analyze_text(input_text)
        progress.setValue(7)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result7)
        analysis_result8 = self.text_analyzer8.analyze_text(input_text)
        progress.setValue(8)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result8)
        analysis_result9=self.text_analyzer9.analyze_text(input_text)
        progress.setValue(9)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result9)
        analysis_result10=self.text_analyzer10.analyze_text(input_text)
        progress.setValue(10)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result10)
        analysis_result11=self.text_analyzer11.analyze_text(input_text)
        progress.setValue(11)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result11)
        analysis_result12=self.text_analyzer12.analyze_text(input_text)
        progress.setValue(12)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result12)
        analysis_result13=self.text_analyzer13.analyze_text(input_text)
        progress.setValue(13)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result13)
        analysis_result14=self.text_analyzer14.analyze_text(input_text)
        progress.setValue(14)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result14)
        analysis_result15=self.text_analyzer15.analyze_text(input_text)
        progress.setValue(15)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result15)
        analysis_result16=self.text_analyzer16.analyze_text(input_text)
        progress.setValue(16)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result16)
        analysis_result17=self.text_analyzer17.analyze_text(input_text)
        progress.setValue(17)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result17)
        analysis_result18=self.text_analyzer18.analyze_text(input_text)
        progress.setValue(18)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result18)
        analysis_result19=self.text_analyzer19.analyze_text(input_text)
        progress.setValue(19)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result19)
        analysis_result20=self.text_analyzer20.analyze_text(input_text)
        progress.setValue(20)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result20)
        analysis_result21=self.text_analyzer21.analyze_text(input_text)
        progress.setValue(21)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result21)
        analysis_result22=self.text_analyzer22.analyze_text(input_text)
        progress.setValue(22)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result22)
        analysis_result23=self.text_analyzer23.analyze_text(input_text)
        progress.setValue(23)  # X = analyzer number
        qtc.QCoreApplication.processEvents()
        print(analysis_result23)

        issues = []

        if analysis_result1.get("issues_para") and analysis_result1.get("issues_found_counter")>0:
            issues.append(analysis_result1["issues_para"])
        if analysis_result2.get("issues_para") and analysis_result2.get("issues_found_counter")>0:
            issues.append(analysis_result2["issues_para"])
        if analysis_result3.get("flagged_sentences") and analysis_result3.get("issues_found_counter")>0:
            issues.append(analysis_result3["flagged_sentences"])
        if analysis_result4.get("flagged_text") and analysis_result4.get("issues_found_counter")>0:
            issues.append(analysis_result4["flagged_text"])
        if analysis_result5.get("issues_para") and analysis_result5.get("issues_found_counter")>0:
            issues.append(analysis_result5["issues_para"])
        if analysis_result6.get("issues_para") and analysis_result6.get("issues_found_counter")>0:
            #print("yes its true")
            issues.append(analysis_result6["issues_para"])
            print(issues)
        if analysis_result7.get("issues_para") and analysis_result7.get("issues_found_counter")>0:
            print("yes its true")
            issues.append(analysis_result7["issues_para"])
            print(issues)
        if analysis_result8.get("issues_para") and analysis_result8.get("issues_found_counter")>0:
            print("yes its true")
            issues.append(analysis_result8["issues_para"])
            print(issues)
        if analysis_result9.get("issues_para") and analysis_result9.get("issues_found_counter")>0:
            print("yes its true")
            issues.append(analysis_result9["issues_para"])
            print(issues)
        if analysis_result10.get("issues_para") and analysis_result10.get("issues_found_counter")>0:
            print("yes its true")
            issues.append(analysis_result10["issues_para"])
            print(issues)
        if analysis_result11.get("issues_para") and analysis_result11.get("issues_found_counter")>0:
            print("yes its true")
            issues.append(analysis_result11["issues_para"])
            print(issues)
        if analysis_result12.get("issues_para") and analysis_result12.get("issues_found_counter")>0:
            print("yes its true")
            issues.append(analysis_result12["issues_para"])
            print(issues)
        if analysis_result13.get("issues_para") and analysis_result13.get("issues_found_counter")>0:
           # print("yes its true")
            issues.append(analysis_result13["issues_para"])
            print(issues)
        if analysis_result14.get("issues_para") and analysis_result14.get("issues_found_counter")>0:
           # print("yes its true")
            issues.append(analysis_result14["issues_para"])
            print(issues)
        if analysis_result15.get("issues_para") and analysis_result15.get("issues_found_counter")>0:
           # print("yes its true")
            issues.append(analysis_result15["issues_para"])
            print(issues)
        if analysis_result16.get("issues_para") and analysis_result16.get("issues_found_counter")>0:
           # print("yes its true")
            issues.append(analysis_result16["issues_para"])
            print(issues)
        if analysis_result17.get("issues_para") and analysis_result17.get("issues_found_counter")>0:
           # print("yes its true")
            issues.append(analysis_result17["issues_para"])
            print(issues)
        if analysis_result18.get("issues_para") and analysis_result18.get("issues_found_counter")>0:
           # print("yes its true")
            issues.append(analysis_result18["issues_para"])
            print(issues)
        if analysis_result19.get("issues_para") and analysis_result19.get("issues_found_counter")>0:
           # print("yes its true")
            issues.append(analysis_result19["issues_para"])
            print(issues)
        if analysis_result20.get("issues_para") and analysis_result20.get("issues_found_counter")>0:
           # print("yes its true")
            issues.append(analysis_result20["issues_para"])
            print(issues)
        if analysis_result21.get("issues_para") and analysis_result21.get("issues_found_counter")>0:
           # print("yes its true")
            issues.append(analysis_result21["issues_para"])
            print(issues)
        if analysis_result22.get("issues_para") and analysis_result22.get("issues_found_counter")>0:
           # print("yes its true")
            issues.append(analysis_result22["issues_para"])
            print(issues)
        if analysis_result23.get("issues_para") and analysis_result23.get("issues_found_counter")>0:
           # print("yes its true")
            issues.append(analysis_result23["issues_para"])
            print(issues)

        if issues:
            print("npthing")
        else:
            issues.append("No Issues Found!")
         # break into pages
        issues_list = []
        for issue in issues:
            if isinstance(issue, str):
                issues_list.append(issue)
        #window = IssueNavigatorWindow(issues=issues_list)
        
        self.issue_navigator_window = IssueNavigatorWindow(issues=issues_list)
        self.issue_navigator_window.show()


            # # Update the result window with the analysis result
            # self.result_window.update_result(analysis_result)
            
            
            # self.result_window.show()

class ResultWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Results")
        self.setGeometry(100, 100, 800, 600)  # Adjust window size

        self.layout = qtw.QVBoxLayout(self)

        # Add a centered label for Analysis Results
        self.result_label = qtw.QLabel("<h4>Analysis Results</h4>", self)
        self.result_label.setFont(qtg.QFont('Times New Roman', 12))
        self.result_label.setAlignment(qtc.Qt.AlignCenter)  # Center the text
        self.layout.addWidget(self.result_label)

        # Add a QTextEdit box to display and edit the analysis result
        self.result_box = qtw.QTextEdit(self)
        self.result_box.setFont(qtg.QFont('Times New Roman', 12))  # Increase font size
        self.result_box.setStyleSheet("""
            background-color: lightyellow; 
            border: 2px solid darkblue; 
            border-radius: 10px;
            padding: 10px;
        """)  # Set yellow background color, blue border, and padding
        self.result_box.setAlignment(qtc.Qt.AlignLeft)  # Left-align the text
        self.result_box.setReadOnly(False)  # Make the box editable
        self.layout.addWidget(self.result_box)

        # Stretch factors to make the result_box take more space
        self.layout.setStretch(0, 1)  # Reduce space taken by the result_label
        self.layout.setStretch(1, 4)  # Increase space taken by the result_box

        self.setLayout(self.layout)

    def update_result(self, result):
        # Handle the dictionary returned from analyze_text
        #issues_found_counter = result.get("issues_found_counter", 0)
        issues_para = result.get("issues_para", "")
            
        # Format the result for display
        display_text = f"\n{issues_para}"
            
        # Update the result_box with the formatted result
        self.result_box.setHtml(display_text)





class IssueNavigatorWindow(qtw.QMainWindow):
    def __init__(self, issues=None):
        super().__init__()
        self.setWindowTitle("Issue Navigator")
        self.setGeometry(100, 100, 800, 600)  # Adjust window size

        self.central_widget = qtw.QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.layout = qtw.QVBoxLayout(self.central_widget)

        # Add a centered label for Issue Navigator
        self.title_label = qtw.QLabel("<h4>Issue Navigator</h4>", self)
        self.title_label.setFont(qtg.QFont('Times New Roman', 12))
        self.title_label.setAlignment(qtc.Qt.AlignCenter)  # Center the text
        self.layout.addWidget(self.title_label)

        # Add a QTextEdit box to display the issue
        self.issue_box = qtw.QTextEdit(self)
        self.issue_box.setFont(qtg.QFont('Times New Roman', 12))  # Increase font size
        self.issue_box.setStyleSheet("""
            background-color: lightyellow; 
            border: 2px solid darkblue; 
            border-radius: 10px;
            padding: 10px;
        """)  # Set light yellow background color, dark blue border, and padding
        self.issue_box.setAlignment(qtc.Qt.AlignLeft)  # Left-align the text
        self.issue_box.setReadOnly(True)  # Make the box read-only
        self.layout.addWidget(self.issue_box)

        # Navigation buttons
        self.button_layout = qtw.QHBoxLayout()

        self.prev_button = qtw.QPushButton("Previous", self)
        self.prev_button.setFont(qtg.QFont('Times New Roman', 12))
        self.prev_button.setStyleSheet("""
            background-color: lightblue; 
            border: 1px solid darkblue; 
            border-radius: 5px;
            padding: 5px;
        """)  # Set light blue background color, dark blue border, and padding
        self.prev_button.clicked.connect(self.show_previous_issue)
        self.button_layout.addWidget(self.prev_button)

        self.next_button = qtw.QPushButton("Next", self)
        self.next_button.setFont(qtg.QFont('Times New Roman', 12))
        self.next_button.setStyleSheet("""
            background-color: lightblue; 
            border: 1px solid darkblue; 
            border-radius: 5px;
            padding: 5px;
        """)  # Set light blue background color, dark blue border, and padding
        self.next_button.clicked.connect(self.show_next_issue)
        self.button_layout.addWidget(self.next_button)

        self.layout.addLayout(self.button_layout)

        self.current_issue_index = 0
        self.issues_list = issues if issues else []

        # Initialize the display with the provided issues
        self.update_display()

    def update_issues(self, issues):
        self.issues_list = issues
        self.current_issue_index = 0 if issues else -1
        self.update_display()

    def update_display(self):
        if self.current_issue_index >= 0 and self.current_issue_index < len(self.issues_list):
            self.issue_box.setHtml(self.issues_list[self.current_issue_index])
        else:
            self.issue_box.clear()

        # Update button states
        self.prev_button.setEnabled(self.current_issue_index > 0)
        self.next_button.setEnabled(self.current_issue_index < len(self.issues_list) - 1)

    def show_previous_issue(self):
        if self.current_issue_index > 0:
            self.current_issue_index -= 1
            self.update_display()

    def show_next_issue(self):
        if self.current_issue_index < len(self.issues_list) - 1:
            self.current_issue_index += 1
            self.update_display()


# Assume `numbered_issues` has been generated from your analysis as shown earlier
# issue_navigator_window = IssueNavigatorWindow()
# issue_navigator_window.show()


#FOR SENTENCE STARTER ::
      

#     def open_result_window(self):
#         if self.result_window is None:
#             self.result_window = ResultWindow()

#         input_text = self.input_box.toPlainText()  # Get text from input box

#         # Analyze the text
#         analysis_result = self.text_analyzer.analyze_text(input_text)

#         # Update the result window with the analysis result
#         self.result_window.update_result(analysis_result)
        
#         self.result_window.show()

# class ResultWindow(qtw.QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Results")
#         self.setGeometry(100, 100, 800, 600)  # Adjust window size

#         self.layout = qtw.QVBoxLayout(self)

#         # Add a centered label for Analysis Results



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = mainWindow()
    mw.show()
    sys.exit(app.exec())

