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

from ts2.Qt import QtCore, QtWidgets

from ts2 import simulation, trains

class TrainListView(QtWidgets.QTreeView):
    """ TODO Document TrainListView class"""
    trainSelected = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.simulation = None
        self.setItemsExpandable(False)
        self.setRootIsDecorated(False)
        self.setHeaderHidden(False)
        self.setSortingEnabled(True)

    

    @QtCore.pyqtSlot(int)
    def updateTrainSelection(self, trainId):
        index = self.model().index(trainId, 0)
        self.selectionModel().select(index,
                                     QtCore.QItemSelectionModel.Rows|
                                     QtCore.QItemSelectionModel.ClearAndSelect)

    @QtCore.pyqtSlot(simulation.Simulation)
    def setupTrainList(self, simulation):
        self.simulation = simulation
        #if self.model() is None:
        #trainsSortedModel = QSortFilterProxyModel()
        #trainsSortedModel.setSourceModel()
        self.setModel(self.simulation.trainListModel)
        self.header().setStretchLastSection(False)
        self.header().setSortIndicatorShown(False)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.simulation.trainStatusChanged.connect(self.model().update)
        #self._simulation.timeChanged.connect(self.model().update)
        #self.trainSelected.connect(self._simulation.selectedTrainModel.setTrainByServiceCode)


    def contextMenuEvent(self, event):
        index = self.selectionModel().selection().indexes()[0]
        if index.isValid():
            train = self.simulation.trains[index.row()]
            train.showTrainActionsMenu(self, event.globalPos())

    @QtCore.pyqtSlot(QtCore.QItemSelection, QtCore.QItemSelection)
    def selectionChanged(self, selected, deselected):
        super().selectionChanged(selected, deselected)
        if len(selected.indexes()) > 0:
            index = selected.indexes()[0]
            if index.isValid():
                self.trainSelected.emit(index.row())

