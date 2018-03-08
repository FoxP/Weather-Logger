# Weather Logger

## About
Simple Python script to log [METAR](https://en.wikipedia.org/wiki/METAR) and [TAF](https://en.wikipedia.org/wiki/Terminal_aerodrome_forecast) weather reports from [aviation.meteo.fr](https://aviation.meteo.fr) XML API to CSV files.

## Usage
Run `METAR_TAF_logger.py` with a `config.ini` file path as `-c` command line argument, for example from a [cron](https://en.wikipedia.org/wiki/Cron) job.  

Crontab every 10 minutes ? There you go :
```
*/10 * * * * cd /SCRIPT_PATH/ && /usr/bin/python3 /SCRIPT_PATH/METAR_TAF_logger.py -c /CONFIG_PATH/config.ini
```
:warning: The `cd /SCRIPT_PATH/` command from the example above is **MANDATORY** in a cron job if you want to use relative paths in your `config.ini` configuration file. You are welcome.

## Output
CSV file(s) containing METAR / TAF reports in the following format : `YYYY-MM-DD HH:mm METAR_OR_TAF_REPORT`  
  
For `LFPG` [ICAO](https://en.wikipedia.org/wiki/ICAO_airport_code) airport code, for example :
- `METAR_LFPG.csv` :
```
2018-02-21 16:00 METAR LFPG 211500Z 02011KT 330V110 4500 HZ NSC 05/M02 Q1021 TEMPO6000=
2018-02-22 16:00 METAR LFPG 220800Z 03014KT 010V090 3000 BR NSC M02/M04 Q1019 NOSIG=
```
- `TAF_LFPG.csv` :
```
2018-02-21 16:00 TAF AMD LFPG 211306Z 2113/2218 03012KT 4000 HZ BKN020 TEMPO 2113/2117 6000 BECMG 2202/2204 4000 BR BKN005 BECMG 2207/2209 5000 NSW SCT010BECMG 2212/2214 SCT025 TX06/2115Z TNM03/2206Z=
2018-02-22 16:00 TAF AMD LFPG 220719Z 2207/2312 03010G20KT 5000 BR NSC TEMPO 2207/2210 3000 BR TEMPO 2210/2218 4500 HZ TX04/2215Z TNM03/2306Z=
```

## Requirements
- [Python 3](https://www.python.org/)
  - [lxml](http://lxml.de/)

## Configuration
Edit the provided `config.ini` configuration file to set up the script. Everything is properly commented, easy peasy !

```ini
[General]
; Should I save TAR reports to CSV? If True, yes. If False, nope
TAF_logging = True
; Should I save METAR reports to CSV? If True, yes. If False, nope
METAR_logging = True
; List of ICAO airport codes, comma separated
ICAO_airport_codes = LFPG,LFPO,PHTO,EGLL
; Your 10 digits aeronautical code
user_code = XXXXXXXXXX

[Directory]
; CSV files will be saved to this directory path
output_directory = ./csv/
```

## XML API overview
For `LFPG` and `LFPO` [ICAO](https://en.wikipedia.org/wiki/ICAO_airport_code) airport codes for example, [aviation.meteo.fr](https://aviation.meteo.fr) XML API will output the following document :

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<groupe>
	<messages oaci="LFPG" nom="PARIS CHARLES DE GAULLE">
		<message type="METAR">
			<texte>
				<![CDATA[
					METAR LFPG 220800Z 03014KT 010V090 3000 BR NSC M02/M04 Q1019 NOSIG=
				]]>
			</texte>
		</message>
		<message type="TAFL">
			<texte>
				<![CDATA[
					TAF AMD LFPG 220719Z 2207/2312 03010G20KT 5000 BR NSC TEMPO 2207/2210 3000 BR TEMPO 2210/2218 4500 HZ TX04/2215Z TNM03/2306Z=
				]]>
			</texte>
		</message>
		<message type="SIGMET">
			<texte>
				<![CDATA[
					LFFF SIGMET 1 VALID 220600/220900 LFPW- LFFF PARIS FIR/UIR SEV TURB FCST WI N4815 E00515 - N4730 E00415 - N4630 E00445 - N4630 E00300 - N4700 E00215 - N4815 E00500 - N4815 E00515 FL170/250 MOV SW 25KT NC=
				]]>
			</texte>
		</message>
	</messages>
	<messages oaci="LFPO" nom="PARIS ORLY">
		<message type="METAR">
			<texte>
				<![CDATA[
					METAR LFPO 220800Z 03012KT 6000 NSC M01/M04 Q1019 NOSIG=
				]]>
			</texte>
		</message>
		<message type="TAFL">
			<texte>
				<![CDATA[
					TAF LFPO 220500Z 2206/2312 02010KT 8000 NSC PROB30 TEMPO 2206/2209 3000 BR SCT008 TEMPO 2211/2224 CAVOK=
				]]>
			</texte>
		</message>
		<message type="SIGMET">
			<texte>
				<![CDATA[
					LFFF SIGMET 1 VALID 220600/220900 LFPW- LFFF PARIS FIR/UIR SEV TURB FCST WI N4815 E00515 - N4730 E00415 - N4630 E00445 - N4630 E00300 - N4700 E00215 - N4815 E00500 - N4815 E00515 FL170/250 MOV SW 25KT NC=
				]]>
			</texte>
		</message>
	</messages>
</groupe>
```

## Todo
- Debug logging
- Error handling

## License
Weather Logger is released under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.fr.html).
