# -*- coding: utf-8 -*-

availableEPSG = [2176, 2177, 2178, 2179, 2180, 4326]

xmlStructureURL_1 = './{http://www.opengis.net/wms}Capability/{http://www.opengis.net/wms}Layer/{http://www.opengis.net/wms}Layer/'
xmlStructureURL_2 = './{http://www.opengis.net/wms}Capability/{http://www.opengis.net/wms}Layer/{http://www.opengis.net/wms}Layer/{http://www.opengis.net/wms}Layer/'


## URL to download WMS
wms_separator = '&'
wms_url = "url=http://mapy.geoportal.gov.pl/wss/service/%s/MapServer/WMSServer"
wms_layers = 'layers='
wms_styles = 'styles='
wms_format = 'format=image/png'
wms_crs = 'crs='

## URL for GetCapabilities:
wms_getcap_url = "http://mapy.geoportal.gov.pl/wss/service/%s/MapServer/WMSServer?service=WMS&request=GetCapabilities"

## Links and list of WMS Services:

wmsLinks = ['img/guest/Administracyjna',
			'pub/guest/G2_BDOT_BUD_2009',
			'pub/guest/G2_BDOT_BUD_2010',
			'pub/guest/G2_GO_WMS',
			'pub/guest/G2_dyspozyt_med_WMS',
			'pub/guest/G2_ISOK_WMS',
			'img/guest/Krajobrazowa',
			'pub/guest/G2_ZSIN_EUPOS_WMS',
			'pub/guest/G2_bezrobocie_GUS_WMS',
			'img/guest/HYDRO',
			'img/guest/SOZO',
			'pub/guest/kompozycjaG2_BDO_WMS',
			'pub/guest/kompozycjaG2_VMAPL2_WMS',
			'pub/guest/G2_NPPDL_2008_2011_WMS',
			'img/guest/Ogolnogeograficzna',
			'img/guest/ORTO',
			'img/guest/ORTO_TIME',
			'pub/guest/G2_OSNOWA_WMS'
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
			'Oddziały ZUS'
			]