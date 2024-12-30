# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'novel_generator_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QStatusBar, QTabWidget, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_NovelGeneratorWindow(object):
    def setupUi(self, NovelGeneratorWindow):
        if not NovelGeneratorWindow.objectName():
            NovelGeneratorWindow.setObjectName(u"NovelGeneratorWindow")
        NovelGeneratorWindow.resize(1200, 800)
        self.centralwidget = QWidget(NovelGeneratorWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setSpacing(10)
        self.leftLayout.setObjectName(u"leftLayout")
        self.settingsGroup = QGroupBox(self.centralwidget)
        self.settingsGroup.setObjectName(u"settingsGroup")
        self.settingsLayout = QVBoxLayout(self.settingsGroup)
        self.settingsLayout.setObjectName(u"settingsLayout")
        self.nameLabel = QLabel(self.settingsGroup)
        self.nameLabel.setObjectName(u"nameLabel")

        self.settingsLayout.addWidget(self.nameLabel)

        self.nameEdit = QLineEdit(self.settingsGroup)
        self.nameEdit.setObjectName(u"nameEdit")

        self.settingsLayout.addWidget(self.nameEdit)

        self.synopsisLabel = QLabel(self.settingsGroup)
        self.synopsisLabel.setObjectName(u"synopsisLabel")

        self.settingsLayout.addWidget(self.synopsisLabel)

        self.synopsisEdit = QTextEdit(self.settingsGroup)
        self.synopsisEdit.setObjectName(u"synopsisEdit")
        self.synopsisEdit.setMaximumHeight(100)

        self.settingsLayout.addWidget(self.synopsisEdit)

        self.genreLabel = QLabel(self.settingsGroup)
        self.genreLabel.setObjectName(u"genreLabel")

        self.settingsLayout.addWidget(self.genreLabel)

        self.genreCombo = QComboBox(self.settingsGroup)
        self.genreCombo.setObjectName(u"genreCombo")

        self.settingsLayout.addWidget(self.genreCombo)

        self.styleLabel = QLabel(self.settingsGroup)
        self.styleLabel.setObjectName(u"styleLabel")

        self.settingsLayout.addWidget(self.styleLabel)

        self.styleCombo = QComboBox(self.settingsGroup)
        self.styleCombo.setObjectName(u"styleCombo")

        self.settingsLayout.addWidget(self.styleCombo)

        self.cultureLabel = QLabel(self.settingsGroup)
        self.cultureLabel.setObjectName(u"cultureLabel")

        self.settingsLayout.addWidget(self.cultureLabel)

        self.cultureCombo = QComboBox(self.settingsGroup)
        self.cultureCombo.addItem("")
        self.cultureCombo.addItem("")
        self.cultureCombo.addItem("")
        self.cultureCombo.addItem("")
        self.cultureCombo.addItem("")
        self.cultureCombo.addItem("")
        self.cultureCombo.addItem("")
        self.cultureCombo.addItem("")
        self.cultureCombo.addItem("")
        self.cultureCombo.setObjectName(u"cultureCombo")

        self.settingsLayout.addWidget(self.cultureCombo)

        self.chapterCountLabel = QLabel(self.settingsGroup)
        self.chapterCountLabel.setObjectName(u"chapterCountLabel")

        self.settingsLayout.addWidget(self.chapterCountLabel)

        self.chapterCountSlider = QSlider(self.settingsGroup)
        self.chapterCountSlider.setObjectName(u"chapterCountSlider")
        self.chapterCountSlider.setMinimum(2)
        self.chapterCountSlider.setMaximum(20)
        self.chapterCountSlider.setValue(5)
        self.chapterCountSlider.setOrientation(Qt.Horizontal)

        self.settingsLayout.addWidget(self.chapterCountSlider)

        self.avgChapterWordsLabel = QLabel(self.settingsGroup)
        self.avgChapterWordsLabel.setObjectName(u"avgChapterWordsLabel")

        self.settingsLayout.addWidget(self.avgChapterWordsLabel)

        self.avgChapterWordsSlider = QSlider(self.settingsGroup)
        self.avgChapterWordsSlider.setObjectName(u"avgChapterWordsSlider")
        self.avgChapterWordsSlider.setMinimum(1000)
        self.avgChapterWordsSlider.setMaximum(10000)
        self.avgChapterWordsSlider.setSingleStep(100)
        self.avgChapterWordsSlider.setValue(3000)
        self.avgChapterWordsSlider.setOrientation(Qt.Horizontal)

        self.settingsLayout.addWidget(self.avgChapterWordsSlider)

        self.totalWordsLabel = QLabel(self.settingsGroup)
        self.totalWordsLabel.setObjectName(u"totalWordsLabel")

        self.settingsLayout.addWidget(self.totalWordsLabel)

        self.mainCharacterCountLabel = QLabel(self.settingsGroup)
        self.mainCharacterCountLabel.setObjectName(u"mainCharacterCountLabel")

        self.settingsLayout.addWidget(self.mainCharacterCountLabel)

        self.mainCharacterCountSlider = QSlider(self.settingsGroup)
        self.mainCharacterCountSlider.setObjectName(u"mainCharacterCountSlider")
        self.mainCharacterCountSlider.setMinimum(1)
        self.mainCharacterCountSlider.setMaximum(10)
        self.mainCharacterCountSlider.setValue(3)
        self.mainCharacterCountSlider.setOrientation(Qt.Horizontal)

        self.settingsLayout.addWidget(self.mainCharacterCountSlider)

        self.supportCharacterCountLabel = QLabel(self.settingsGroup)
        self.supportCharacterCountLabel.setObjectName(u"supportCharacterCountLabel")

        self.settingsLayout.addWidget(self.supportCharacterCountLabel)

        self.supportCharacterCountSlider = QSlider(self.settingsGroup)
        self.supportCharacterCountSlider.setObjectName(u"supportCharacterCountSlider")
        self.supportCharacterCountSlider.setMinimum(0)
        self.supportCharacterCountSlider.setMaximum(20)
        self.supportCharacterCountSlider.setValue(5)
        self.supportCharacterCountSlider.setOrientation(Qt.Horizontal)

        self.settingsLayout.addWidget(self.supportCharacterCountSlider)

        self.enableTranslation = QCheckBox(self.settingsGroup)
        self.enableTranslation.setObjectName(u"enableTranslation")

        self.settingsLayout.addWidget(self.enableTranslation)

        self.languageLayout = QVBoxLayout()
        self.languageLayout.setObjectName(u"languageLayout")

        self.settingsLayout.addLayout(self.languageLayout)

        self.generateBtn = QPushButton(self.settingsGroup)
        self.generateBtn.setObjectName(u"generateBtn")

        self.settingsLayout.addWidget(self.generateBtn)

        self.expandBtn = QPushButton(self.settingsGroup)
        self.expandBtn.setObjectName(u"expandBtn")

        self.settingsLayout.addWidget(self.expandBtn)

        self.translateBtn = QPushButton(self.settingsGroup)
        self.translateBtn.setObjectName(u"translateBtn")
        self.translateBtn.setEnabled(False)

        self.settingsLayout.addWidget(self.translateBtn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.settingsLayout.addItem(self.verticalSpacer)


        self.leftLayout.addWidget(self.settingsGroup)


        self.horizontalLayout.addLayout(self.leftLayout)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.outlineTab = QWidget()
        self.outlineTab.setObjectName(u"outlineTab")
        self.verticalLayout = QVBoxLayout(self.outlineTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.outlineEdit = QTextEdit(self.outlineTab)
        self.outlineEdit.setObjectName(u"outlineEdit")

        self.verticalLayout.addWidget(self.outlineEdit)

        self.tabWidget.addTab(self.outlineTab, "")
        self.expandedTab = QWidget()
        self.expandedTab.setObjectName(u"expandedTab")
        self.verticalLayout_2 = QVBoxLayout(self.expandedTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.expandedEdit = QTextEdit(self.expandedTab)
        self.expandedEdit.setObjectName(u"expandedEdit")

        self.verticalLayout_2.addWidget(self.expandedEdit)

        self.tabWidget.addTab(self.expandedTab, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        NovelGeneratorWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(NovelGeneratorWindow)
        self.statusbar.setObjectName(u"statusbar")
        NovelGeneratorWindow.setStatusBar(self.statusbar)

        self.retranslateUi(NovelGeneratorWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(NovelGeneratorWindow)
    # setupUi

    def retranslateUi(self, NovelGeneratorWindow):
        NovelGeneratorWindow.setWindowTitle(QCoreApplication.translate("NovelGeneratorWindow", u"\u5c0f\u8bf4\u751f\u6210\u5668", None))
        self.settingsGroup.setTitle(QCoreApplication.translate("NovelGeneratorWindow", u"\u8bbe\u7f6e", None))
        self.nameLabel.setText(QCoreApplication.translate("NovelGeneratorWindow", u"\u5c0f\u8bf4\u540d\u79f0\uff1a", None))
        self.nameEdit.setPlaceholderText(QCoreApplication.translate("NovelGeneratorWindow", u"\u8f93\u5165\u5c0f\u8bf4\u540d\u79f0\uff08\u53ef\u9009\uff09", None))
        self.synopsisLabel.setText(QCoreApplication.translate("NovelGeneratorWindow", u"\u6545\u4e8b\u6897\u6982\uff1a", None))
        self.synopsisEdit.setPlaceholderText(QCoreApplication.translate("NovelGeneratorWindow", u"\u8f93\u5165\u6545\u4e8b\u6897\u6982\uff08\u53ef\u9009\uff09", None))
        self.genreLabel.setText(QCoreApplication.translate("NovelGeneratorWindow", u"\u5c0f\u8bf4\u7c7b\u578b\uff1a", None))
        self.styleLabel.setText(QCoreApplication.translate("NovelGeneratorWindow", u"\u5199\u4f5c\u98ce\u683c\uff1a", None))
        self.cultureLabel.setText(QCoreApplication.translate("NovelGeneratorWindow", u"\u6587\u5316\u80cc\u666f\uff1a", None))
        self.cultureCombo.setItemText(0, QCoreApplication.translate("NovelGeneratorWindow", u"\u4e2d\u56fd\u4f20\u7edf\u6587\u5316", None))
        self.cultureCombo.setItemText(1, QCoreApplication.translate("NovelGeneratorWindow", u"\u73b0\u4ee3\u90fd\u5e02\u6587\u5316", None))
        self.cultureCombo.setItemText(2, QCoreApplication.translate("NovelGeneratorWindow", u"\u6b27\u7f8e\u6587\u5316", None))
        self.cultureCombo.setItemText(3, QCoreApplication.translate("NovelGeneratorWindow", u"\u65e5\u672c\u6587\u5316", None))
        self.cultureCombo.setItemText(4, QCoreApplication.translate("NovelGeneratorWindow", u"\u97e9\u56fd\u6587\u5316", None))
        self.cultureCombo.setItemText(5, QCoreApplication.translate("NovelGeneratorWindow", u"\u5370\u5ea6\u6587\u5316", None))
        self.cultureCombo.setItemText(6, QCoreApplication.translate("NovelGeneratorWindow", u"\u963f\u62c9\u4f2f\u6587\u5316", None))
        self.cultureCombo.setItemText(7, QCoreApplication.translate("NovelGeneratorWindow", u"\u975e\u6d32\u6587\u5316", None))
        self.cultureCombo.setItemText(8, QCoreApplication.translate("NovelGeneratorWindow", u"\u62c9\u7f8e\u6587\u5316", None))

        self.chapterCountLabel.setText(QCoreApplication.translate("NovelGeneratorWindow", u"\u7ae0\u8282\u6570\u91cf\uff1a5\u7ae0", None))
        self.avgChapterWordsLabel.setText(QCoreApplication.translate("NovelGeneratorWindow", u"\u6bcf\u7ae0\u5e73\u5747\u5b57\u6570\uff1a3000\u5b57", None))
        self.totalWordsLabel.setText(QCoreApplication.translate("NovelGeneratorWindow", u"\u603b\u5b57\u6570\uff1a15000\u5b57", None))
        self.mainCharacterCountLabel.setText(QCoreApplication.translate("NovelGeneratorWindow", u"\u4e3b\u8981\u4eba\u7269\u6570\u91cf\uff1a3\u4eba", None))
        self.supportCharacterCountLabel.setText(QCoreApplication.translate("NovelGeneratorWindow", u"\u6b21\u8981\u4eba\u7269\u6570\u91cf\uff1a5\u4eba", None))
        self.enableTranslation.setText(QCoreApplication.translate("NovelGeneratorWindow", u"\u542f\u7528\u7ffb\u8bd1\u548c\u6587\u5316\u9002\u5e94", None))
        self.generateBtn.setText(QCoreApplication.translate("NovelGeneratorWindow", u"\u751f\u6210\u5927\u7eb2", None))
        self.expandBtn.setText(QCoreApplication.translate("NovelGeneratorWindow", u"\u6269\u5199\u5185\u5bb9", None))
        self.translateBtn.setText(QCoreApplication.translate("NovelGeneratorWindow", u"\u7ffb\u8bd1\u5185\u5bb9", None))
        self.outlineEdit.setPlaceholderText(QCoreApplication.translate("NovelGeneratorWindow", u"\u8fd9\u91cc\u5c06\u663e\u793a\u751f\u6210\u7684\u5927\u7eb2...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.outlineTab), QCoreApplication.translate("NovelGeneratorWindow", u"\u5927\u7eb2", None))
        self.expandedEdit.setPlaceholderText(QCoreApplication.translate("NovelGeneratorWindow", u"\u8fd9\u91cc\u5c06\u663e\u793a\u6269\u5199\u7684\u5185\u5bb9...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.expandedTab), QCoreApplication.translate("NovelGeneratorWindow", u"\u6269\u5199", None))
    # retranslateUi

