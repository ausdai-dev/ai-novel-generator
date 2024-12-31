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
    QWidget, QSplitter)

class Ui_NovelGeneratorWindow(object):
    def setupUi(self, NovelGeneratorWindow):
        if not NovelGeneratorWindow.objectName():
            NovelGeneratorWindow.setObjectName(u"NovelGeneratorWindow")
        NovelGeneratorWindow.resize(1200, 800)
        
        # 创建中央部件
        self.centralwidget = QWidget(NovelGeneratorWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        # 创建主布局
        self.mainLayout = QHBoxLayout(self.centralwidget)
        
        # 创建设置组
        self.settingsGroup = QGroupBox("设置")
        self.settingsLayout = QVBoxLayout(self.settingsGroup)
        
        # 添加各种控件到设置组
        self.nameLabel = QLabel("小说名称：")
        self.settingsLayout.addWidget(self.nameLabel)
        
        self.nameEdit = QLineEdit()
        self.settingsLayout.addWidget(self.nameEdit)
        
        self.synopsisLabel = QLabel("故事梗概：")
        self.settingsLayout.addWidget(self.synopsisLabel)
        
        self.synopsisEdit = QTextEdit()
        self.synopsisEdit.setMaximumHeight(100)
        self.settingsLayout.addWidget(self.synopsisEdit)
        
        self.genreLabel = QLabel("小说类型：")
        self.settingsLayout.addWidget(self.genreLabel)
        
        self.genreCombo = QComboBox()
        self.settingsLayout.addWidget(self.genreCombo)
        
        self.styleLabel = QLabel("写作风格：")
        self.settingsLayout.addWidget(self.styleLabel)
        
        self.styleCombo = QComboBox()
        self.settingsLayout.addWidget(self.styleCombo)
        
        self.cultureLabel = QLabel("文化背景：")
        self.settingsLayout.addWidget(self.cultureLabel)
        
        self.cultureCombo = QComboBox()
        self.settingsLayout.addWidget(self.cultureCombo)
        
        self.chapterCountLabel = QLabel("章节数量：5章")
        self.settingsLayout.addWidget(self.chapterCountLabel)
        
        self.chapterCountSlider = QSlider(Qt.Horizontal)
        self.chapterCountSlider.setMinimum(2)
        self.chapterCountSlider.setMaximum(20)
        self.chapterCountSlider.setValue(5)
        self.settingsLayout.addWidget(self.chapterCountSlider)
        
        self.avgChapterWordsLabel = QLabel("每章平均字数：3000字")
        self.settingsLayout.addWidget(self.avgChapterWordsLabel)
        
        self.avgChapterWordsSlider = QSlider(Qt.Horizontal)
        self.avgChapterWordsSlider.setMinimum(1000)
        self.avgChapterWordsSlider.setMaximum(10000)
        self.avgChapterWordsSlider.setSingleStep(100)
        self.avgChapterWordsSlider.setValue(3000)
        self.settingsLayout.addWidget(self.avgChapterWordsSlider)
        
        self.totalWordsLabel = QLabel("总字数：15000字")
        self.settingsLayout.addWidget(self.totalWordsLabel)
        
        self.mainCharacterCountLabel = QLabel("主要人物数量：3人")
        self.settingsLayout.addWidget(self.mainCharacterCountLabel)
        
        self.mainCharacterCountSlider = QSlider(Qt.Horizontal)
        self.mainCharacterCountSlider.setMinimum(1)
        self.mainCharacterCountSlider.setMaximum(10)
        self.mainCharacterCountSlider.setValue(3)
        self.settingsLayout.addWidget(self.mainCharacterCountSlider)
        
        self.supportCharacterCountLabel = QLabel("次要人物数量：5人")
        self.settingsLayout.addWidget(self.supportCharacterCountLabel)
        
        self.supportCharacterCountSlider = QSlider(Qt.Horizontal)
        self.supportCharacterCountSlider.setMinimum(0)
        self.supportCharacterCountSlider.setMaximum(20)
        self.supportCharacterCountSlider.setValue(5)
        self.settingsLayout.addWidget(self.supportCharacterCountSlider)
        
        self.enableTranslation = QCheckBox("启用翻译和文化适应")
        self.settingsLayout.addWidget(self.enableTranslation)
        
        self.generateBtn = QPushButton("生成大纲")
        self.settingsLayout.addWidget(self.generateBtn)
        
        self.expandBtn = QPushButton("扩写内容")
        self.settingsLayout.addWidget(self.expandBtn)
        
        self.translateBtn = QPushButton("翻译内容")
        self.translateBtn.setEnabled(False)
        self.settingsLayout.addWidget(self.translateBtn)
        
        # 添加弹簧
        self.settingsLayout.addStretch()
        
        # 创建标签页组件
        self.tabWidget = QTabWidget()
        
        # 创建大纲标签页
        self.outlineTab = QWidget()
        outlineLayout = QVBoxLayout(self.outlineTab)
        self.outlineEdit = QTextEdit()
        outlineLayout.addWidget(self.outlineEdit)
        self.tabWidget.addTab(self.outlineTab, "大纲")
        
        # 创建扩写标签页
        self.expandedTab = QWidget()
        expandedLayout = QVBoxLayout(self.expandedTab)
        self.expandedEdit = QTextEdit()
        expandedLayout.addWidget(self.expandedEdit)
        self.tabWidget.addTab(self.expandedTab, "扩写")
        
        # 创建分割器并添加组件
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.settingsGroup)
        self.splitter.addWidget(self.tabWidget)
        
        # 设置分割比例
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)
        
        # 将分割器添加到主布局
        self.mainLayout.addWidget(self.splitter)
        
        # 设置中央部件
        NovelGeneratorWindow.setCentralWidget(self.centralwidget)
        
        # 创建状态栏
        self.statusbar = QStatusBar(NovelGeneratorWindow)
        NovelGeneratorWindow.setStatusBar(self.statusbar)
        
        # 设置默认标签页
        self.tabWidget.setCurrentIndex(0)
        
        # 设置占位符文本
        self.nameEdit.setPlaceholderText("输入小说名称（可选）")
        self.synopsisEdit.setPlaceholderText("输入故事梗概（可选）")
        self.outlineEdit.setPlaceholderText("这里将显示生成的大纲...")
        self.expandedEdit.setPlaceholderText("这里将显示扩写的内容...")
        
        # 连接信号和槽
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

