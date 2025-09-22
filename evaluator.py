from PyQt5 import QtWidgets as qtw, QtCore as qtc, QtGui as qtg

class EvaluatorWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Evaluator")
        self.setGeometry(150, 150, 800, 500)

        # Central widget
        central_widget = qtw.QWidget()
        self.setCentralWidget(central_widget)
        layout = qtw.QVBoxLayout(central_widget)

        # --- Input yellow box ---
        self.input_box = qtw.QTextEdit()
        self.input_box.setFont(qtg.QFont("Times New Roman", 12))
        self.input_box.setPlaceholderText("Enter text for evaluation...")
        self.input_box.setStyleSheet("""
            background-color: lightyellow;
            border: 2px solid darkblue;
            border-radius: 8px;
            padding: 8px;
        """)
        layout.addWidget(self.input_box)

        # --- Output box ---
        self.output_box = qtw.QTextEdit()
        self.output_box.setFont(qtg.QFont("Times New Roman", 12))
        self.output_box.setReadOnly(True)
        self.output_box.setStyleSheet("""
            background-color: #f5f5f5;
            border: 1px solid gray;
            border-radius: 8px;
            padding: 8px;
        """)
        layout.addWidget(self.output_box)

        # --- Menu Bar with dropdowns ---
        menubar = self.menuBar()

        # Indices dropdown
        indices_menu = menubar.addMenu("Indices")
        indices = ["MTLD", "HD-D (vocd)", "Maas"]
        for idx in indices:
            action = indices_menu.addAction(idx)
            action.triggered.connect(lambda checked, text=idx: self.select_index(text))

        # View dropdown
        view_menu = menubar.addMenu("View")
        view_options = ["Show Index", "Show Text"]
        for opt in view_options:
            action = view_menu.addAction(opt)
            action.triggered.connect(lambda checked, text=opt: self.select_view(text))

    # --- Handlers for dropdowns ---
    def select_index(self, text):
        self.output_box.append(f"Selected Index: {text}")

    def select_view(self, text):
        self.output_box.append(f"View Option: {text}")
