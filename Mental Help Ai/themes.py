LIGHT_THEME = """
QWidget {
    background-color: #ffffff;
    color: #000;
}
QLineEdit, QTextEdit {
    background-color: #f5f5f5;
    color: #000;
    border: 1px solid #ccc;
    border-radius: 6px;
    padding: 5px;
}
QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #0078d7; /* Windows blue accent */
    outline: none;
}
QTabBar::tab {
    background: #e0e0e0;
    color: #000;
    padding: 6px 12px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}
QTabBar::tab:selected {
    background: #ffffff;
    font-weight: bold;
}
"""

DARK_THEME = """
QWidget {
    background-color: #121212;
    color: #fff;
}
QLineEdit, QTextEdit {
    background-color: #1e1e1e;
    color: #000;
    border: 1px solid #444;
    border-radius: 6px;
    padding: 5px;
}
QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #0078d7; /* Windows blue accent */
    outline: none;
}
QTabBar::tab {
    background: #2a2a2a;
    color: #fff;
    padding: 6px 12px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}
QTabBar::tab:selected {
    background: #121212;
    font-weight: bold;
}
"""
