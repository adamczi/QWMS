# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QWMS
                                 A QGIS plugin - WMS services in one place.
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
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
        self.dlg.comboBox_2.clear()
        self.selectedWMSIndex = self.dlg.comboBox.currentIndex()
        print "current index: ",self.selectedWMSIndex
        return self.selectedWMSIndex       

    def selectedChoice(self):
        ## pobieranie listy warstw:
        service = wmsLinks[self.dlg.comboBox.currentIndex()]
        url_to_wms_getcaps = wms_getcap_url % (service)
        print url_to_wms_getcaps

        tree = ET.parse(urllib2.urlopen(url_to_wms_getcaps));
        root = tree.getroot()
        self.layerDict = {}
        self.layerDictURL = {}
        layerID = 0
        

        for child in root.iter('{http://www.opengis.net/wms}Layer'):
            print child.attrib
            if child.attrib == {'queryable' : '1'}:
                correctLevel = True
        print correctLevel
        if correctLevel == True:
            xmlStructureURL = xmlStructureURL_1
        else:
            xmlStructureURL = xmlStructureURL_2

        for layer in root.findall(xmlStructureURL):
            if layer.tag == '{http://www.opengis.net/wms}Title':
                self.layerDict[layerID] = (layer.text)
                #print layer.text
            if layer.tag == '{http://www.opengis.net/wms}Name':
                self.layerDictURL[layerID] = (layer.text)
                print layer.text
                layerID += 1
        print self.layerDictURL
        print self.layerDictURL.values()

        ## wybieranie warstwy z uslugi:
        
        self.dlg.comboBox_2.addItems(self.layerDict.values())
        return


    def textBox(self):
        ## pobiera uzywane epsg
        canvas = self.iface.mapCanvas()
        currentEPSG = canvas.mapRenderer().destinationCrs().authid()
        #currentEPSG = 4326 if not currentEPSG in availableEPSG

        service = wmsLinks[self.dlg.comboBox.currentIndex()]
        index = self.layerDictURL[self.dlg.comboBox_2.currentIndex()]
        self.urlWithParams = wms_separator.join((wms_url % (service),
                                            wms_layers
                                            + str(index),
                                            wms_styles,
                                            wms_format,
                                            wms_crs
                                            + currentEPSG))            

        self.dlg.textEdit.setPlainText(self.urlWithParams)
        return self.urlWithParams

    def run(self):                

        ## show the dialog
        self.dlg.show()
                
        ## wybieranie uslugi:
        if self.dlg.comboBox.count() == 0:
            self.dlg.comboBox.addItems(wmsList)

        self.dlg.comboBox.currentIndexChanged.connect(self.approveChoice)

        ## pobranie innych warstw jesli zmiana indexu
        self.dlg.pushButton.clicked.connect(self.selectedChoice)
        self.dlg.pushButton_2.clicked.connect(self.textBox)



        ## Run the dialog event loop
        result = self.dlg.exec_()       

        ## po wcisnieciu OK
        if result:                    
            # urlWithParams = wms_separator.join((wms_url % (service),
            #                                     wms_layers
            #                                     + str(index),
            #                                     wms_styles,
            #                                     wms_format,
            #                                     wms_crs
            #                                     + currentEPSG))            
            #print self.urlWithParams

            finalURL = self.textBox()

            index_2 = self.layerDict[(self.dlg.comboBox_2.currentIndex()+1)]

            ## dodanie warstwy
            rlayer = QgsRasterLayer(finalURL, wmsList[self.dlg.comboBox.currentIndex()]+'/'+index_2, 'wms')
            QgsMapLayerRegistry.instance().addMapLayer(rlayer)
            if not rlayer.isValid():
                 print "Layer failed to load!"