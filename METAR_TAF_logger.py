#!/usr/bin/env python
# -*- coding: utf-8 -*-

#	##### BEGIN GPL LICENSE BLOCK #####
#
#	This program is free software; you can redistribute it and/or
#	modify it under the terms of the GNU General Public License
#	as published by the Free Software Foundation; either version 2
#	of the License, or (at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
# 	along with this program; if not, write to the Free Software Foundation,
#	Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#	##### END GPL LICENSE BLOCK #####

#	Name :
#				Weather Logger
# 	Author :
#				▄▄▄▄▄▄▄  ▄ ▄▄ ▄▄▄▄▄▄▄
#				█ ▄▄▄ █ ██ ▀▄ █ ▄▄▄ █
#				█ ███ █ ▄▀ ▀▄ █ ███ █
#				█▄▄▄▄▄█ █ ▄▀█ █▄▄▄▄▄█
#				▄▄ ▄  ▄▄▀██▀▀ ▄▄▄ ▄▄
#				 ▀█▄█▄▄▄█▀▀ ▄▄▀█ █▄▀█
#				 █ █▀▄▄▄▀██▀▄ █▄▄█ ▀█
#				▄▄▄▄▄▄▄ █▄█▀ ▄ ██ ▄█
#				█ ▄▄▄ █  █▀█▀ ▄▀▀  ▄▀
#				█ ███ █ ▀▄  ▄▀▀▄▄▀█▀█
#				█▄▄▄▄▄█ ███▀▄▀ ▀██ ▄

# DEPENDENCIES

import sys
import os.path
import argparse
import datetime
import configparser
import urllib.request
from lxml import etree

# CONFIGURATION

PROGRAM_NAME = "Weather Logger"
PROGRAM_VERSION = "1.0"

argParser = argparse.ArgumentParser(description=PROGRAM_NAME + " " + PROGRAM_VERSION)
argParser.add_argument('-c', '--config', metavar='PATH', help='"config.ini" configuration file path', required=True)
args = vars(argParser.parse_args())
sConfigFilePath = args['config']

if not os.path.isfile(sConfigFilePath):
	print("Invalid INI configuration file path")
	sys.exit(1)
try:
	configObj = configparser.RawConfigParser()
	configObj.read(sConfigFilePath)
except:
	print("Badly written INI configuration file")
	sys.exit(1)

# URL OPENING

sLocationCodes = configObj.get('General', 'ICAO_airport_codes').replace(" ", "").split(",")

sWeatherDataUrl = "http://aviation.meteo.fr/FR/aviation/serveur_donnees.jsp?ID=" + configObj.get('General', 'user_code') + "&TYPE_DONNEES=OPMET&LIEUID=" + "%7C".join(sLocationCodes) + "&METAR=oui&TAF=Deux"
oFile = urllib.request.urlopen(sWeatherDataUrl)
sFileContent = oFile.read()

# XML PARSING

rootXML = etree.fromstring(sFileContent)
if not rootXML.find('code') is None:
	print("Invalid 10-digits aeronautical code")
	sys.exit(1)

for sLocationCode in sLocationCodes:

	# DATA EXTRACTION

	sDataMETAR = rootXML.xpath("///messages[attribute::oaci='" + sLocationCode + "']/message[attribute::type='METAR']/texte")[0].text.replace('\n', '') + '\n'
	sDataTAF = rootXML.xpath("///messages[attribute::oaci='" + sLocationCode + "']/message[attribute::type='TAFL']/texte")[0].text.replace('\n', '') + '\n'

	# CSV FILES

	sOutputPath = configObj.get('Directory', 'output_directory')
	if not os.path.exists(sOutputPath):
		os.makedirs(sOutputPath)
	sDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M ')

	if configObj.getboolean('General', 'METAR_logging'):
		csvFileMETAR = open(os.path.join(sOutputPath, "METAR_" + sLocationCode + ".csv"), 'a')
		csvFileMETAR.write(sDateTime + sDataMETAR)
		csvFileMETAR.close()

	if configObj.getboolean('General', 'TAF_logging'):
		csvFileTAF = open(os.path.join(sOutputPath, "TAF_" + sLocationCode + ".csv"), 'a')
		csvFileTAF.write(sDateTime + sDataTAF)
		csvFileTAF.close()
