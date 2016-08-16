# -*- coding: utf-8 -*-
"""
/***************************************************************************
        QWMS
        A QGIS plugin - WMS services in one place.
        
        WMS Services are (C) by Glowny Urzad Geodezji i Kartografii, Poland
        www.geoportal.gov.pl
        
                              -------------------
        begin                : 2016-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Adam Borczyk
        email                : ad.borczyk@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QListWidget, QListWidgetItem
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from qwms_dialog import QWMSDialog
import os.path
from qgis.core import *
from utils import *
import urllib2
import xml.etree.ElementTree as ET

class QWMS:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'QWMS_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = QWMSDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&QWMS')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'QWMS')
        self.toolbar.setObjectName(u'QWMS')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('QWMS', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/QWMS/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Get WMS'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&QWMS'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def approveChoice(self, i):
        """Returns index of WMS service"""
        self.dlg.comboBox_2.clear()
        self.dlg.textEdit.clear()
        self.selectedWMSIndex = self.dlg.comboBox.currentIndex()
        return self.selectedWMSIndex       

    def selectedChoice(self):
        """Gets layers of selected WMS"""
        
        ## Execute GetCapabilities
        self.dlg.comboBox_2.clear()
        if self.dlg.comboBox.currentIndex() == len(wmsList): # if GDOS
            url_to_wms_getcaps = wms_getcap_gdos
        else:            
            service = wmsLinks[self.dlg.comboBox.currentIndex()] # else
            url_to_wms_getcaps = wms_getcap_geop % (service)

        ## Read the XML
        try:
            tree = ET.parse(urllib2.urlopen(url_to_wms_getcaps))
        except: 
            self.dlg.textEdit.setPlainText('Server error')
        root = tree.getroot()

        self.layerDict = {} # User-friendly names
        self.layerDictURL = {} # Names that URL parses

        ## Choose proper path and get available layers to dict
        ## depending on XML structure
        layerID = 0 
     
        if root.findall(xmlStructureURL_3):
            for layer in root.findall(xmlStructureURL_3):
                if layer.tag == layerTagTitle:
                    self.layerDict[layerID-1] = (layer.text)
                if layer.tag == layerTagName:
                    self.layerDictURL[layerID] = (layer.text)
                layerID += 1            
        else: 
            if root.findall(xmlStructureURL_2):
                for layer in root.findall(xmlStructureURL_2):
                    if layer.tag == layerTagTitle:
                        self.layerDict[layerID-1] = (layer.text)
                    if layer.tag == layerTagName:
                        self.layerDictURL[layerID] = (layer.text)
                        layerID += 1            
            else:
                if root.findall(xmlStructureURL_1):
                    for layer in root.findall(xmlStructureURL_1):
                        if layer.tag == layerTagTitle:
                            self.layerDict[layerID-1] = (layer.text)
                        if layer.tag == layerTagName:
                            self.layerDictURL[layerID] = (layer.text)
                            layerID += 1
                else:
                    if root.findall(xmlStructureURL_4):
                        for layer in root.findall(xmlStructureURL_4):
                            if layer.tag == layerTagTitle:
                                self.layerDict[layerID-1] = (layer.text)
                            if layer.tag == layerTagName:
                                self.layerDictURL[layerID] = (layer.text)
                            layerID += 1       
                    else:
                        print 'Unknown XML structure'
            
        ## Gets available layers and adds them as checkboxes
        self.dlg.listWidget.clear()
        self.dlg.listWidget.setVisible(True)  
        for key, value in self.layerDict.iteritems():
            self.layerToSelect = QListWidgetItem()
            self.layerToSelect.setText(value)
            self.layerToSelect.setFlags(self.layerToSelect.flags() | QtCore.Qt.ItemIsUserCheckable)
            if len(self.layerDict) <= 1: # if only one layer available
                self.layerToSelect.setCheckState(QtCore.Qt.Checked)
                self.dlg.listWidget.addItem(self.layerToSelect)
                self.dlg.listWidget.setEnabled(False)    
            else: # if more than one available
                self.layerToSelect.setCheckState(QtCore.Qt.Unchecked)
                self.dlg.listWidget.addItem(self.layerToSelect)
                self.dlg.listWidget.setEnabled(True) 
                self.dlg.pushButton_3.setEnabled(True)          
        self.dlg.pushButton_2.setEnabled(True)
        return

    def iterate(self):
        """Checks which layers have been selected and returns them"""
        self.items = []
        self.countChecked = 0
        for index in xrange(self.dlg.listWidget.count()):
            if self.dlg.listWidget.item(index).checkState() == QtCore.Qt.Checked:
                self.countChecked += 1
                self.items.append(self.dlg.listWidget.item(index).text())

        ## Get IDs of chosen layers to query it from listDictURL dict
        self.keysIDs = []
        self.keysURL = []
        self.indexStyles = []
        for i in self.items:
            for key, value in self.layerDict.iteritems():
                if i == value:
                    self.keysIDs.append(key)

        ## Create 'styles' part of WMS URL depending on number of layers chosen
        for i in self.keysIDs:
            for key, value in self.layerDictURL.iteritems():
                if i == key:
                    self.keysURL.append(value)
                    self.indexStyles.append(wms_styles)
        return self.items

    def textBox(self):
        """Shows URL to be queried in the text box"""
        
        ## Gets current EPSG
        canvas = self.iface.mapCanvas()
        currentEPSG = canvas.mapRenderer().destinationCrs().authid()
        if currentEPSG not in availableEPSG:
            currentEPSG = 'EPSG:4326'

        ## Get part of WMS URL corresponding to selected service
        if self.dlg.comboBox.currentIndex() == len(wmsList):
            wms_url = wms_url_gdos
        else:            
            service = wmsLinks[self.dlg.comboBox.currentIndex()]
            wms_url = wms_url_geop % (service)

        self.iterate()

        ## If more than one layer selected
        if self.countChecked > 1:
            for selectedLayer in self.keysURL:
                indexLayers = '&layers='.join(self.keysURL)
                indexStyles = '&'.join(self.indexStyles)

            self.urlWithParams = wms_separator.join((wms_url,
                                                wms_format,
                                                wms_layers
                                                 + indexLayers,
                                                indexStyles,
                                                wms_crs
                                                + currentEPSG))
        ## If one layer selected
        elif self.countChecked == 1:
            for selectedLayer in self.keysURL:
                indexLayers = self.keysURL[0]

            self.urlWithParams = wms_separator.join((wms_url,
                                    wms_format,
                                    wms_layers
                                     + indexLayers,
                                    wms_styles,
                                    wms_crs
                                    + currentEPSG))
        else:
            self.urlWithParams = 'Error'

        ## Insert URL to be queried in TextBox
        self.dlg.textEdit.setPlainText(self.urlWithParams)

        return self.urlWithParams

    def selectAllNone(self):
        """Selects or deselects all layers in checkbox list"""
        if self.dlg.listWidget.item(0).checkState() == QtCore.Qt.Unchecked:
            for index in xrange(self.dlg.listWidget.count()):
                self.dlg.listWidget.item(index).setCheckState(QtCore.Qt.Checked)
        else:
            for index in xrange(self.dlg.listWidget.count()):
                self.dlg.listWidget.item(index).setCheckState(QtCore.Qt.Unchecked)

    def run(self):      
        """ Run the plugin """        
        self.dlg.pushButton_2.setEnabled(False)
        self.dlg.comboBox_2.setEnabled(False)
        self.dlg.pushButton_3.setEnabled(False)
        ## Show the dialog
        self.dlg.show()

        ## Add services to the list:
        if self.dlg.comboBox.count() == 0:
            self.dlg.comboBox.addItems(wmsList)
            self.dlg.comboBox.insertSeparator(39)

        ## Refreshes window after changing service
        self.dlg.comboBox.currentIndexChanged.connect(self.approveChoice)

        ## Get layers of selected service
        self.dlg.pushButton.clicked.connect(self.selectedChoice)

        ## Select all/none layers
        self.dlg.pushButton_3.clicked.connect(self.selectAllNone)

        ## Get WMS address to be queried
        self.dlg.pushButton_2.clicked.connect(self.textBox)

        ## Run the dialog event loop
        result = self.dlg.exec_()       

        ## After pressing OK do
        if result:      
            if self.dlg.textEdit.toPlainText() == '':
                self.textBox() # If Get WMS URL is not clicked

            finalURL = self.dlg.textEdit.toPlainText()
            if finalURL != 'Error':
            ## Add layer(s)
                if self.dlg.comboBox.currentIndex() == len(wmsList): # if GDOS
                    rlayer = QgsRasterLayer(finalURL, wmsList[39], 'wms')
                else:            
                    rlayer = QgsRasterLayer(finalURL, wmsList[self.dlg.comboBox.currentIndex()], 'wms')

                if not rlayer.isValid():
                     print "Layer failed to load!"
                else:
                    QgsMapLayerRegistry.instance().addMapLayer(rlayer)
            else:
                print 'Error in querying available layers'