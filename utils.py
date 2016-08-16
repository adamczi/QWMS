# -*- coding: utf-8 -*-

availableEPSG = ['EPSG:2176', 'EPSG:2177', 'EPSG:2178', 'EPSG:2179', 'EPSG:2180', 'EPSG:4326']

xmlStructureURL_4 = './{http://www.opengis.net/wms}Capability/{http://www.opengis.net/wms}Layer/' # ISOK Hipsometria & Ortofotomapa archiwalna
xmlStructureURL_1 = xmlStructureURL_4+'{http://www.opengis.net/wms}Layer/'
xmlStructureURL_2 = xmlStructureURL_1+'{http://www.opengis.net/wms}Layer/'
xmlStructureURL_3 = xmlStructureURL_2+'{http://www.opengis.net/wms}Layer/'


layerTagTitle = '{http://www.opengis.net/wms}Title'
layerTagName = '{http://www.opengis.net/wms}Name'

## URL parameters
wms_separator = '&'
wms_url_geop = "url=http://mapy.geoportal.gov.pl/wss/service/%s/WMSServer"
wms_url_gdos = 'url=http://sdi.gdos.gov.pl/wms'
wms_layers = 'layers='
wms_styles = 'styles='
wms_format = 'format=image/png8'
wms_crs = 'crs='

## URL for GetCapabilities:
wms_getcap_geop = "http://mapy.geoportal.gov.pl/wss/service/%s/WMSServer?service=WMS&request=GetCapabilities"
wms_getcap_gdos = 'http://sdi.gdos.gov.pl/wms?request=GetCapabilities'

## Links and list of WMS Services
## taken from http://www.geoportal.gov.pl/uslugi/usluga-przegladania-wms
# mialy byc importowane z CSV ale moze pozniej :(

wmsLinks = ['img/guest/Administracyjna/MapServer',
            'pub/guest/G2_BDOT_BUD_2009/MapServer',
            'pub/guest/G2_BDOT_BUD_2010/MapServer',
            'pub/guest/G2_GO_WMS/MapServer',
            'pub/guest/G2_dyspozyt_med_WMS/MapServer',
            'pub/guest/G2_ISOK_WMS/MapServer',
            'img/guest/Krajobrazowa/MapServer',
            'pub/guest/G2_ZSIN_EUPOS_WMS/MapServer',
            'pub/guest/G2_bezrobocie_GUS_WMS/MapServer',
            'img/guest/HYDRO/MapServer',
            'img/guest/SOZO/MapServer',
            'pub/guest/kompozycjaG2_BDO_WMS/MapServer',
            'pub/guest/kompozycjaG2_VMAPL2_WMS/MapServer',
            'pub/guest/G2_NPPDL_2008_2011_WMS/MapServer',
            'img/guest/Ogolnogeograficzna/MapServer',
            'img/guest/ORTO/MapServer',
            'img/guest/ORTO_TIME/MapServer',
            'pub/guest/G2_OSNOWA_WMS/MapServer',
            'PZGIKINSP/guest/services/G2_EMUIA_WMS/MapServer',
            'PZGIKINSP/guest/services/G2_PRGAD_WMS/MapServer',
            'PZGIKINSP/guest/services/G2_PRGJT_WMS/MapServer',
            'pub/guest/G2_PRNG_WMS/MapServer',
            'img/guest/TOPO/MapServer',
            'pub/guest/G2_ASG_EUPOS_WMS/MapServer',
            'img/guest/TOPO_SERIA/MapServer',
            'pub/guest/G2_TRANSPORT_WMS/MapServer',
            'wmsimg/guest/ISOK_HipsoDyn/ImageServer',
            'img/guest/CIEN/MapServer',
            'img/guest/HIPSO/MapServer',
            'pub/guest/kompozycjaG2_TBD_WMS/MapServer',
            'pub/guest/kompozycja_BDOT10k_WMS/MapServer',
            'pub/guest/G2_SKOROWIDZE_SOZO/MapServer',
            'pub/guest/G2_SKOROWIDZE_OSNOWA/MapServer',
            'pub/guest/G2_SKOROWIDZE_ZDJECIA/MapServer',
            'pub/guest/G2_SKOROWIDZE_BDO/MapServer',
            'pub/guest/G2_SKOROWIDZE_BDOT/MapServer',
            'pub/guest/G2_SKOROWIDZE_TOPO/MapServer',
            'pub/guest/G2_SKOROWIDZE_HYDRO/MapServer',
            'pub/guest/G2_ZUS_WMS/MapServer'
            # separator
            # gdos
            ]

wmsList = ['Administracyjna Mapa Polski',
            'Budynki BDOT 2009',
            'Budynki BDOT 2010',
            'Dane o charakterze katastralnym',
            'Dyspozytornie medyczne',
            'ISOK – zasięg produktów',
            'Krajobrazowa Mapa Polski',
            'Lokalizacja stacji EUPOS',
            'Mapa bezrobocia według GUS',
            'Mapa Hydrograficzna Polski',
            'Mapa Sozologiczna Polski',
            'Mapa topograficzna (BDO)',
            'Mapa topograficzna (VMapL2)',
            'Narodowy Program Przebudowy Dróg Lokalnych 2008-2011',
            'Ogólnogeograficzna Mapa Polski',
            'Ortofotomapa',
            'Ortofotomapa - archiwalna',
            'Osnowa',
            'Ewidencja Miejscowości Ulic i Adresów ',
            'Państwowy Rejestr Granic - punkty adresowe',
            'Państwowy Rejestr Granic - jednostki terytorialne',
            'Państwowy Rejestr Nazw Geograficznych',
            'Rastrowa Mapa Topograficzna Polski',
            'Stacje ASG-EUPOS',
            'Rastrowa Mapa Topograficzna Polski – serie',
            'Transport',
            'Numeryczny Model Terenu ISOK – Hipsometria',
            'Numeryczny Model Terenu LPIS – Cieniowanie',
            'Numeryczny Model Terenu LPIS – Hipsometria',
            'Wizualizacja BDOT',
            'Wizualizacja BDOT10K',
            'Mapa Sozologiczna – skorowidze',
            'Osnowa – skorowidze',
            'Zdjęcia lotnicze – skorowidze',
            'Baza Danych Ogólnogeograficznych – skorowidze',
            'Baza Danych Obiektów Topograficznych – skorowidze',
            'Mapa topograficzna – skorowidze',
            'Mapa hydrograficzna - skorowidze',
            'Oddziały ZUS',
            # separator
            'Geoserwis GDOS'
            ]