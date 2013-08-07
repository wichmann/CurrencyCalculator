#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Währungsrechner mit grafischer Benutzeroberfläche.

@author: Christian Wichmann
"""

from PyQt4 import QtGui, uic
import sys


class CurrencyCalculator(QtGui.QMainWindow):  
    """Hauptfenster für Währungsrechner"""

    def __init__(self):
        """Initialisierung von Hauptfenster"""
        QtGui.QMainWindow.__init__(self)
        self.contentWidget = QtGui.QWidget()
        self.titleLabel = QtGui.QLabel(APP_NAME)

        ### Widgets für Ursprungswährung
        self.label_source = QtGui.QLabel("Ursprungswährung")
        self.input_source = QtGui.QLineEdit()
        self.input_source.setToolTip("Betrag in Ursprungswährung")
        self.input_source.textEdited.connect(self.handle_input_change)
        self.currency_source = QtGui.QComboBox(self)
        self.currency_source.addItems(currencies)
        self.currency_source.currentIndexChanged.connect(self.handle_input_change)

        ### Widgets für Zielwährung
        self.label_destination = QtGui.QLabel("Zielwährung")
        self.input_destination = QtGui.QLabel(EMPTY_VALUE)
        self.input_destination.setToolTip("Betrag in Zielwährung")
        self.currency_destination = QtGui.QComboBox(self)
        self.currency_destination.addItems(currencies)
        self.currency_destination.currentIndexChanged.connect(self.handle_input_change)

        ### Button
        self.quit_button = QtGui.QPushButton("Beenden")
        self.quit_button.setToolTip("Währungsrechner beenden")
        self.quit_button.clicked.connect(self.handle_quit)

        ### Layout setzen
        layout = QtGui.QGridLayout()
        layout.addWidget(self.titleLabel, 0, 1)
        layout.addWidget(self.label_source, 1, 0)
        layout.addWidget(self.input_source, 1, 1)
        layout.addWidget(self.currency_source, 1, 2)
        layout.addWidget(self.label_destination, 2, 0)
        layout.addWidget(self.input_destination, 2, 1)
        layout.addWidget(self.currency_destination, 2, 2)
        layout.addWidget(self.quit_button, 3, 2)
        
        self.contentWidget.setLayout(layout)
        self.setWindowTitle(APP_NAME)
        self.setCentralWidget(self.contentWidget)

    def handle_quit(self):
        """Handler zum Beenden des Programms"""
        self.close()

    def handle_input_change(self):
        """Handler bei Änderungen am Ursprungsbetrag"""
        input_text = self.input_source.text()
        try:
            # Umwandlung der Zeichenkette in eine Zahl
            input_value = float(self.input_source.text())
            output_value = str(input_value * self.calculateFactor())
            self.input_destination.setText(output_value)
        except ValueError:
            # bei einem Fehler gibt '0.00' als Zahl aus
            self.input_destination.setText(EMPTY_VALUE)
            # und zeige eine Infobox
            self.handle_wrong_number_format()

    def calculateFactor(self):
        """Berechnet den Umrechnungsfaktor für die ausgewählten Währungen"""
        factor = 1
        # zuerst Umrechnung in EUR
        factor *= factors[str(self.currency_source.currentText())]
        # dann Umrechnung in Zielwährung
        factor /= factors[str(self.currency_destination.currentText())]
        return factor

    def handle_wrong_number_format(self):
        """Zeigt eine Infobox bei Eingabe einer ungültigen Zahl"""
        reply = QtGui.QMessageBox.information(self, "Fehler",
            "Ungültige Zahl eingegeben!", QtGui.QMessageBox.Ok,
            QtGui.QMessageBox.Ok)


if __name__ == "__main__":
    
    APP_NAME = "Währungsrechner"
    EMPTY_VALUE = "0.00"
    
    # Liste mit allen Währungen und Umrechnungsfaktoren in EUR
    currencies = ("EUR", "USD", "YEN")
    factors = {"EUR": 1,
               "USD": 0.751540658,
               "YEN": 0.00774763265}

    app = QtGui.QApplication(sys.argv)
    main_window = CurrencyCalculator()  
    main_window.show()

    sys.exit(app.exec_())

