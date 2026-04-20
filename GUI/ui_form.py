# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFormLayout, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_RL_Strategy_GUI(object):
    def setupUi(self, RL_Strategy_GUI):
        if not RL_Strategy_GUI.objectName():
            RL_Strategy_GUI.setObjectName(u"RL_Strategy_GUI")
        RL_Strategy_GUI.resize(1257, 972)
        font = QFont()
        font.setFamilies([u"Unity Sans TT"])
        RL_Strategy_GUI.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(RL_Strategy_GUI)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetMaximumSize)
        self.lbl_ImperialLogo = QLabel(RL_Strategy_GUI)
        self.lbl_ImperialLogo.setObjectName(u"lbl_ImperialLogo")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_ImperialLogo.sizePolicy().hasHeightForWidth())
        self.lbl_ImperialLogo.setSizePolicy(sizePolicy)
        self.lbl_ImperialLogo.setMinimumSize(QSize(188, 50))
        self.lbl_ImperialLogo.setMaximumSize(QSize(188, 50))
        font1 = QFont()
        font1.setFamilies([u"Unity Sans TT"])
        font1.setPointSize(32)
        self.lbl_ImperialLogo.setFont(font1)
        self.lbl_ImperialLogo.setScaledContents(True)
        self.lbl_ImperialLogo.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.lbl_ImperialLogo)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.lbl_MercedesLogo = QLabel(RL_Strategy_GUI)
        self.lbl_MercedesLogo.setObjectName(u"lbl_MercedesLogo")
        sizePolicy.setHeightForWidth(self.lbl_MercedesLogo.sizePolicy().hasHeightForWidth())
        self.lbl_MercedesLogo.setSizePolicy(sizePolicy)
        self.lbl_MercedesLogo.setMinimumSize(QSize(160, 50))
        self.lbl_MercedesLogo.setMaximumSize(QSize(160, 50))
        self.lbl_MercedesLogo.setFont(font1)
        self.lbl_MercedesLogo.setScaledContents(True)
        self.lbl_MercedesLogo.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.lbl_MercedesLogo)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.tabW_TrainDeploy = QTabWidget(RL_Strategy_GUI)
        self.tabW_TrainDeploy.setObjectName(u"tabW_TrainDeploy")
        self.tab_Train = QWidget()
        self.tab_Train.setObjectName(u"tab_Train")
        self.horizontalLayout_3 = QHBoxLayout(self.tab_Train)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tabW_Train = QTabWidget(self.tab_Train)
        self.tabW_Train.setObjectName(u"tabW_Train")
        self.tab_TrainModel = QWidget()
        self.tab_TrainModel.setObjectName(u"tab_TrainModel")
        self.horizontalLayout_6 = QHBoxLayout(self.tab_TrainModel)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setRowWrapPolicy(QFormLayout.WrapLongRows)
        self.lbl_NumEpisodes = QLabel(self.tab_TrainModel)
        self.lbl_NumEpisodes.setObjectName(u"lbl_NumEpisodes")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lbl_NumEpisodes)

        self.lbl_Seed = QLabel(self.tab_TrainModel)
        self.lbl_Seed.setObjectName(u"lbl_Seed")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lbl_Seed)

        self.lbl_FixedSeed = QLabel(self.tab_TrainModel)
        self.lbl_FixedSeed.setObjectName(u"lbl_FixedSeed")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lbl_FixedSeed)

        self.lbl_StepSize = QLabel(self.tab_TrainModel)
        self.lbl_StepSize.setObjectName(u"lbl_StepSize")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.lbl_StepSize)

        self.box_FixedSeed = QCheckBox(self.tab_TrainModel)
        self.box_FixedSeed.setObjectName(u"box_FixedSeed")
        self.box_FixedSeed.setMinimumSize(QSize(150, 0))

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.box_FixedSeed)

        self.dsb_StepSize = QDoubleSpinBox(self.tab_TrainModel)
        self.dsb_StepSize.setObjectName(u"dsb_StepSize")
        self.dsb_StepSize.setMinimumSize(QSize(150, 0))
        self.dsb_StepSize.setSingleStep(0.010000000000000)
        self.dsb_StepSize.setValue(1.000000000000000)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.dsb_StepSize)

        self.lbl_Epsilon = QLabel(self.tab_TrainModel)
        self.lbl_Epsilon.setObjectName(u"lbl_Epsilon")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.lbl_Epsilon)

        self.dsb_Epsilon = QDoubleSpinBox(self.tab_TrainModel)
        self.dsb_Epsilon.setObjectName(u"dsb_Epsilon")
        self.dsb_Epsilon.setMinimumSize(QSize(150, 0))
        self.dsb_Epsilon.setDecimals(3)
        self.dsb_Epsilon.setMaximum(1.000000000000000)
        self.dsb_Epsilon.setSingleStep(0.010000000000000)
        self.dsb_Epsilon.setValue(1.000000000000000)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.dsb_Epsilon)

        self.dsb_NumEpisodes = QDoubleSpinBox(self.tab_TrainModel)
        self.dsb_NumEpisodes.setObjectName(u"dsb_NumEpisodes")
        self.dsb_NumEpisodes.setMinimumSize(QSize(150, 0))
        self.dsb_NumEpisodes.setDecimals(0)
        self.dsb_NumEpisodes.setMaximum(1000000.000000000000000)
        self.dsb_NumEpisodes.setSingleStep(10.000000000000000)
        self.dsb_NumEpisodes.setValue(10.000000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.dsb_NumEpisodes)

        self.dsb_Seed = QDoubleSpinBox(self.tab_TrainModel)
        self.dsb_Seed.setObjectName(u"dsb_Seed")
        self.dsb_Seed.setMinimumSize(QSize(150, 0))
        self.dsb_Seed.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.dsb_Seed.setDecimals(0)
        self.dsb_Seed.setMaximum(1000000.000000000000000)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.dsb_Seed)

        self.lbl_EpsilonDecay = QLabel(self.tab_TrainModel)
        self.lbl_EpsilonDecay.setObjectName(u"lbl_EpsilonDecay")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.lbl_EpsilonDecay)

        self.dsb_EpsilonDecay = QDoubleSpinBox(self.tab_TrainModel)
        self.dsb_EpsilonDecay.setObjectName(u"dsb_EpsilonDecay")
        self.dsb_EpsilonDecay.setMinimumSize(QSize(150, 0))
        self.dsb_EpsilonDecay.setDecimals(3)
        self.dsb_EpsilonDecay.setMaximum(1.000000000000000)
        self.dsb_EpsilonDecay.setSingleStep(0.010000000000000)
        self.dsb_EpsilonDecay.setValue(0.990000000000000)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.dsb_EpsilonDecay)

        self.lbl_MinEpsilon = QLabel(self.tab_TrainModel)
        self.lbl_MinEpsilon.setObjectName(u"lbl_MinEpsilon")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.lbl_MinEpsilon)

        self.dsb_MinEpsilon = QDoubleSpinBox(self.tab_TrainModel)
        self.dsb_MinEpsilon.setObjectName(u"dsb_MinEpsilon")
        self.dsb_MinEpsilon.setMinimumSize(QSize(150, 0))
        self.dsb_MinEpsilon.setDecimals(3)
        self.dsb_MinEpsilon.setMaximum(1.000000000000000)
        self.dsb_MinEpsilon.setSingleStep(0.010000000000000)
        self.dsb_MinEpsilon.setValue(0.100000000000000)

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.dsb_MinEpsilon)

        self.lbl_Gamma = QLabel(self.tab_TrainModel)
        self.lbl_Gamma.setObjectName(u"lbl_Gamma")

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.lbl_Gamma)

        self.dsb_Gamma = QDoubleSpinBox(self.tab_TrainModel)
        self.dsb_Gamma.setObjectName(u"dsb_Gamma")
        self.dsb_Gamma.setMinimumSize(QSize(150, 0))
        self.dsb_Gamma.setDecimals(3)
        self.dsb_Gamma.setSingleStep(0.010000000000000)
        self.dsb_Gamma.setValue(0.990000000000000)

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.dsb_Gamma)

        self.lbl_LearningRate = QLabel(self.tab_TrainModel)
        self.lbl_LearningRate.setObjectName(u"lbl_LearningRate")

        self.formLayout.setWidget(11, QFormLayout.LabelRole, self.lbl_LearningRate)

        self.dsb_LearningRate = QDoubleSpinBox(self.tab_TrainModel)
        self.dsb_LearningRate.setObjectName(u"dsb_LearningRate")
        self.dsb_LearningRate.setMinimumSize(QSize(150, 0))
        self.dsb_LearningRate.setDecimals(3)
        self.dsb_LearningRate.setMaximum(1.000000000000000)
        self.dsb_LearningRate.setSingleStep(0.001000000000000)
        self.dsb_LearningRate.setValue(0.001000000000000)

        self.formLayout.setWidget(11, QFormLayout.FieldRole, self.dsb_LearningRate)

        self.lbl_WeightDecay = QLabel(self.tab_TrainModel)
        self.lbl_WeightDecay.setObjectName(u"lbl_WeightDecay")

        self.formLayout.setWidget(12, QFormLayout.LabelRole, self.lbl_WeightDecay)

        self.dsb_WeightDecay = QDoubleSpinBox(self.tab_TrainModel)
        self.dsb_WeightDecay.setObjectName(u"dsb_WeightDecay")
        self.dsb_WeightDecay.setMinimumSize(QSize(150, 0))
        self.dsb_WeightDecay.setDecimals(3)

        self.formLayout.setWidget(12, QFormLayout.FieldRole, self.dsb_WeightDecay)

        self.lbl_ReplayBufferSize = QLabel(self.tab_TrainModel)
        self.lbl_ReplayBufferSize.setObjectName(u"lbl_ReplayBufferSize")

        self.formLayout.setWidget(13, QFormLayout.LabelRole, self.lbl_ReplayBufferSize)

        self.dsb_ReplayBufferSize = QDoubleSpinBox(self.tab_TrainModel)
        self.dsb_ReplayBufferSize.setObjectName(u"dsb_ReplayBufferSize")
        self.dsb_ReplayBufferSize.setMinimumSize(QSize(150, 0))
        self.dsb_ReplayBufferSize.setDecimals(0)
        self.dsb_ReplayBufferSize.setMaximum(1000000.000000000000000)
        self.dsb_ReplayBufferSize.setValue(10000.000000000000000)

        self.formLayout.setWidget(13, QFormLayout.FieldRole, self.dsb_ReplayBufferSize)

        self.lbl_ReplayBufferSampleSize = QLabel(self.tab_TrainModel)
        self.lbl_ReplayBufferSampleSize.setObjectName(u"lbl_ReplayBufferSampleSize")

        self.formLayout.setWidget(14, QFormLayout.LabelRole, self.lbl_ReplayBufferSampleSize)

        self.dsb_ReplayBufferSampleSize = QDoubleSpinBox(self.tab_TrainModel)
        self.dsb_ReplayBufferSampleSize.setObjectName(u"dsb_ReplayBufferSampleSize")
        self.dsb_ReplayBufferSampleSize.setMinimumSize(QSize(150, 0))
        self.dsb_ReplayBufferSampleSize.setDecimals(0)
        self.dsb_ReplayBufferSampleSize.setMaximum(1000000.000000000000000)
        self.dsb_ReplayBufferSampleSize.setValue(50.000000000000000)

        self.formLayout.setWidget(14, QFormLayout.FieldRole, self.dsb_ReplayBufferSampleSize)

        self.lbl_EpisodesUpdateTargetNetwork = QLabel(self.tab_TrainModel)
        self.lbl_EpisodesUpdateTargetNetwork.setObjectName(u"lbl_EpisodesUpdateTargetNetwork")

        self.formLayout.setWidget(15, QFormLayout.LabelRole, self.lbl_EpisodesUpdateTargetNetwork)

        self.dsb_EpisodesUpdateTargetNetwork = QDoubleSpinBox(self.tab_TrainModel)
        self.dsb_EpisodesUpdateTargetNetwork.setObjectName(u"dsb_EpisodesUpdateTargetNetwork")
        self.dsb_EpisodesUpdateTargetNetwork.setMinimumSize(QSize(150, 0))
        self.dsb_EpisodesUpdateTargetNetwork.setDecimals(0)
        self.dsb_EpisodesUpdateTargetNetwork.setMaximum(1000000.000000000000000)
        self.dsb_EpisodesUpdateTargetNetwork.setValue(10.000000000000000)

        self.formLayout.setWidget(15, QFormLayout.FieldRole, self.dsb_EpisodesUpdateTargetNetwork)

        self.cb_RewardFunction = QComboBox(self.tab_TrainModel)
        self.cb_RewardFunction.addItem("")
        self.cb_RewardFunction.setObjectName(u"cb_RewardFunction")
        self.cb_RewardFunction.setMinimumSize(QSize(150, 0))

        self.formLayout.setWidget(16, QFormLayout.FieldRole, self.cb_RewardFunction)

        self.lbl_NumEpisodes_2 = QLabel(self.tab_TrainModel)
        self.lbl_NumEpisodes_2.setObjectName(u"lbl_NumEpisodes_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lbl_NumEpisodes_2)

        self.cb_SelectedDriver = QComboBox(self.tab_TrainModel)
        self.cb_SelectedDriver.addItem("")
        self.cb_SelectedDriver.addItem("")
        self.cb_SelectedDriver.setObjectName(u"cb_SelectedDriver")
        self.cb_SelectedDriver.setMinimumSize(QSize(150, 0))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.cb_SelectedDriver)

        self.lbl_ModelName = QLabel(self.tab_TrainModel)
        self.lbl_ModelName.setObjectName(u"lbl_ModelName")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lbl_ModelName)

        self.le_ModelName = QLineEdit(self.tab_TrainModel)
        self.le_ModelName.setObjectName(u"le_ModelName")
        self.le_ModelName.setMinimumSize(QSize(150, 0))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.le_ModelName)

        self.lbl_DisableSC = QLabel(self.tab_TrainModel)
        self.lbl_DisableSC.setObjectName(u"lbl_DisableSC")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.lbl_DisableSC)

        self.box_DisableSC = QCheckBox(self.tab_TrainModel)
        self.box_DisableSC.setObjectName(u"box_DisableSC")
        self.box_DisableSC.setMinimumSize(QSize(150, 0))

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.box_DisableSC)

        self.lbl_RewardFunction = QLabel(self.tab_TrainModel)
        self.lbl_RewardFunction.setObjectName(u"lbl_RewardFunction")

        self.formLayout.setWidget(16, QFormLayout.LabelRole, self.lbl_RewardFunction)


        self.horizontalLayout_6.addLayout(self.formLayout)

        self.te_ConsoleLog = QTextEdit(self.tab_TrainModel)
        self.te_ConsoleLog.setObjectName(u"te_ConsoleLog")
        self.te_ConsoleLog.setReadOnly(True)

        self.horizontalLayout_6.addWidget(self.te_ConsoleLog)

        self.horizontalLayout_6.setStretch(1, 1)
        self.tabW_Train.addTab(self.tab_TrainModel, "")
        self.tab_TrainDecisionTree = QWidget()
        self.tab_TrainDecisionTree.setObjectName(u"tab_TrainDecisionTree")
        self.horizontalLayout_9 = QHBoxLayout(self.tab_TrainDecisionTree)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.formLayout_6 = QFormLayout()
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.label_11 = QLabel(self.tab_TrainDecisionTree)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_6.setWidget(0, QFormLayout.LabelRole, self.label_11)

        self.label_20 = QLabel(self.tab_TrainDecisionTree)
        self.label_20.setObjectName(u"label_20")

        self.formLayout_6.setWidget(1, QFormLayout.LabelRole, self.label_20)

        self.label_21 = QLabel(self.tab_TrainDecisionTree)
        self.label_21.setObjectName(u"label_21")

        self.formLayout_6.setWidget(2, QFormLayout.LabelRole, self.label_21)

        self.label_22 = QLabel(self.tab_TrainDecisionTree)
        self.label_22.setObjectName(u"label_22")

        self.formLayout_6.setWidget(3, QFormLayout.LabelRole, self.label_22)

        self.label_23 = QLabel(self.tab_TrainDecisionTree)
        self.label_23.setObjectName(u"label_23")

        self.formLayout_6.setWidget(4, QFormLayout.LabelRole, self.label_23)

        self.label_24 = QLabel(self.tab_TrainDecisionTree)
        self.label_24.setObjectName(u"label_24")

        self.formLayout_6.setWidget(5, QFormLayout.LabelRole, self.label_24)

        self.sb_MaxDepth = QSpinBox(self.tab_TrainDecisionTree)
        self.sb_MaxDepth.setObjectName(u"sb_MaxDepth")
        self.sb_MaxDepth.setMinimumSize(QSize(75, 0))

        self.formLayout_6.setWidget(0, QFormLayout.FieldRole, self.sb_MaxDepth)

        self.sb_MaxIterations = QSpinBox(self.tab_TrainDecisionTree)
        self.sb_MaxIterations.setObjectName(u"sb_MaxIterations")
        self.sb_MaxIterations.setMinimumSize(QSize(75, 0))

        self.formLayout_6.setWidget(1, QFormLayout.FieldRole, self.sb_MaxIterations)

        self.sb_MaxSamples = QSpinBox(self.tab_TrainDecisionTree)
        self.sb_MaxSamples.setObjectName(u"sb_MaxSamples")
        self.sb_MaxSamples.setMinimumSize(QSize(75, 0))

        self.formLayout_6.setWidget(2, QFormLayout.FieldRole, self.sb_MaxSamples)

        self.box_ReweightSamples = QCheckBox(self.tab_TrainDecisionTree)
        self.box_ReweightSamples.setObjectName(u"box_ReweightSamples")
        self.box_ReweightSamples.setMinimumSize(QSize(75, 0))

        self.formLayout_6.setWidget(3, QFormLayout.FieldRole, self.box_ReweightSamples)

        self.sb_BatchRollouts = QSpinBox(self.tab_TrainDecisionTree)
        self.sb_BatchRollouts.setObjectName(u"sb_BatchRollouts")
        self.sb_BatchRollouts.setMinimumSize(QSize(75, 0))

        self.formLayout_6.setWidget(4, QFormLayout.FieldRole, self.sb_BatchRollouts)

        self.sb_TestRollouts = QSpinBox(self.tab_TrainDecisionTree)
        self.sb_TestRollouts.setObjectName(u"sb_TestRollouts")
        self.sb_TestRollouts.setMinimumSize(QSize(75, 0))

        self.formLayout_6.setWidget(5, QFormLayout.FieldRole, self.sb_TestRollouts)


        self.horizontalLayout_9.addLayout(self.formLayout_6)

        self.te_DecisionTreeConsoleLog = QTextEdit(self.tab_TrainDecisionTree)
        self.te_DecisionTreeConsoleLog.setObjectName(u"te_DecisionTreeConsoleLog")
        self.te_DecisionTreeConsoleLog.setReadOnly(True)

        self.horizontalLayout_9.addWidget(self.te_DecisionTreeConsoleLog)

        self.horizontalLayout_9.setStretch(1, 1)
        self.tabW_Train.addTab(self.tab_TrainDecisionTree, "")

        self.horizontalLayout_3.addWidget(self.tabW_Train)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_StartTraining = QPushButton(self.tab_Train)
        self.btn_StartTraining.setObjectName(u"btn_StartTraining")

        self.verticalLayout.addWidget(self.btn_StartTraining)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btn_SaveModel = QPushButton(self.tab_Train)
        self.btn_SaveModel.setObjectName(u"btn_SaveModel")

        self.verticalLayout.addWidget(self.btn_SaveModel)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.tabW_TrainDeploy.addTab(self.tab_Train, "")
        self.tab_Deploy = QWidget()
        self.tab_Deploy.setObjectName(u"tab_Deploy")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tab_Deploy.sizePolicy().hasHeightForWidth())
        self.tab_Deploy.setSizePolicy(sizePolicy1)
        self.verticalLayout_5 = QVBoxLayout(self.tab_Deploy)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lbl_LoadedModel = QLabel(self.tab_Deploy)
        self.lbl_LoadedModel.setObjectName(u"lbl_LoadedModel")
        font2 = QFont()
        font2.setFamilies([u"Unity Sans TT"])
        font2.setPointSize(28)
        self.lbl_LoadedModel.setFont(font2)

        self.horizontalLayout.addWidget(self.lbl_LoadedModel, 0, Qt.AlignHCenter)

        self.btn_LoadModel = QPushButton(self.tab_Deploy)
        self.btn_LoadModel.setObjectName(u"btn_LoadModel")

        self.horizontalLayout.addWidget(self.btn_LoadModel)

        self.cb_DataSource = QComboBox(self.tab_Deploy)
        self.cb_DataSource.addItem("")
        self.cb_DataSource.addItem("")
        self.cb_DataSource.addItem("")
        self.cb_DataSource.addItem("")
        self.cb_DataSource.setObjectName(u"cb_DataSource")
        self.cb_DataSource.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.cb_DataSource)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFormAlignment(Qt.AlignCenter)
        self.lbl_IPAddress = QLabel(self.tab_Deploy)
        self.lbl_IPAddress.setObjectName(u"lbl_IPAddress")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.lbl_IPAddress)

        self.le_IPAddress = QLineEdit(self.tab_Deploy)
        self.le_IPAddress.setObjectName(u"le_IPAddress")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.le_IPAddress)

        self.lbl_Port = QLabel(self.tab_Deploy)
        self.lbl_Port.setObjectName(u"lbl_Port")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.lbl_Port)

        self.sb_Port = QSpinBox(self.tab_Deploy)
        self.sb_Port.setObjectName(u"sb_Port")
        self.sb_Port.setMaximum(65535)
        self.sb_Port.setValue(20789)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.sb_Port)

        self.btn_StartStop = QPushButton(self.tab_Deploy)
        self.btn_StartStop.setObjectName(u"btn_StartStop")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.btn_StartStop)

        self.lbl_RunStatus = QLabel(self.tab_Deploy)
        self.lbl_RunStatus.setObjectName(u"lbl_RunStatus")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.lbl_RunStatus)

        self.label_38 = QLabel(self.tab_Deploy)
        self.label_38.setObjectName(u"label_38")
        font3 = QFont()
        font3.setFamilies([u"Unity Sans TT"])
        font3.setPointSize(15)
        font3.setBold(True)
        self.label_38.setFont(font3)
        self.label_38.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(0, QFormLayout.SpanningRole, self.label_38)


        self.horizontalLayout_4.addLayout(self.formLayout_2)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lbl_DTPrediction = QLabel(self.tab_Deploy)
        self.lbl_DTPrediction.setObjectName(u"lbl_DTPrediction")
        font4 = QFont()
        font4.setFamilies([u"Unity Sans TT"])
        font4.setPointSize(50)
        font4.setBold(False)
        self.lbl_DTPrediction.setFont(font4)
        self.lbl_DTPrediction.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lbl_DTPrediction, 1, 1, 1, 1)

        self.lbl_ModelPrediction = QLabel(self.tab_Deploy)
        self.lbl_ModelPrediction.setObjectName(u"lbl_ModelPrediction")
        font5 = QFont()
        font5.setFamilies([u"Unity Sans TT"])
        font5.setPointSize(50)
        self.lbl_ModelPrediction.setFont(font5)
        self.lbl_ModelPrediction.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lbl_ModelPrediction, 1, 0, 1, 1)

        self.label_42 = QLabel(self.tab_Deploy)
        self.label_42.setObjectName(u"label_42")
        font6 = QFont()
        font6.setFamilies([u"Unity Sans TT"])
        font6.setPointSize(18)
        font6.setBold(True)
        self.label_42.setFont(font6)
        self.label_42.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_42, 0, 0, 1, 1)

        self.lbl_DTPredTitle = QLabel(self.tab_Deploy)
        self.lbl_DTPredTitle.setObjectName(u"lbl_DTPredTitle")
        self.lbl_DTPredTitle.setEnabled(True)
        self.lbl_DTPredTitle.setFont(font6)
        self.lbl_DTPredTitle.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lbl_DTPredTitle, 0, 1, 1, 1)

        self.gridLayout_3.setRowStretch(1, 1)

        self.horizontalLayout_4.addLayout(self.gridLayout_3)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.cb_RaceSelect = QComboBox(self.tab_Deploy)
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.addItem("")
        self.cb_RaceSelect.setObjectName(u"cb_RaceSelect")
        self.cb_RaceSelect.setEnabled(False)
        self.cb_RaceSelect.setMinimumSize(QSize(150, 0))
        self.cb_RaceSelect.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout.addWidget(self.cb_RaceSelect, 1, 4, 1, 1)

        self.btn_PitHard = QPushButton(self.tab_Deploy)
        self.btn_PitHard.setObjectName(u"btn_PitHard")
        self.btn_PitHard.setEnabled(False)

        self.gridLayout.addWidget(self.btn_PitHard, 2, 1, 1, 1)

        self.btn_PitSoft = QPushButton(self.tab_Deploy)
        self.btn_PitSoft.setObjectName(u"btn_PitSoft")
        self.btn_PitSoft.setEnabled(False)

        self.gridLayout.addWidget(self.btn_PitSoft, 2, 0, 1, 1)

        self.btn_StepModel = QPushButton(self.tab_Deploy)
        self.btn_StepModel.setObjectName(u"btn_StepModel")
        self.btn_StepModel.setEnabled(False)

        self.gridLayout.addWidget(self.btn_StepModel, 1, 2, 1, 1)

        self.btn_NoPit = QPushButton(self.tab_Deploy)
        self.btn_NoPit.setObjectName(u"btn_NoPit")
        self.btn_NoPit.setEnabled(False)

        self.gridLayout.addWidget(self.btn_NoPit, 1, 0, 1, 1)

        self.cb_YearSelect = QComboBox(self.tab_Deploy)
        self.cb_YearSelect.addItem("")
        self.cb_YearSelect.addItem("")
        self.cb_YearSelect.addItem("")
        self.cb_YearSelect.setObjectName(u"cb_YearSelect")
        self.cb_YearSelect.setEnabled(False)

        self.gridLayout.addWidget(self.cb_YearSelect, 2, 4, 1, 1)

        self.btn_PitMedium = QPushButton(self.tab_Deploy)
        self.btn_PitMedium.setObjectName(u"btn_PitMedium")
        self.btn_PitMedium.setEnabled(False)

        self.gridLayout.addWidget(self.btn_PitMedium, 1, 1, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_3 = QLabel(self.tab_Deploy)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_3)

        self.sb_Seed = QSpinBox(self.tab_Deploy)
        self.sb_Seed.setObjectName(u"sb_Seed")
        self.sb_Seed.setEnabled(False)

        self.horizontalLayout_11.addWidget(self.sb_Seed)


        self.gridLayout.addLayout(self.horizontalLayout_11, 1, 3, 1, 1)

        self.btn_ResetSimulation = QPushButton(self.tab_Deploy)
        self.btn_ResetSimulation.setObjectName(u"btn_ResetSimulation")
        self.btn_ResetSimulation.setEnabled(False)

        self.gridLayout.addWidget(self.btn_ResetSimulation, 2, 3, 1, 1)

        self.btn_StepDecisionTree = QPushButton(self.tab_Deploy)
        self.btn_StepDecisionTree.setObjectName(u"btn_StepDecisionTree")
        self.btn_StepDecisionTree.setEnabled(False)

        self.gridLayout.addWidget(self.btn_StepDecisionTree, 2, 2, 1, 1)

        self.label_34 = QLabel(self.tab_Deploy)
        self.label_34.setObjectName(u"label_34")
        font7 = QFont()
        font7.setFamilies([u"Unity Sans TT"])
        font7.setPointSize(15)
        font7.setBold(True)
        font7.setUnderline(False)
        self.label_34.setFont(font7)
        self.label_34.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_34, 0, 0, 1, 2)

        self.label_35 = QLabel(self.tab_Deploy)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setFont(font7)
        self.label_35.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_35, 0, 2, 1, 1)

        self.label_36 = QLabel(self.tab_Deploy)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setFont(font7)
        self.label_36.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_36, 0, 3, 1, 2)


        self.horizontalLayout_4.addLayout(self.gridLayout)

        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.formLayout_5 = QFormLayout()
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.label_4 = QLabel(self.tab_Deploy)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.lbl_StatePosition = QLabel(self.tab_Deploy)
        self.lbl_StatePosition.setObjectName(u"lbl_StatePosition")
        self.lbl_StatePosition.setMinimumSize(QSize(200, 0))
        self.lbl_StatePosition.setFont(font5)
        self.lbl_StatePosition.setAlignment(Qt.AlignCenter)

        self.formLayout_5.setWidget(0, QFormLayout.FieldRole, self.lbl_StatePosition)

        self.label_12 = QLabel(self.tab_Deploy)
        self.label_12.setObjectName(u"label_12")
        sizePolicy2.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy2)

        self.formLayout_5.setWidget(1, QFormLayout.LabelRole, self.label_12)

        self.lbl_StateSafetyCarStatus = QLabel(self.tab_Deploy)
        self.lbl_StateSafetyCarStatus.setObjectName(u"lbl_StateSafetyCarStatus")
        self.lbl_StateSafetyCarStatus.setMinimumSize(QSize(200, 0))
        self.lbl_StateSafetyCarStatus.setFont(font5)
        self.lbl_StateSafetyCarStatus.setAlignment(Qt.AlignCenter)

        self.formLayout_5.setWidget(1, QFormLayout.FieldRole, self.lbl_StateSafetyCarStatus)

        self.label_13 = QLabel(self.tab_Deploy)
        self.label_13.setObjectName(u"label_13")
        sizePolicy2.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy2)

        self.formLayout_5.setWidget(2, QFormLayout.LabelRole, self.label_13)

        self.lbl_StateLapNumber = QLabel(self.tab_Deploy)
        self.lbl_StateLapNumber.setObjectName(u"lbl_StateLapNumber")
        self.lbl_StateLapNumber.setMinimumSize(QSize(200, 0))
        self.lbl_StateLapNumber.setFont(font5)
        self.lbl_StateLapNumber.setAlignment(Qt.AlignCenter)

        self.formLayout_5.setWidget(2, QFormLayout.FieldRole, self.lbl_StateLapNumber)

        self.label_14 = QLabel(self.tab_Deploy)
        self.label_14.setObjectName(u"label_14")
        sizePolicy2.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy2)

        self.formLayout_5.setWidget(3, QFormLayout.LabelRole, self.label_14)

        self.lbl_StateCurrentTyre = QLabel(self.tab_Deploy)
        self.lbl_StateCurrentTyre.setObjectName(u"lbl_StateCurrentTyre")
        self.lbl_StateCurrentTyre.setMinimumSize(QSize(200, 0))
        self.lbl_StateCurrentTyre.setFont(font5)
        self.lbl_StateCurrentTyre.setAlignment(Qt.AlignCenter)

        self.formLayout_5.setWidget(3, QFormLayout.FieldRole, self.lbl_StateCurrentTyre)

        self.label_15 = QLabel(self.tab_Deploy)
        self.label_15.setObjectName(u"label_15")
        sizePolicy2.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy2)

        self.formLayout_5.setWidget(4, QFormLayout.LabelRole, self.label_15)

        self.lbl_StateTyreDegradation = QLabel(self.tab_Deploy)
        self.lbl_StateTyreDegradation.setObjectName(u"lbl_StateTyreDegradation")
        self.lbl_StateTyreDegradation.setMinimumSize(QSize(200, 0))
        self.lbl_StateTyreDegradation.setFont(font5)
        self.lbl_StateTyreDegradation.setAlignment(Qt.AlignCenter)

        self.formLayout_5.setWidget(4, QFormLayout.FieldRole, self.lbl_StateTyreDegradation)

        self.label_16 = QLabel(self.tab_Deploy)
        self.label_16.setObjectName(u"label_16")
        sizePolicy2.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy2)

        self.formLayout_5.setWidget(6, QFormLayout.LabelRole, self.label_16)

        self.lbl_StateGapBehind = QLabel(self.tab_Deploy)
        self.lbl_StateGapBehind.setObjectName(u"lbl_StateGapBehind")
        self.lbl_StateGapBehind.setMinimumSize(QSize(200, 0))
        self.lbl_StateGapBehind.setFont(font5)
        self.lbl_StateGapBehind.setAlignment(Qt.AlignCenter)

        self.formLayout_5.setWidget(6, QFormLayout.FieldRole, self.lbl_StateGapBehind)

        self.lbl_StateGapAhead = QLabel(self.tab_Deploy)
        self.lbl_StateGapAhead.setObjectName(u"lbl_StateGapAhead")
        self.lbl_StateGapAhead.setMinimumSize(QSize(200, 0))
        self.lbl_StateGapAhead.setFont(font5)
        self.lbl_StateGapAhead.setAlignment(Qt.AlignCenter)

        self.formLayout_5.setWidget(5, QFormLayout.FieldRole, self.lbl_StateGapAhead)

        self.label_17 = QLabel(self.tab_Deploy)
        self.label_17.setObjectName(u"label_17")
        sizePolicy2.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy2)

        self.formLayout_5.setWidget(5, QFormLayout.LabelRole, self.label_17)

        self.lbl_StateGapToLeader = QLabel(self.tab_Deploy)
        self.lbl_StateGapToLeader.setObjectName(u"lbl_StateGapToLeader")
        self.lbl_StateGapToLeader.setMinimumSize(QSize(200, 0))
        self.lbl_StateGapToLeader.setFont(font5)
        self.lbl_StateGapToLeader.setAlignment(Qt.AlignCenter)

        self.formLayout_5.setWidget(7, QFormLayout.FieldRole, self.lbl_StateGapToLeader)

        self.label_18 = QLabel(self.tab_Deploy)
        self.label_18.setObjectName(u"label_18")
        sizePolicy2.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy2)

        self.formLayout_5.setWidget(7, QFormLayout.LabelRole, self.label_18)

        self.lbl_StateLastLap = QLabel(self.tab_Deploy)
        self.lbl_StateLastLap.setObjectName(u"lbl_StateLastLap")
        self.lbl_StateLastLap.setMinimumSize(QSize(200, 0))
        self.lbl_StateLastLap.setFont(font5)
        self.lbl_StateLastLap.setAlignment(Qt.AlignCenter)

        self.formLayout_5.setWidget(8, QFormLayout.FieldRole, self.lbl_StateLastLap)

        self.label_19 = QLabel(self.tab_Deploy)
        self.label_19.setObjectName(u"label_19")
        sizePolicy2.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy2)

        self.formLayout_5.setWidget(8, QFormLayout.LabelRole, self.label_19)


        self.horizontalLayout_5.addLayout(self.formLayout_5)

        self.tabW_Deploy = QTabWidget(self.tab_Deploy)
        self.tabW_Deploy.setObjectName(u"tabW_Deploy")
        self.tab_DeployFeatureImportance = QWidget()
        self.tab_DeployFeatureImportance.setObjectName(u"tab_DeployFeatureImportance")
        self.horizontalLayout_7 = QHBoxLayout(self.tab_DeployFeatureImportance)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.fe_layout = QVBoxLayout()
        self.fe_layout.setObjectName(u"fe_layout")

        self.horizontalLayout_7.addLayout(self.fe_layout)

        self.horizontalLayout_7.setStretch(0, 1)
        self.tabW_Deploy.addTab(self.tab_DeployFeatureImportance, "")
        self.tab_DeployDecisionTree = QWidget()
        self.tab_DeployDecisionTree.setObjectName(u"tab_DeployDecisionTree")
        self.horizontalLayout_8 = QHBoxLayout(self.tab_DeployDecisionTree)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.dt_layout = QVBoxLayout()
        self.dt_layout.setObjectName(u"dt_layout")

        self.horizontalLayout_8.addLayout(self.dt_layout)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_25 = QLabel(self.tab_DeployDecisionTree)
        self.label_25.setObjectName(u"label_25")
        font8 = QFont()
        font8.setFamilies([u"Unity Sans TT"])
        font8.setPointSize(20)
        font8.setBold(True)
        font8.setUnderline(True)
        font8.setKerning(True)
        self.label_25.setFont(font8)
        self.label_25.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_25)

        self.te_DecisionPath = QTextEdit(self.tab_DeployDecisionTree)
        self.te_DecisionPath.setObjectName(u"te_DecisionPath")
        self.te_DecisionPath.setMinimumSize(QSize(300, 0))
        font9 = QFont()
        font9.setFamilies([u"Unity Sans TT"])
        font9.setPointSize(18)
        self.te_DecisionPath.setFont(font9)
        self.te_DecisionPath.setReadOnly(True)

        self.verticalLayout_6.addWidget(self.te_DecisionPath)


        self.horizontalLayout_8.addLayout(self.verticalLayout_6)

        self.horizontalLayout_8.setStretch(0, 1)
        self.tabW_Deploy.addTab(self.tab_DeployDecisionTree, "")
        self.tab_DeployCF = QWidget()
        self.tab_DeployCF.setObjectName(u"tab_DeployCF")
        self.verticalLayout_3 = QVBoxLayout(self.tab_DeployCF)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.box_CFNoPit = QCheckBox(self.tab_DeployCF)
        self.box_CFNoPit.setObjectName(u"box_CFNoPit")
        self.box_CFNoPit.setMinimumSize(QSize(100, 0))
        font10 = QFont()
        font10.setFamilies([u"Unity Sans TT"])
        font10.setPointSize(20)
        self.box_CFNoPit.setFont(font10)

        self.horizontalLayout_10.addWidget(self.box_CFNoPit, 0, Qt.AlignHCenter)

        self.box_CFPitSoft = QCheckBox(self.tab_DeployCF)
        self.box_CFPitSoft.setObjectName(u"box_CFPitSoft")
        self.box_CFPitSoft.setMinimumSize(QSize(100, 0))
        self.box_CFPitSoft.setFont(font10)

        self.horizontalLayout_10.addWidget(self.box_CFPitSoft, 0, Qt.AlignHCenter)

        self.box_CFPitMedium = QCheckBox(self.tab_DeployCF)
        self.box_CFPitMedium.setObjectName(u"box_CFPitMedium")
        self.box_CFPitMedium.setMinimumSize(QSize(100, 0))
        self.box_CFPitMedium.setFont(font10)

        self.horizontalLayout_10.addWidget(self.box_CFPitMedium, 0, Qt.AlignHCenter)

        self.box_CFPitHard = QCheckBox(self.tab_DeployCF)
        self.box_CFPitHard.setObjectName(u"box_CFPitHard")
        self.box_CFPitHard.setMinimumSize(QSize(100, 0))
        self.box_CFPitHard.setFont(font10)

        self.horizontalLayout_10.addWidget(self.box_CFPitHard, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer)

        self.btn_CFCandidateLess = QPushButton(self.tab_DeployCF)
        self.btn_CFCandidateLess.setObjectName(u"btn_CFCandidateLess")
        self.btn_CFCandidateLess.setEnabled(False)

        self.horizontalLayout_10.addWidget(self.btn_CFCandidateLess)

        self.label_37 = QLabel(self.tab_DeployCF)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setAlignment(Qt.AlignCenter)
        self.label_37.setWordWrap(True)

        self.horizontalLayout_10.addWidget(self.label_37)

        self.lbl_CFDistance = QLabel(self.tab_DeployCF)
        self.lbl_CFDistance.setObjectName(u"lbl_CFDistance")
        self.lbl_CFDistance.setMinimumSize(QSize(75, 0))
        font11 = QFont()
        font11.setFamilies([u"Unity Sans TT"])
        font11.setPointSize(15)
        self.lbl_CFDistance.setFont(font11)
        self.lbl_CFDistance.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_10.addWidget(self.lbl_CFDistance)

        self.btn_CFCandidateMore = QPushButton(self.tab_DeployCF)
        self.btn_CFCandidateMore.setObjectName(u"btn_CFCandidateMore")

        self.horizontalLayout_10.addWidget(self.btn_CFCandidateMore)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.cf_layout = QVBoxLayout()
        self.cf_layout.setObjectName(u"cf_layout")

        self.horizontalLayout_13.addLayout(self.cf_layout)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_26 = QLabel(self.tab_DeployCF)
        self.label_26.setObjectName(u"label_26")
        font12 = QFont()
        font12.setFamilies([u"Unity Sans TT"])
        font12.setPointSize(20)
        font12.setBold(True)
        font12.setUnderline(True)
        self.label_26.setFont(font12)
        self.label_26.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.label_26)

        self.te_CFRequiredChanges = QTextEdit(self.tab_DeployCF)
        self.te_CFRequiredChanges.setObjectName(u"te_CFRequiredChanges")
        self.te_CFRequiredChanges.setMinimumSize(QSize(400, 0))
        self.te_CFRequiredChanges.setFont(font9)
        self.te_CFRequiredChanges.setReadOnly(True)

        self.verticalLayout_8.addWidget(self.te_CFRequiredChanges)


        self.horizontalLayout_13.addLayout(self.verticalLayout_8)

        self.horizontalLayout_13.setStretch(0, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_13)

        self.verticalLayout_3.setStretch(1, 1)
        self.tabW_Deploy.addTab(self.tab_DeployCF, "")
        self.tab_RacePlot = QWidget()
        self.tab_RacePlot.setObjectName(u"tab_RacePlot")
        self.horizontalLayout_12 = QHBoxLayout(self.tab_RacePlot)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.rp_layout = QVBoxLayout()
        self.rp_layout.setObjectName(u"rp_layout")

        self.horizontalLayout_12.addLayout(self.rp_layout)

        self.horizontalLayout_12.setStretch(0, 1)
        self.tabW_Deploy.addTab(self.tab_RacePlot, "")

        self.horizontalLayout_5.addWidget(self.tabW_Deploy)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.verticalLayout_5.setStretch(2, 1)
        self.tabW_TrainDeploy.addTab(self.tab_Deploy, "")
        self.tab_TestResults = QWidget()
        self.tab_TestResults.setObjectName(u"tab_TestResults")
        self.verticalLayout_11 = QVBoxLayout(self.tab_TestResults)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.btn_ReloadDataset = QPushButton(self.tab_TestResults)
        self.btn_ReloadDataset.setObjectName(u"btn_ReloadDataset")

        self.gridLayout_2.addWidget(self.btn_ReloadDataset, 1, 6, 1, 1)

        self.label_33 = QLabel(self.tab_TestResults)
        self.label_33.setObjectName(u"label_33")
        font13 = QFont()
        font13.setFamilies([u"Unity Sans TT"])
        font13.setBold(True)
        self.label_33.setFont(font13)
        self.label_33.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_33, 0, 5, 1, 1)

        self.label_32 = QLabel(self.tab_TestResults)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font13)
        self.label_32.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_32, 0, 4, 1, 1)

        self.sb_FinishingPositionFilter = QSpinBox(self.tab_TestResults)
        self.sb_FinishingPositionFilter.setObjectName(u"sb_FinishingPositionFilter")
        self.sb_FinishingPositionFilter.setMinimumSize(QSize(75, 0))
        self.sb_FinishingPositionFilter.setMaximum(20)

        self.gridLayout_2.addWidget(self.sb_FinishingPositionFilter, 1, 4, 1, 1)

        self.cb_TrackFilter = QComboBox(self.tab_TestResults)
        self.cb_TrackFilter.setObjectName(u"cb_TrackFilter")

        self.gridLayout_2.addWidget(self.cb_TrackFilter, 1, 2, 1, 1)

        self.label_29 = QLabel(self.tab_TestResults)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setFont(font13)
        self.label_29.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_29, 0, 1, 1, 1)

        self.label_30 = QLabel(self.tab_TestResults)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font13)
        self.label_30.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_30, 0, 2, 1, 1)

        self.cb_NameFilter = QComboBox(self.tab_TestResults)
        self.cb_NameFilter.setObjectName(u"cb_NameFilter")

        self.gridLayout_2.addWidget(self.cb_NameFilter, 1, 1, 1, 1)

        self.cb_YearFilter = QComboBox(self.tab_TestResults)
        self.cb_YearFilter.setObjectName(u"cb_YearFilter")

        self.gridLayout_2.addWidget(self.cb_YearFilter, 1, 3, 1, 1)

        self.label_28 = QLabel(self.tab_TestResults)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font13)
        self.label_28.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_28, 0, 0, 1, 1)

        self.le_TyreStrategy = QLineEdit(self.tab_TestResults)
        self.le_TyreStrategy.setObjectName(u"le_TyreStrategy")

        self.gridLayout_2.addWidget(self.le_TyreStrategy, 1, 5, 1, 1)

        self.label_31 = QLabel(self.tab_TestResults)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font13)
        self.label_31.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_31, 0, 3, 1, 1)

        self.sb_TestRunFilter = QSpinBox(self.tab_TestResults)
        self.sb_TestRunFilter.setObjectName(u"sb_TestRunFilter")
        self.sb_TestRunFilter.setMinimumSize(QSize(75, 0))

        self.gridLayout_2.addWidget(self.sb_TestRunFilter, 1, 0, 1, 1)

        self.gridLayout_2.setColumnStretch(5, 1)

        self.verticalLayout_11.addLayout(self.gridLayout_2)

        self.table_TestResults = QTableWidget(self.tab_TestResults)
        if (self.table_TestResults.columnCount() < 6):
            self.table_TestResults.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_TestResults.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_TestResults.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_TestResults.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_TestResults.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_TestResults.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_TestResults.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.table_TestResults.setObjectName(u"table_TestResults")
        self.table_TestResults.setEnabled(True)
        self.table_TestResults.setMaximumSize(QSize(16777215, 400))
        self.table_TestResults.setFont(font11)
        self.table_TestResults.horizontalHeader().setVisible(True)
        self.table_TestResults.horizontalHeader().setHighlightSections(True)
        self.table_TestResults.horizontalHeader().setProperty("showSortIndicator", False)

        self.verticalLayout_11.addWidget(self.table_TestResults)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_40 = QLabel(self.tab_TestResults)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setFont(font13)

        self.horizontalLayout_15.addWidget(self.label_40)

        self.cb_TyreStrategyTrack = QComboBox(self.tab_TestResults)
        self.cb_TyreStrategyTrack.setObjectName(u"cb_TyreStrategyTrack")
        self.cb_TyreStrategyTrack.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_15.addWidget(self.cb_TyreStrategyTrack)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_2)

        self.label_39 = QLabel(self.tab_TestResults)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setFont(font13)

        self.horizontalLayout_15.addWidget(self.label_39)

        self.sb_NumPlotTyreStrategies = QSpinBox(self.tab_TestResults)
        self.sb_NumPlotTyreStrategies.setObjectName(u"sb_NumPlotTyreStrategies")
        self.sb_NumPlotTyreStrategies.setMinimumSize(QSize(50, 0))
        self.sb_NumPlotTyreStrategies.setMinimum(1)
        self.sb_NumPlotTyreStrategies.setMaximum(20)
        self.sb_NumPlotTyreStrategies.setValue(5)

        self.horizontalLayout_15.addWidget(self.sb_NumPlotTyreStrategies)


        self.verticalLayout_15.addLayout(self.horizontalLayout_15)

        self.ts_layout = QVBoxLayout()
        self.ts_layout.setObjectName(u"ts_layout")

        self.verticalLayout_15.addLayout(self.ts_layout)

        self.verticalLayout_15.setStretch(1, 1)

        self.horizontalLayout_14.addLayout(self.verticalLayout_15)

        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label = QLabel(self.tab_TestResults)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(200, 0))
        self.label.setFont(font12)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.label)

        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_2 = QLabel(self.tab_TestResults)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font11)

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.lbl_StatsBestFinish = QLabel(self.tab_TestResults)
        self.lbl_StatsBestFinish.setObjectName(u"lbl_StatsBestFinish")
        self.lbl_StatsBestFinish.setFont(font11)

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.lbl_StatsBestFinish)

        self.label_5 = QLabel(self.tab_TestResults)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font11)

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.lbl_StatsWorstFinish = QLabel(self.tab_TestResults)
        self.lbl_StatsWorstFinish.setObjectName(u"lbl_StatsWorstFinish")
        self.lbl_StatsWorstFinish.setFont(font11)

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.lbl_StatsWorstFinish)

        self.label_7 = QLabel(self.tab_TestResults)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font11)

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.label_7)

        self.lbl_StatsMeanFinish = QLabel(self.tab_TestResults)
        self.lbl_StatsMeanFinish.setObjectName(u"lbl_StatsMeanFinish")
        self.lbl_StatsMeanFinish.setFont(font11)

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.lbl_StatsMeanFinish)

        self.label_6 = QLabel(self.tab_TestResults)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font11)

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.label_6)

        self.lbl_StatsModeFinish = QLabel(self.tab_TestResults)
        self.lbl_StatsModeFinish.setObjectName(u"lbl_StatsModeFinish")
        self.lbl_StatsModeFinish.setFont(font11)

        self.formLayout_4.setWidget(3, QFormLayout.FieldRole, self.lbl_StatsModeFinish)

        self.label_9 = QLabel(self.tab_TestResults)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font11)

        self.formLayout_4.setWidget(4, QFormLayout.LabelRole, self.label_9)

        self.lbl_StatsStdDev = QLabel(self.tab_TestResults)
        self.lbl_StatsStdDev.setObjectName(u"lbl_StatsStdDev")
        self.lbl_StatsStdDev.setFont(font11)

        self.formLayout_4.setWidget(4, QFormLayout.FieldRole, self.lbl_StatsStdDev)

        self.label_10 = QLabel(self.tab_TestResults)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font11)

        self.formLayout_4.setWidget(5, QFormLayout.LabelRole, self.label_10)

        self.lbl_StatsNumValidTests = QLabel(self.tab_TestResults)
        self.lbl_StatsNumValidTests.setObjectName(u"lbl_StatsNumValidTests")
        self.lbl_StatsNumValidTests.setFont(font11)

        self.formLayout_4.setWidget(5, QFormLayout.FieldRole, self.lbl_StatsNumValidTests)

        self.label_27 = QLabel(self.tab_TestResults)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font11)

        self.formLayout_4.setWidget(6, QFormLayout.LabelRole, self.label_27)

        self.lbl_StatsTestFails = QLabel(self.tab_TestResults)
        self.lbl_StatsTestFails.setObjectName(u"lbl_StatsTestFails")
        self.lbl_StatsTestFails.setFont(font11)

        self.formLayout_4.setWidget(6, QFormLayout.FieldRole, self.lbl_StatsTestFails)


        self.verticalLayout_14.addLayout(self.formLayout_4)

        self.label_8 = QLabel(self.tab_TestResults)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font12)
        self.label_8.setAlignment(Qt.AlignCenter)
        self.label_8.setWordWrap(True)

        self.verticalLayout_14.addWidget(self.label_8)

        self.fpd_layout = QVBoxLayout()
        self.fpd_layout.setObjectName(u"fpd_layout")

        self.verticalLayout_14.addLayout(self.fpd_layout)

        self.verticalLayout_14.setStretch(3, 1)

        self.horizontalLayout_14.addLayout(self.verticalLayout_14)

        self.horizontalLayout_14.setStretch(0, 1)

        self.verticalLayout_11.addLayout(self.horizontalLayout_14)

        self.verticalLayout_11.setStretch(2, 1)
        self.tabW_TrainDeploy.addTab(self.tab_TestResults, "")

        self.verticalLayout_2.addWidget(self.tabW_TrainDeploy)


        self.retranslateUi(RL_Strategy_GUI)

        self.tabW_TrainDeploy.setCurrentIndex(1)
        self.tabW_Train.setCurrentIndex(0)
        self.tabW_Deploy.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(RL_Strategy_GUI)
    # setupUi

    def retranslateUi(self, RL_Strategy_GUI):
        RL_Strategy_GUI.setWindowTitle(QCoreApplication.translate("RL_Strategy_GUI", u"RL_Strategy_GUI", None))
        self.lbl_ImperialLogo.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Imperial College London", None))
        self.lbl_MercedesLogo.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Mercedes-AMG", None))
        self.lbl_NumEpisodes.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Number of Episodes", None))
        self.lbl_Seed.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Seed", None))
        self.lbl_FixedSeed.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Fixed Seed", None))
        self.lbl_StepSize.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Simulation Step Size", None))
        self.box_FixedSeed.setText("")
        self.lbl_Epsilon.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Epsilon", None))
        self.lbl_EpsilonDecay.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Epsilon Decay", None))
        self.lbl_MinEpsilon.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Minimum Epsilon", None))
        self.lbl_Gamma.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Gamma", None))
        self.lbl_LearningRate.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Learning Rate", None))
        self.lbl_WeightDecay.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Weight Decay", None))
        self.lbl_ReplayBufferSize.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Replay Buffer Size", None))
        self.lbl_ReplayBufferSampleSize.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Replay Buffer Sample Size", None))
        self.lbl_EpisodesUpdateTargetNetwork.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Episodes to Update Target Network", None))
        self.cb_RewardFunction.setItemText(0, QCoreApplication.translate("RL_Strategy_GUI", u"Basic", None))

        self.lbl_NumEpisodes_2.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Selected Driver", None))
        self.cb_SelectedDriver.setItemText(0, QCoreApplication.translate("RL_Strategy_GUI", u"Lewis Hamilton", None))
        self.cb_SelectedDriver.setItemText(1, QCoreApplication.translate("RL_Strategy_GUI", u"George Russell", None))

        self.lbl_ModelName.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Model Name", None))
        self.lbl_DisableSC.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Disable Safety Car", None))
        self.box_DisableSC.setText("")
        self.lbl_RewardFunction.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Reward Function", None))
        self.tabW_Train.setTabText(self.tabW_Train.indexOf(self.tab_TrainModel), QCoreApplication.translate("RL_Strategy_GUI", u"Model", None))
        self.label_11.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Maximum Depth", None))
        self.label_20.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Maximum Iterations", None))
        self.label_21.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Maximum Samples", None))
        self.label_22.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Reweight Samples", None))
        self.label_23.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Batch Rollouts", None))
        self.label_24.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Test Rollouts", None))
        self.box_ReweightSamples.setText("")
        self.tabW_Train.setTabText(self.tabW_Train.indexOf(self.tab_TrainDecisionTree), QCoreApplication.translate("RL_Strategy_GUI", u"Decision Tree", None))
        self.btn_StartTraining.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Start Training", None))
        self.btn_SaveModel.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Save Model", None))
        self.tabW_TrainDeploy.setTabText(self.tabW_TrainDeploy.indexOf(self.tab_Train), QCoreApplication.translate("RL_Strategy_GUI", u"Train", None))
        self.lbl_LoadedModel.setText(QCoreApplication.translate("RL_Strategy_GUI", u"No Model Loaded", None))
        self.btn_LoadModel.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Load Model", None))
        self.cb_DataSource.setItemText(0, QCoreApplication.translate("RL_Strategy_GUI", u"F1 23", None))
        self.cb_DataSource.setItemText(1, QCoreApplication.translate("RL_Strategy_GUI", u"Race Simulator", None))
        self.cb_DataSource.setItemText(2, QCoreApplication.translate("RL_Strategy_GUI", u"DiL Simulator", None))
        self.cb_DataSource.setItemText(3, QCoreApplication.translate("RL_Strategy_GUI", u"Live Race", None))

        self.lbl_IPAddress.setText(QCoreApplication.translate("RL_Strategy_GUI", u"IP Address", None))
        self.le_IPAddress.setInputMask("")
        self.le_IPAddress.setText(QCoreApplication.translate("RL_Strategy_GUI", u"192.168.0.109", None))
        self.lbl_Port.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Port", None))
        self.btn_StartStop.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Start", None))
        self.lbl_RunStatus.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Stopped", None))
        self.label_38.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Telemetry Settings", None))
        self.lbl_DTPrediction.setText(QCoreApplication.translate("RL_Strategy_GUI", u"NO_PIT", None))
        self.lbl_ModelPrediction.setText(QCoreApplication.translate("RL_Strategy_GUI", u"NO_PIT", None))
        self.label_42.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Model Action", None))
        self.lbl_DTPredTitle.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Decision Tree Action", None))
        self.cb_RaceSelect.setItemText(0, QCoreApplication.translate("RL_Strategy_GUI", u"Abu Dhabi", None))
        self.cb_RaceSelect.setItemText(1, QCoreApplication.translate("RL_Strategy_GUI", u"Australia", None))
        self.cb_RaceSelect.setItemText(2, QCoreApplication.translate("RL_Strategy_GUI", u"Austria", None))
        self.cb_RaceSelect.setItemText(3, QCoreApplication.translate("RL_Strategy_GUI", u"Azerbaijan", None))
        self.cb_RaceSelect.setItemText(4, QCoreApplication.translate("RL_Strategy_GUI", u"Bahrain", None))
        self.cb_RaceSelect.setItemText(5, QCoreApplication.translate("RL_Strategy_GUI", u"Belgium", None))
        self.cb_RaceSelect.setItemText(6, QCoreApplication.translate("RL_Strategy_GUI", u"Brazil", None))
        self.cb_RaceSelect.setItemText(7, QCoreApplication.translate("RL_Strategy_GUI", u"Canada", None))
        self.cb_RaceSelect.setItemText(8, QCoreApplication.translate("RL_Strategy_GUI", u"China", None))
        self.cb_RaceSelect.setItemText(9, QCoreApplication.translate("RL_Strategy_GUI", u"Emilia Romagna", None))
        self.cb_RaceSelect.setItemText(10, QCoreApplication.translate("RL_Strategy_GUI", u"Hungary", None))
        self.cb_RaceSelect.setItemText(11, QCoreApplication.translate("RL_Strategy_GUI", u"Italy", None))
        self.cb_RaceSelect.setItemText(12, QCoreApplication.translate("RL_Strategy_GUI", u"Japan", None))
        self.cb_RaceSelect.setItemText(13, QCoreApplication.translate("RL_Strategy_GUI", u"Las Vegas", None))
        self.cb_RaceSelect.setItemText(14, QCoreApplication.translate("RL_Strategy_GUI", u"Mexico", None))
        self.cb_RaceSelect.setItemText(15, QCoreApplication.translate("RL_Strategy_GUI", u"Miami", None))
        self.cb_RaceSelect.setItemText(16, QCoreApplication.translate("RL_Strategy_GUI", u"Monaco", None))
        self.cb_RaceSelect.setItemText(17, QCoreApplication.translate("RL_Strategy_GUI", u"Netherlands", None))
        self.cb_RaceSelect.setItemText(18, QCoreApplication.translate("RL_Strategy_GUI", u"Qatar", None))
        self.cb_RaceSelect.setItemText(19, QCoreApplication.translate("RL_Strategy_GUI", u"Saudi Arabia", None))
        self.cb_RaceSelect.setItemText(20, QCoreApplication.translate("RL_Strategy_GUI", u"Singapore", None))
        self.cb_RaceSelect.setItemText(21, QCoreApplication.translate("RL_Strategy_GUI", u"Spain", None))
        self.cb_RaceSelect.setItemText(22, QCoreApplication.translate("RL_Strategy_GUI", u"UK", None))
        self.cb_RaceSelect.setItemText(23, QCoreApplication.translate("RL_Strategy_GUI", u"USA", None))

        self.btn_PitHard.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Pit Hard", None))
        self.btn_PitSoft.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Pit Soft", None))
        self.btn_StepModel.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Step Model", None))
        self.btn_NoPit.setText(QCoreApplication.translate("RL_Strategy_GUI", u"No Pit", None))
        self.cb_YearSelect.setItemText(0, QCoreApplication.translate("RL_Strategy_GUI", u"2023", None))
        self.cb_YearSelect.setItemText(1, QCoreApplication.translate("RL_Strategy_GUI", u"2022", None))
        self.cb_YearSelect.setItemText(2, QCoreApplication.translate("RL_Strategy_GUI", u"2021", None))

        self.btn_PitMedium.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Pit Medium", None))
        self.label_3.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Seed:", None))
        self.btn_ResetSimulation.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Reset Simulation", None))
        self.btn_StepDecisionTree.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Step Decision Tree", None))
        self.label_34.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Force Decision", None))
        self.label_35.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Trained Decision", None))
        self.label_36.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Simulation Parameters", None))
        self.label_4.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Position", None))
        self.lbl_StatePosition.setText(QCoreApplication.translate("RL_Strategy_GUI", u"P1", None))
        self.label_12.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Safety Car", None))
        self.lbl_StateSafetyCarStatus.setText(QCoreApplication.translate("RL_Strategy_GUI", u"NSC", None))
        self.label_13.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Lap Number", None))
        self.lbl_StateLapNumber.setText(QCoreApplication.translate("RL_Strategy_GUI", u"L0", None))
        self.label_14.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Current Tyre", None))
        self.lbl_StateCurrentTyre.setText(QCoreApplication.translate("RL_Strategy_GUI", u"CT", None))
        self.label_15.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Tyre Degradation", None))
        self.lbl_StateTyreDegradation.setText(QCoreApplication.translate("RL_Strategy_GUI", u"TD", None))
        self.label_16.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Gap Behind", None))
        self.lbl_StateGapBehind.setText(QCoreApplication.translate("RL_Strategy_GUI", u"GB", None))
        self.lbl_StateGapAhead.setText(QCoreApplication.translate("RL_Strategy_GUI", u"GA", None))
        self.label_17.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Gap Ahead", None))
        self.lbl_StateGapToLeader.setText(QCoreApplication.translate("RL_Strategy_GUI", u"GL", None))
        self.label_18.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Gap To Leader", None))
        self.lbl_StateLastLap.setText(QCoreApplication.translate("RL_Strategy_GUI", u"LL", None))
        self.label_19.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Last Lap", None))
        self.tabW_Deploy.setTabText(self.tabW_Deploy.indexOf(self.tab_DeployFeatureImportance), QCoreApplication.translate("RL_Strategy_GUI", u"Feature Importance", None))
        self.label_25.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Decision Tree Path", None))
        self.tabW_Deploy.setTabText(self.tabW_Deploy.indexOf(self.tab_DeployDecisionTree), QCoreApplication.translate("RL_Strategy_GUI", u"Decision Tree", None))
        self.box_CFNoPit.setText(QCoreApplication.translate("RL_Strategy_GUI", u"No Pit", None))
        self.box_CFPitSoft.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Pit Soft", None))
        self.box_CFPitMedium.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Pit Medium", None))
        self.box_CFPitHard.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Pit Hard", None))
        self.btn_CFCandidateLess.setText(QCoreApplication.translate("RL_Strategy_GUI", u"<", None))
        self.label_37.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Counterfactual Distance:", None))
        self.lbl_CFDistance.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Distance", None))
        self.btn_CFCandidateMore.setText(QCoreApplication.translate("RL_Strategy_GUI", u">", None))
        self.label_26.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Required Changes", None))
        self.tabW_Deploy.setTabText(self.tabW_Deploy.indexOf(self.tab_DeployCF), QCoreApplication.translate("RL_Strategy_GUI", u"Counterfactual", None))
        self.tabW_Deploy.setTabText(self.tabW_Deploy.indexOf(self.tab_RacePlot), QCoreApplication.translate("RL_Strategy_GUI", u"Race Plot", None))
        self.tabW_TrainDeploy.setTabText(self.tabW_TrainDeploy.indexOf(self.tab_Deploy), QCoreApplication.translate("RL_Strategy_GUI", u"Deploy", None))
        self.btn_ReloadDataset.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Reload Dataset", None))
        self.label_33.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Tyre Strategy", None))
        self.label_32.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Finishing Position", None))
        self.label_29.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Model Name", None))
        self.label_30.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Track", None))
        self.label_28.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Test Run", None))
        self.label_31.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Year", None))
        ___qtablewidgetitem = self.table_TestResults.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Test Run", None));
        ___qtablewidgetitem1 = self.table_TestResults.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Model Name", None));
        ___qtablewidgetitem2 = self.table_TestResults.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Track", None));
        ___qtablewidgetitem3 = self.table_TestResults.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Year", None));
        ___qtablewidgetitem4 = self.table_TestResults.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Finishing Position", None));
        ___qtablewidgetitem5 = self.table_TestResults.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Tyre Strategy", None));
        self.label_40.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Plot Track:", None))
        self.label_39.setText(QCoreApplication.translate("RL_Strategy_GUI", u"No. Plot Strategies:", None))
        self.label.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Statistics", None))
        self.label_2.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Best Finish:", None))
        self.lbl_StatsBestFinish.setText(QCoreApplication.translate("RL_Strategy_GUI", u"0", None))
        self.label_5.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Worst Finish:", None))
        self.lbl_StatsWorstFinish.setText(QCoreApplication.translate("RL_Strategy_GUI", u"0", None))
        self.label_7.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Mean Finish:", None))
        self.lbl_StatsMeanFinish.setText(QCoreApplication.translate("RL_Strategy_GUI", u"0", None))
        self.label_6.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Mode Finish:", None))
        self.lbl_StatsModeFinish.setText(QCoreApplication.translate("RL_Strategy_GUI", u"0", None))
        self.label_9.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Std Dev:", None))
        self.lbl_StatsStdDev.setText(QCoreApplication.translate("RL_Strategy_GUI", u"0", None))
        self.label_10.setText(QCoreApplication.translate("RL_Strategy_GUI", u"No. Valid Tests", None))
        self.lbl_StatsNumValidTests.setText(QCoreApplication.translate("RL_Strategy_GUI", u"0", None))
        self.label_27.setText(QCoreApplication.translate("RL_Strategy_GUI", u"No. Test Fails", None))
        self.lbl_StatsTestFails.setText(QCoreApplication.translate("RL_Strategy_GUI", u"0", None))
        self.label_8.setText(QCoreApplication.translate("RL_Strategy_GUI", u"Finishing Position Distribution", None))
        self.tabW_TrainDeploy.setTabText(self.tabW_TrainDeploy.indexOf(self.tab_TestResults), QCoreApplication.translate("RL_Strategy_GUI", u"Test Results", None))
    # retranslateUi

