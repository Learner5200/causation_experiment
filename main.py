# === IMPORTS ===
import sys
from PyQt5.QtWidgets import *
from collections import OrderedDict
from causationUI import *
from auxiliaryFunctions import *
from causationProgram import *


# === CONSTANTS ===

FILENAME = 'causationData.csv'
CONDITIONS = {
    'experimental': 0,
    'control': 0
}
FIELDS = [ # List of fields for the data file
    'participantID',
    'condition',
    'gender',
    'age',
    'unlockTime',
    'triangleTime',
    'goalTime',
    'congratulationsTime',
    'expRemember',
    'expSaw',
    'expSense',
    'expOther',
    'attribution'
]
# Turns list into dictionary for recording data for each field; orderedDict allows order of above list to be maintained
# when this is written to the csv file
FIELDSDIC = OrderedDict((field, 0) for field in FIELDS)


# === FUNCTIONS ===

def sizeWindow(window):
    # Sets window parameters to fit user's desktop
    window.setGeometry(
        0,
        0,
        window.desktop.width(),
        window.desktop.height()
    )

def centreWidget(widget):
    centredX = window.width() / 2
    centredY = window.height() / 2
    widget.setGeometry(
        centredX - widget.width() / 2,
        centredY - widget.height() / 2,
        widget.width(),
        widget.height()
    )

def nextPage():
    index = ui.experimentPages.currentIndex()
    maxIndex = len(ui.experimentPages.children()) - 2
    if index < maxIndex:
        ui.experimentPages.setCurrentIndex(index + 1)
    else:
        ui.experimentPages.setCurrentIndex(max)

def previousPage():
    index = ui.experimentPages.currentIndex()
    minIndex = 0
    if index > minIndex:
        ui.experimentPages.setCurrentIndex(index - 1)

def switchWindow():
    # Hides PyQt window and runs Pygame program; when the latter finishes, the PyQt window resumes at the next page
    window.hide()
    causation(FIELDSDIC['condition'], window)
    window.show()
    nextPage()

def checkConsent():
    if ui.consentBox.isChecked():
        ui.consentError.hide()
        if window.sender() == ui.btnConsentNext:
            nextPage()
    else:
        ui.consentError.show()

def checkAge():
    if int(ui.ageBox.value()) < 18:
        ui.ageError18.show()
        window.age18_OK = False  # Underscored to avoid ambiguity of 'O'
    else:
        ui.ageError18.hide()
        window.age18_OK = True

    if int(ui.ageBox.value()) > 90:
        ui.ageError90.show()
        window.age90_OK = False
    else:
        ui.ageError90.hide()
        window.age90_OK = True

def checkGender():
    if ui.genderBox.currentText() == '':
        ui.genderError.show()
        window.genderOK = False
    else:
        ui.genderError.hide()
        window.genderOK = True

def checkDemographics():
    checkAge()
    checkGender()
    if (window.age18_OK and window.age90_OK
            and window.genderOK):
        FIELDSDIC['age'] = str(ui.ageBox.value()) # Records value as string to facilitate writing
        FIELDSDIC['gender'] = ui.genderBox.currentText()
        switchWindow()

def checkCausalOrder():
    dropDownList = [ui.dropDown1, ui.dropDown2, ui.dropDown3, ui.dropDown4]

    # Stores mapping from variable names/values to the code used in the csv file
    codingDic = {ui.dropDown1: '1', ui.dropDown2: '2', ui.dropDown3: '3', ui.dropDown4: '4',
                 'The green square collided with the black platform': 'unlockTime',
                 'The red square entered the purple box': 'goalTime',
                 'The red square became a triangle': 'triangleTime',
                 "A 'Congratulations' message appeared": 'congratulationsTime'}

    # Checks if any field is empty, or shares a value with any other field
    window.orderOK = True
    for item1 in dropDownList:
        if item1.currentText() == '----------':
            window.orderOK = False
        for item2 in [item for item in dropDownList if item != item1]:
            if item1.currentText() == item2.currentText():
                window.orderOK = False

    if window.orderOK == False:
        ui.orderError.show()
    else:
        ui.orderError.hide()
        if window.sender() == ui.btnCausalNext:
            # Codes the data before storing it
            for item in dropDownList:
                key = codingDic[item.currentText()]
                value = codingDic[item]
                FIELDSDIC[key] = value
            nextPage()

def checkExplanation():
    explanationCheckboxes = [ui.expCheckOther, ui.expCheckRemember, ui.expCheckSense, ui.expCheckSaw]
    if all(checkbox.isChecked() == False for checkbox in explanationCheckboxes):
        ui.expError.show() # Shows error if no checkboxes are checked
    else:
        ui.expError.hide()
        if window.sender() == ui.btnExplanationNext:
            FIELDSDIC['expSaw'] = str(ui.expCheckSaw.isChecked())
            FIELDSDIC['expSense'] = str(ui.expCheckSense.isChecked())
            FIELDSDIC['expRemember'] = str(ui.expCheckRemember.isChecked())
            if ui.expTextOther.toPlainText() == '':
                FIELDSDIC['expOther'] = 'NA' # Codes empty 'other' box as NA
            else:
                FIELDSDIC['expOther'] = ui.expTextOther.toPlainText()
            nextPage()

def checkAttribution():
    attributionCheckboxes = [ui.attCheckRed, ui.attCheckGreen, ui.attCheckOther]
    if all(checkbox.isChecked() == False for checkbox in attributionCheckboxes):
        ui.attError.show()
    else:
        ui.attError.hide()
        if window.sender() == ui.btnAttributionNext:
            if ui.attCheckRed.isChecked():
                FIELDSDIC['attribution'] = 'red'
            elif ui.attCheckGreen.isChecked():
                FIELDSDIC['attribution'] = 'green'
            elif ui.attCheckOther.isChecked():
                FIELDSDIC['attribution'] = ui.attTextOther.toPlainText()
            nextPage()

def completeExperiment():
    recordData(FILENAME, list(FIELDSDIC.values())) # Writes values from dictionary of fields to csv file
    window.close()


# === SETUP ===

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

# Hide error messages
ui.consentError.hide()
ui.ageError18.hide()
ui.ageError90.hide()
ui.genderError.hide()
ui.orderError.hide()
ui.expError.hide()
ui.attError.hide()
# Subjects in the control condition should not see an option that mentions previous rounds
if FIELDSDIC['condition'] == 'control':
    ui.expCheckRemember.hide()

# Connect signals to relevant functions
ui.btnConsentNext.clicked.connect(checkConsent)
ui.btnDemogNext.clicked.connect(checkDemographics)
ui.consentBox.clicked.connect(checkConsent)
ui.ageBox.valueChanged.connect(checkAge)
ui.genderBox.currentIndexChanged.connect(checkGender)
ui.btnCausalNext.clicked.connect(checkCausalOrder)
ui.btnExplanationNext.clicked.connect(checkExplanation)
ui.btnAttributionNext.clicked.connect(checkAttribution)

ui.btnExplanationPrevious.clicked.connect(previousPage)
ui.btnAttributionPrevious.clicked.connect(previousPage)

ui.btnDebriefExit.clicked.connect(completeExperiment)

ui.dropDown1.currentIndexChanged.connect(checkCausalOrder)
ui.dropDown2.currentIndexChanged.connect(checkCausalOrder)
ui.dropDown3.currentIndexChanged.connect(checkCausalOrder)
ui.dropDown4.currentIndexChanged.connect(checkCausalOrder)

ui.expCheckRemember.clicked.connect(checkExplanation)
ui.expCheckSaw.clicked.connect(checkExplanation)
ui.expCheckSense.clicked.connect(checkExplanation)
ui.expCheckOther.clicked.connect(checkExplanation)

ui.attCheckRed.clicked.connect(checkAttribution)
ui.attCheckGreen.clicked.connect(checkAttribution)
ui.attCheckOther.clicked.connect(checkAttribution)



# Sizing and positioning
window.desktop = QDesktopWidget().screenGeometry() # Gets desktop width and height
sizeWindow(window)
centreWidget(ui.experimentPages)


# === MAIN PROGRAM ===

conditionIndex = FIELDS.index('condition') # Needed to set condition
FIELDSDIC['participantID'] = initialise(FILENAME, FIELDS)
FIELDSDIC['condition'] = setCondition(FILENAME, conditionIndex, CONDITIONS)
ui.debriefText.setText(ui.debriefText.text().format(FIELDSDIC['condition']))
window.show()

sys.exit(app.exec_())