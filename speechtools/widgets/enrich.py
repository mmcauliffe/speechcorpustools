
from collections import OrderedDict

from PyQt5 import QtGui, QtCore, QtWidgets

from polyglotdb import CorpusContext

from .base import RadioSelectWidget, BaseSummaryWidget

from .lexicon import WordSelectWidget

from .inventory import PhoneSelectWidget, PhoneSubsetSelectWidget

class BaseDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(BaseDialog, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()

        aclayout = QtWidgets.QHBoxLayout()

        self.acceptButton = QtWidgets.QPushButton('Encode')
        self.acceptButton.clicked.connect(self.accept)
        self.cancelButton = QtWidgets.QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.reject)

        aclayout.addWidget(self.acceptButton)
        aclayout.addWidget(self.cancelButton)

        layout.addLayout(aclayout)

        self.setLayout(layout)

    def validate(self):
        return True

    def accept(self):
        if self.validate():
            super(BaseDialog, self).accept()

class EncodePauseDialog(BaseDialog):
    def __init__(self, config, parent):
        super(EncodePauseDialog, self).__init__(parent)

        layout = QtWidgets.QFormLayout()

        self.wordSelect = WordSelectWidget(config)

        layout.addRow(self.wordSelect)

        self.layout().insertLayout(0, layout)

        self.setWindowTitle('Encode non-speech elements')

    def value(self):
        return self.wordSelect.value()

class EncodeUtteranceDialog(BaseDialog):
    def __init__(self, config, parent):
        super(EncodeUtteranceDialog, self).__init__(parent)

        layout = QtWidgets.QFormLayout()

        self.minPauseEdit = QtWidgets.QLineEdit()
        self.minPauseEdit.setText('0')

        self.minUttEdit = QtWidgets.QLineEdit()
        self.minUttEdit.setText('0')

        layout.addRow('Minimum duration of pause between utterances (seconds)', self.minPauseEdit)
        layout.addRow('Minimum duration of utterances (seconds)', self.minUttEdit)

        self.layout().insertLayout(0, layout)

        self.setWindowTitle('Encode utterances')

    def validate(self):
        try:
            val = self.value()
        except ValueError:
            reply = QtWidgets.QMessageBox.critical(self,
                    "Invalid information",
                    'Please make sure that the durations are properly specified.')
            return False
        if val[0] > 10 or val[1] > 10:
            reply = QtWidgets.QMessageBox.warning(self, "Long duration",
            'Are you sure that durations are specified in seconds?',
            buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            if reply == QtWidgets.QMessageBox.Cancel:
                return False
        return True


    def value(self):
        return float(self.minPauseEdit.text()), float(self.minUttEdit.text())

class EncodeSpeechRateDialog(BaseDialog):
    def __init__(self, config, parent):
        super(EncodeSpeechRateDialog, self).__init__(parent)

        layout = QtWidgets.QFormLayout()

        self.subsetSelect = PhoneSubsetSelectWidget(config)

        layout.addRow('Select set of phones to count', self.subsetSelect)

        self.layout().insertLayout(0, layout)

        self.setWindowTitle('Encode speech rate')

    def value(self):
        return self.subsetSelect.value()

class EncodeUtterancePositionDialog(BaseDialog):
    def __init__(self, config, parent):
        super(EncodeUtterancePositionDialog, self).__init__(parent)

        self.setWindowTitle('Encode utterance positions')

class AnalyzeAcousticsDialog(BaseDialog):
    def __init__(self, config, parent):
        super(AnalyzeAcousticsDialog, self).__init__(parent)

        self.setWindowTitle('Analyze acoustics')

        layout = QtWidgets.QFormLayout()

        self.acousticsWidget = RadioSelectWidget('Acoustics to encode',
                                            OrderedDict([
                                            #('Probabilistic onsets and codas (language-independent)','probabilistic'),
                                            ('Pitch','pitch'),]))

        layout.addRow(self.acousticsWidget)

        self.layout().insertLayout(0, layout)

    def value(self):
        return self.acousticsWidget.value()

class EncodeSyllabicsDialog(BaseDialog):
    def __init__(self, config, parent):
        super(EncodeSyllabicsDialog, self).__init__(parent)

        layout = QtWidgets.QFormLayout()

        self.phoneSelect = PhoneSelectWidget(config)
        for i in range(self.phoneSelect.selectWidget.count()):
            item = self.phoneSelect.selectWidget.item(i)
            for v in ['a','e','i','o','u']:
                if v in item.text().lower():
                    index = self.phoneSelect.selectWidget.model().index(i,0)
                    self.phoneSelect.selectWidget.selectionModel().select(index, QtCore.QItemSelectionModel.Select)
                    break

        layout.addRow('Syllabic segments', self.phoneSelect)

        self.layout().insertLayout(0, layout)

        self.setWindowTitle('Encode syllabic segments')

    def value(self):
        return self.phoneSelect.value()

class EncodeSyllablesDialog(BaseDialog):
    def __init__(self, config, parent):
        super(EncodeSyllablesDialog, self).__init__(parent)

        layout = QtWidgets.QFormLayout()

        self.algorithmWidget = RadioSelectWidget('Syllabification algorithm',
                                            OrderedDict([
                                            #('Probabilistic onsets and codas (language-independent)','probabilistic'),
                                            ('Max attested onset (language-independent)','maxonset'),]))

        layout.addRow(self.algorithmWidget)

        self.layout().insertLayout(0, layout)

        self.setWindowTitle('Encode syllables')

    def value(self):
        return self.algorithmWidget.value()

class EncodePhoneSubsetDialog(BaseDialog):
    def __init__(self, config, parent):
        super(EncodePhoneSubsetDialog, self).__init__(parent)

        layout = QtWidgets.QFormLayout()

        self.labelEdit = QtWidgets.QLineEdit()

        layout.addRow('Class label', self.labelEdit)

        self.phoneSelect = PhoneSelectWidget(config)

        layout.addRow('Segments', self.phoneSelect)

        self.layout().insertLayout(0, layout)

        self.setWindowTitle('Encode phone subsets')

    def value(self):
        return self.labelEdit.text(), self.phoneSelect.value()

class EnrichLexiconDialog(BaseDialog):
    def __init__(self, config, parent):
        super(EnrichLexiconDialog, self).__init__(parent)

        layout = QtWidgets.QFormLayout()

        self.caseCheck = QtWidgets.QCheckBox()

        layout.addRow('Case sensitive', self.caseCheck)

        self.layout().insertLayout(0, layout)

        self.setWindowTitle('Enrich lexicon')
        self.path = None

    def accept(self):
        self.path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select lexicon", filter = "CSV (*.txt  *.csv)")
        if not self.path:
            return
        QtWidgets.QDialog.accept(self)

    def value(self):
        return self.path, self.caseCheck.isChecked()

class EnrichFeaturesDialog(BaseDialog):
    def __init__(self, config, parent):
        super(EnrichFeaturesDialog, self).__init__(parent)

        layout = QtWidgets.QFormLayout()

        self.layout().insertLayout(0, layout)

        self.setWindowTitle('Enrich phones with features')
        self.path = None

    def accept(self):
        self.path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select feature file", filter = "CSV (*.txt  *.csv)")
        if not self.path:
            return
        QtWidgets.QDialog.accept(self)

    def value(self):
        return self.path

class AnnotationTypeSelect(QtWidgets.QComboBox):
    def __init__(self, hierarchy, subsets = False):
        super(AnnotationTypeSelect, self).__init__()
        self.hierarchy = hierarchy
        self.subsets = subsets
        self.baseAnnotation = None
        self.generateItems()

    def setBase(self, base):
        self.baseAnnotation = base
        self.generateItems()

    def generateItems(self):
        self.clear()
        if self.baseAnnotation is None:
            toiter = self.hierarchy.highest_to_lowest[:-1]
        else:
            toiter = self.hierarchy.get_lower_types(self.baseAnnotation)
        for at in toiter:
            self.addItem(at)
            if self.subsets:
                subs = []
                if at in self.hierarchy.subset_types:
                    subs += self.hierarchy.subset_types[at]
                if at in self.hierarchy.subset_tokens:
                    subs += self.hierarchy.subset_tokens[at]

                for s in sorted(subs):
                    self.addItem(' - '.join([at, s]))

class EncodeHierarchicalPropertiesDialog(BaseDialog):
    def __init__(self, config, parent):
        super(EncodeHierarchicalPropertiesDialog, self).__init__(parent)
        with CorpusContext(config) as c:
            hierarchy = c.hierarchy
        layout = QtWidgets.QFormLayout()

        self.higherSelect = AnnotationTypeSelect(hierarchy)
        self.higherSelect.currentIndexChanged.connect(self.updateBase)
        self.higherSelect.currentIndexChanged.connect(self.updateName)
        self.lowerSelect = AnnotationTypeSelect(hierarchy, subsets = True)
        self.lowerSelect.currentIndexChanged.connect(self.updateName)

        self.typeSelect = QtWidgets.QComboBox()
        self.typeSelect.addItem('count')
        self.typeSelect.addItem('rate')
        self.typeSelect.addItem('position')
        self.typeSelect.currentIndexChanged.connect(self.updateName)

        self.nameEdit = QtWidgets.QLineEdit()
        self.updateBase()
        self.updateName()

        layout.addRow('Higher annotation', self.higherSelect)
        layout.addRow('Lower annotation', self.lowerSelect)
        layout.addRow('Type of property', self.typeSelect)
        layout.addRow('Name of property', self.nameEdit)

        self.layout().insertLayout(0, layout)

        self.setWindowTitle('Enrich hierarchical annotations')

    def updateBase(self):
        self.lowerSelect.setBase(self.higherSelect.currentText())

    def updateName(self):
        lower, subset = self.splitLower()
        if subset is not None:
            lower = subset
        to_build = [self.typeSelect.currentText().title(), 'of', lower,
                    'in', self.higherSelect.currentText()]
        self.nameEdit.setText('_'.join(to_build))

    def validate(self):
        if self.nameEdit.text() == '':
            reply = QtWidgets.QMessageBox.critical(self,
                    "Missing information", 'Please make sure a name for the new property is specified.')
            return False
        ## FIXME add check for whether the name of the property already exists
        return True

    def splitLower(self):
        lower_text = self.lowerSelect.currentText()
        if ' - ' in lower_text:
            lower, subset = lower_text.split(' - ')
        else:
            lower = lower_text
            subset = None
        return lower, subset

    def value(self):
        lower, subset = self.splitLower()
        return {'higher': self.higherSelect.currentText(), 'type':self.typeSelect.currentText(),
                'lower': lower, 'subset': subset, 'name': self.nameEdit.text()}

class EncodeLabel(QtWidgets.QWidget):
    toEncode = QtCore.pyqtSignal(str)
    def __init__(self, annotation_type, parent = None):
        super(EncodeLabel, self).__init__(parent)

        self.annotation_type = annotation_type

        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel(self.annotation_type.title() + 's')
        layout.addWidget(self.label)

        self.enrichButton = QtWidgets.QToolButton()
        self.enrichButton.setText('Enrich')
        self.enrichButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)

        self.enrichButton.setEnabled(False)

        #self.encodeButton.clicked.connect(self.toEncode.emit)

        layout.addWidget(self.enrichButton)

        self.setLayout(layout)


    def updateEnrichMenu(self, config):
        menu = QtWidgets.QMenu()
        if config is not None:
            self.enrichButton.setEnabled(True)
            with CorpusContext(config) as c:
                if self.annotation_type == 'non-speech element':
                    t = 'Encode non-speech elements'
                    if c.hierarchy.has_token_subset(c.word_name, 'pause'):
                        t = 'Re-encode non-speech elements'
                    pauseAction = QtWidgets.QAction(t, self)
                    pauseAction.triggered.connect(lambda : self.toEncode.emit('pause'))
                    menu.addAction(pauseAction)
                elif self.annotation_type not in [c.phone_name, c.word_name]:
                    t = 'Encode'
                    if self.annotation_type in c.hierarchy.annotation_types:
                        t = 'Re-encode'
                    encodeAction = QtWidgets.QAction(t, self)
                    encodeAction.triggered.connect(lambda : self.toEncode.emit(self.annotation_type))
                    menu.addAction(encodeAction)
                elif self.annotation_type == c.word_name:
                    lexiconAction = QtWidgets.QAction('Enrich lexicon', self)
                    lexiconAction.triggered.connect(lambda : self.toEncode.emit('lexicon'))
                    menu.addAction(lexiconAction)
                else:
                    t = 'Encode syllabic segments'
                    if c.hierarchy.has_type_subset(c.phone_name, 'syllabic'):
                        t = 'Re-encode syllabic segments'
                    syllabicsAction = QtWidgets.QAction(t, self)
                    syllabicsAction.triggered.connect(lambda : self.toEncode.emit('syllabic'))
                    menu.addAction(syllabicsAction)
                    classAction = QtWidgets.QAction('Encode phone subsets (classes)', self)
                    classAction.triggered.connect(lambda : self.toEncode.emit('class'))
                    menu.addAction(classAction)
                    inventoryAction = QtWidgets.QAction('Enrich phonological inventory', self)
                    inventoryAction.triggered.connect(lambda : self.toEncode.emit('inventory'))
                    menu.addAction(inventoryAction)
        else:
            self.enrichButton.setEnabled(False)
        self.enrichButton.setMenu(menu)


class PropertySummaryWidget(QtWidgets.QWidget):
    def __init__(self, property_name, parent = None):
        super(PropertySummaryWidget, self).__init__(parent)

        layout = QtWidgets.QFormLayout()

        layout.addRow(QtWidgets.QLabel(property_name))

        self.setLayout(layout)

class AnnotationSummaryWidget(QtWidgets.QWidget):
    def __init__(self, annotation_type, parent = None):
        super(AnnotationSummaryWidget, self).__init__(parent)
        self.annotation_type = annotation_type

        layout = QtWidgets.QHBoxLayout()

        self.unknownWidget = QtWidgets.QLabel('Please connect to a server and select a corpus.')

        self.setLayout(layout)

    def updateConfig(self, config):
        while self.layout().count():
            item = self.layout().takeAt(0)
            if item is not None:
                w = item.widget()
                w.setParent(None)
                if w != self.unknownWidget:
                    w.deleteLater()
        if config is None:
            self.layout().addWidget(self.unknownWidget)
        else:
            with CorpusContext(config) as c:
                if self.annotation_type in c.hierarchy.annotation_types:
                    props = (c.hierarchy.type_properties[self.annotation_type] |
                            c.hierarchy.token_properties[self.annotation_type])
                    for p, t in sorted(props):
                        if p == 'id':
                            continue
                        w = PropertySummaryWidget(p)
                        self.layout().addWidget(w)
                else:
                    lab = 'This annotation type is not encoded.'
                    if self.annotation_type == 'syllable' and \
                            not c.hierarchy.has_type_subset(c.phone_name, 'syllabic'):
                        lab += '\nSyllabic phones must be encoded before syllables can be encoded.'
                    elif self.annotation_type == 'utterance' and \
                            not c.hierarchy.has_token_subset(c.word_name, 'pause'):
                        lab += '\nNon-speech elements must be encoded before utterances can be encoded.'
                    self.layout().addWidget(QtWidgets.QLabel(lab))


class EnrichmentWidget(QtWidgets.QWidget):
    def __init__(self, annotation_type, parent = None):
        super(EnrichmentWidget, self).__init__(parent)
        self.annotation_type = annotation_type

        layout = QtWidgets.QHBoxLayout()

        self.label = EncodeLabel(self.annotation_type)

        self.summary = AnnotationSummaryWidget(self.annotation_type)

        layout.addWidget(self.label)

        layout.addWidget(self.summary)

        self.setLayout(layout)

    def updateConfig(self, config):
        self.summary.updateConfig(config)
        self.label.updateEnrichMenu(config)

class PauseWidget(EnrichmentWidget):
    def __init__(self, parent = None):
        super(PauseWidget, self).__init__('non-speech element', parent)

class EnrichmentSummaryWidget(BaseSummaryWidget):
    def __init__(self, parent = None):
        super(EnrichmentSummaryWidget, self).__init__(parent)


        layout = QtWidgets.QVBoxLayout()
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        mainWidget = QtWidgets.QWidget()

        mainWidget.setSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
        mainWidget.setLayout(self.mainLayout)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(mainWidget)
        scroll.setMinimumHeight(10)
        scroll.setSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
        policy = scroll.sizePolicy()
        policy.setVerticalStretch(1)
        scroll.setSizePolicy(policy)
        layout.addWidget(scroll)

        self.pauseWidget = PauseWidget()

        self.mainLayout.addWidget(self.pauseWidget)

        for k in ['utterance', 'word', 'syllable', 'phone']:
            self.mainLayout.addWidget(EnrichmentWidget(k))

        self.setLayout(layout)

    def refresh(self):
        for i in range(self.mainLayout.count()):
            self.mainLayout.itemAt(i).widget().updateConfig(self.config)
