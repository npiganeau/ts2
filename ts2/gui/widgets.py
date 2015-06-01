#
#   Copyright (C) 2008-2013 by Nicolas Piganeau
#   npi@m4x.org
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the
#   Free Software Foundation, Inc.,
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#

from Qt import QtCore, QtWidgets

from ts2 import simulation


class Clock(QtWidgets.QLCDNumber):

    def __init__(self, parent):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.setNumDigits(8)
        self.display("--:--:--")
        self.resize(100,20)

    @QtCore.pyqtSlot(QtCore.QTime)
    def setTime(self, t):
        self.display(t.toString("hh:mm:ss"))


class Panel(QtWidgets.QWidget):
    """The panel is the display rectangle below the scene holding the widgets
    necessary to play the simulation (e.g. clock)."""

    def __init__(self, parent, simulationWindow):
        """Constructor for the Panel class."""
        super().__init__(parent)
        self.simulation = None
        self.simulationWindow = simulationWindow
        # Clock
        self.clock = Clock(self)
        # Pause button
        self.pauseButton = QtWidgets.QPushButton(self.tr("Pause"), self)
        self.pauseButton.setCheckable(True)
        # Time factor spinBox
        self.timeFactorSpinBox = QtWidgets.QSpinBox(self)
        self.timeFactorSpinBox.setRange(0, 10)
        self.timeFactorSpinBox.setSingleStep(1)
        self.timeFactorSpinBox.setValue(1)
        self.timeFactorSpinBox.setSuffix("x")
        # Zoom spinBox
        self.zoomSpinBox = QtWidgets.QSpinBox(self)
        self.zoomSpinBox.setRange(10,200)
        self.zoomSpinBox.setSingleStep(10)
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.valueChanged.connect(self.zoomSpinBoxChanged)
        # score display
        self.scoreDisplay = QtWidgets.QLCDNumber(self)
        self.scoreDisplay.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scoreDisplay.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scoreDisplay.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.scoreDisplay.setNumDigits(5)
        self.scoreDisplay.resize(70, 25)

        layout = QtWidgets.QHBoxLayout()
        layout.addSpacing(5)
        layout.addWidget(self.clock)
        layout.addSpacing(5)
        layout.addWidget(self.pauseButton)
        layout.addSpacing(5)
        layout.addWidget(QtWidgets.QLabel(self.tr("Simulation speed: ")))
        layout.addWidget(self.timeFactorSpinBox)
        layout.addSpacing(5)
        layout.addWidget(QtWidgets.QLabel(self.tr("Zoom: ")))
        layout.addWidget(self.zoomSpinBox)
        layout.addStretch()
        layout.addWidget(QtWidgets.QLabel(self.tr("Penalty points: ")))
        layout.addWidget(self.scoreDisplay)
        self.setLayout(layout)

        self.simulationWindow.simulationLoaded.connect(self.activate)

    @QtCore.pyqtSlot(simulation.Simulation)
    def activate(self, simulation):
        """Activates the panel with the given simulation."""
        self.simulation = simulation
        self.pauseButton.toggled.connect(self.simulation.pause)
        self.pauseButton.toggled.connect(self.changePauseButtonText)
        self.timeFactorSpinBox.valueChanged.connect(
                                            self.simulation.setTimeFactor)
        self.timeFactorSpinBox.setValue(
                                float(self.simulation.option("timeFactor")))

    zoomChanged = QtCore.pyqtSignal(int)

    def sizeHint(self):
        return QtCore.QSize(800,40)

    def minimumSizeHint(self):
        return QtCore.QSize(200,40)

    def sizePolicy(self):
        return QtCore.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Fixed)

    @QtCore.pyqtSlot(bool)
    def changePauseButtonText(self, paused):
        if paused:
            self.pauseButton.setText(self.tr("Continue"));
        else:
            self.pauseButton.setText(self.tr("Pause"));

    @QtCore.pyqtSlot(int)
    def zoomSpinBoxChanged(self, percent):
        self.zoomChanged.emit(percent)

