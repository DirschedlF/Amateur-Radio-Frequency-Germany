#!/usr/bin/env python3
"""Generates src/data/bandplan.json from transcribed IARU Region 1 band plans.

Sources (see src/data/meta.js BANDPLAN_SOURCES):
  HF  : IARU Region 1 HF Band Plan, effective 16 Oct 2020 (edited by DF5JL)
  VHF : IARU Region 1 VHF band plan, effective Dec 2020 (VGC Novi Sad, ON4AVJ)
  UHF : IARU Region 1 UHF band plan, effective Dec 2020 / PDF dated 18.03.2021

Row format: (from, to, bandwidth, mode, category, usage)
  from/to : kHz for HF bands, MHz for VHF/UHF bands (as printed in the source)
  bandwidth: Hz (int) or text as printed
  category: cw | narrow | all | beacon | fm | sat | other
"""
import json, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'bandplan.json')
UA = 'unrestricted'


def hf(rows):
    out = []
    for r in rows:
        a, b, bw, m, c, u = r[:6]
        d = dict(f=round(a / 1000, 6), t=round(b / 1000, 6), bw=bw, mode=m, cat=c, use=u)
        if len(r) > 6:
            d.update(r[6])
        out.append(d)
    return out


def mhz(rows):
    out = []
    for r in rows:
        a, b, bw, m, c, u = r[:6]
        d = dict(f=a, t=b, bw=bw, mode=m, cat=c, use=u)
        if len(r) > 6:
            d.update(r[6])
        out.append(d)
    return out


bands = []

# ---------------------------------------------------------------- HF (kHz)
bands.append(dict(id='2200m', label='2200 m', title='135,7 – 137,8 kHz', src='hf', unit='kHz', rows=hf([
    (135.7, 137.8, 200, 'CW', 'cw', 'CW, QRSS and narrow band digital modes'),
]), notes=[]))
bands.append(dict(id='630m', label='630 m', title='472 – 479 kHz', src='hf', unit='kHz', rows=hf([
    (472, 475, 200, 'CW', 'cw', 'CW'),
    (475, 479, '(#) nicht festgelegt, 500 Hz empfohlen', 'Narrow band modes', 'narrow', 'CW, digimodes'),
]), notes=['Angaben sind laut Quelle „proposed usage“ (Empfehlung). Auf noch bestehende Funkfeuer (NDB) des Flugnavigationsfunks achten.']))
bands.append(dict(id='160m', label='160 m', title='1.810 – 2.000 kHz', src='hf', unit='kHz', rows=hf([
    (1810, 1838, 200, 'CW', 'cw', '1836 kHz – CW QRP Centre of Activity'),
    (1838, 1840, 500, 'Narrow band modes', 'narrow', ''),
    (1840, 1843, 2700, 'All modes (1)', 'all', 'Digimodes'),
    (1843, 2000, 2700, 'All modes (1)', 'all', ''),
]), notes=['(1) Niedrigste Dial-Einstellung für LSB-Sprache: 1843 kHz.']))
bands.append(dict(id='80m', label='80 m', title='3.500 – 3.800 kHz', src='hf', unit='kHz', rows=hf([
    (3500, 3510, 200, 'CW', 'cw', 'Priority for inter-continental operation'),
    (3510, 3560, 200, 'CW', 'cw', 'CW contest preferred; 3555 kHz – CW QRS Centre of Activity'),
    (3560, 3570, 200, 'CW', 'cw', '3560 kHz – CW QRP Centre of Activity'),
    (3570, 3580, 200, 'Narrow band modes', 'narrow', 'Digimodes'),
    (3580, 3590, 500, 'Narrow band modes', 'narrow', 'Digimodes'),
    (3590, 3600, 500, 'Narrow band modes', 'narrow', 'Digimodes, automatically controlled data stations (unattended)'),
    (3600, 3620, 2700, 'All modes (1)', 'all', 'Digimodes, automatically controlled data stations (unattended)', dict(overlap=True)),
    (3600, 3650, 2700, 'All modes (1)', 'all', 'SSB contest preferred; 3630 kHz – Digital Voice Centre of Activity', dict(overlap=True)),
    (3650, 3700, 2700, 'All modes', 'all', '3690 kHz – SSB QRP Centre of Activity'),
    (3700, 3775, 2700, 'All modes', 'all', 'SSB contest preferred; 3735 kHz – Image Centre of Activity; 3760 kHz – R1 Emergency Centre of Activity'),
    (3775, 3800, 2700, 'All modes', 'all', 'SSB contest preferred – Priority for inter-continental operation'),
]), notes=['(1) Niedrigste Dial-Einstellung für LSB-Sprache: 3603 kHz.', 'Die Segmente 3600–3620 und 3600–3650 kHz überlappen sich in der Quelle so.']))
bands.append(dict(id='60m', label='60 m', title='5.351,5 – 5.366,5 kHz', src='hf', unit='kHz', rows=hf([
    (5351.5, 5354, 200, 'CW, Narrow band modes', 'narrow', ''),
    (5354, 5366, 2700, 'All modes', 'all', 'USB recommended for voice operation (##)'),
    (5366, 5366.5, '20 (!)', 'Weak signal narrow band modes', 'narrow', ''),
]), notes=['Angaben sind laut Quelle „proposed usage“ (Empfehlung).', '(##) Höchste Dial-Einstellung für USB-Sprache: 5363 kHz.',
          'Frequenzen innerhalb der WRC-15-Zuweisung sollen nur genutzt werden, wenn keine andere Frequenz im 5-MHz-Bereich nach nationaler Genehmigung verfügbar ist. Lokale Runden und lange Ragchews sollen auf 80 m, 40 m oder die nationalen 5-MHz-Frequenzen ausweichen.']))
bands.append(dict(id='40m', label='40 m', title='7.000 – 7.200 kHz', src='hf', unit='kHz', rows=hf([
    (7000, 7040, 200, 'CW', 'cw', '7030 kHz – CW, QRP Centre of Activity'),
    (7040, 7047, 500, 'Narrow band modes', 'narrow', 'Digimodes'),
    (7047, 7050, 500, 'Narrow band modes', 'narrow', 'Digimodes, automatically controlled data stations (unattended)'),
    (7050, 7053, 2700, 'All modes (1)', 'all', 'Digimodes, automatically controlled data stations (unattended)'),
    (7053, 7060, 2700, 'All modes', 'all', 'Digimodes'),
    (7060, 7100, 2700, 'All modes', 'all', 'SSB contest preferred; 7070 kHz – Digital Voice Centre of Activity; 7090 kHz – SSB QRP Centre of Activity'),
    (7100, 7130, 2700, 'All modes', 'all', '7110 kHz – Region 1 Emergency Centre'),
    (7130, 7175, 2700, 'All modes', 'all', 'SSB contest preferred; 7165 kHz – Image Centre of Activity'),
    (7175, 7200, 2700, 'All modes', 'all', 'SSB contest preferred – Priority for inter-continental Activity'),
]), notes=['(1) Niedrigste Dial-Einstellung für LSB-Sprache: 7053 kHz.']))
bands.append(dict(id='30m', label='30 m', title='10.100 – 10.150 kHz', src='hf', unit='kHz', rows=hf([
    (10100, 10130, 200, 'CW', 'cw', '10116 kHz – CW QRP Centre of Activity'),
    (10130, 10150, 500, 'Narrow band modes', 'narrow', 'Digimodes'),
]), notes=['Der Amateurfunkdienst hat auf 30 m nur sekundären Status. Wer sich mit einer unbemannten automatisch arbeitenden Station verbindet, ist selbst für Störungsfreiheit verantwortlich.']))
bands.append(dict(id='20m', label='20 m', title='14.000 – 14.350 kHz', src='hf', unit='kHz', rows=hf([
    (14000, 14060, 200, 'CW', 'cw', 'CW contest preferred; 14055 kHz – QRS Centre of Activity'),
    (14060, 14070, 200, 'CW', 'cw', '14060 kHz – CW QRP Centre of Activity'),
    (14070, 14089, 500, 'Narrow band modes', 'narrow', 'Digimodes'),
    (14089, 14099, 500, 'Narrow band modes', 'narrow', 'Digimodes, automatically controlled data stations (unattended)'),
    (14099, 14101, '', 'International Beacon Project', 'beacon', 'Beacons exclusively'),
    (14101, 14112, 2700, 'All modes', 'all', 'Digimodes, automatically controlled data stations (unattended)'),
    (14112, 14125, 2700, 'All modes', 'all', ''),
    (14125, 14300, 2700, 'All modes', 'all', 'SSB contest preferred; 14130 kHz – Digital Voice CoA; 14195 ±5 kHz – Priority for DX-peditions; 14230 kHz – Image CoA; 14285 kHz – SSB QRP CoA'),
    (14300, 14350, 2700, 'All modes', 'all', '14300 kHz – Global Emergency Centre of Activity'),
]), notes=[]))
bands.append(dict(id='17m', label='17 m', title='18.068 – 18.168 kHz', src='hf', unit='kHz', rows=hf([
    (18068, 18095, 200, 'CW', 'cw', '18086 kHz – CW QRP Centre of Activity'),
    (18095, 18105, 500, 'Narrow band modes', 'narrow', 'Digimodes'),
    (18105, 18109, 500, 'Narrow band modes', 'narrow', 'Digimodes, automatically controlled data stations (unattended)'),
    (18109, 18111, '', 'International Beacon Project', 'beacon', 'Beacons exclusively'),
    (18111, 18120, 2700, 'All modes', 'all', 'Digimodes, automatically controlled data stations (unattended)'),
    (18120, 18168, 2700, 'All modes', 'all', '18130 kHz – SSB QRP CoA; 18150 kHz – Digital Voice CoA; 18160 kHz – Emergency CoA'),
]), notes=[]))
bands.append(dict(id='15m', label='15 m', title='21.000 – 21.450 kHz', src='hf', unit='kHz', rows=hf([
    (21000, 21070, 200, 'CW', 'cw', '21055 kHz – QRS Centre of Activity; 21060 kHz – QRP Centre of Activity'),
    (21070, 21090, 500, 'Narrow band modes', 'narrow', 'Digimodes'),
    (21090, 21110, 500, 'Narrow band modes', 'narrow', 'Digimodes, automatically controlled data stations (unattended)'),
    (21110, 21120, 2700, 'All modes', 'all', 'Digimodes, automatically controlled data stations (unattended), (not SSB)'),
    (21120, 21149, 500, 'Narrow band modes', 'narrow', ''),
    (21149, 21151, '', 'International Beacon Project', 'beacon', 'Beacons exclusively'),
    (21151, 21450, 2700, 'All modes', 'all', '21180 kHz – Digital Voice CoA; 21285 kHz – SSB QRP CoA; 21340 kHz – Image CoA; 21360 kHz – Global Emergency CoA'),
]), notes=['Seit 2020: Segment 21125–21450 kHz ist für Amateurfunksatelliten nicht exklusiv vorgesehen, Frequenzen oberhalb 21400 kHz werden klar bevorzugt.']))
bands.append(dict(id='12m', label='12 m', title='24.890 – 24.990 kHz', src='hf', unit='kHz', rows=hf([
    (24890, 24915, 200, 'CW', 'cw', '24906 kHz – CW QRP Centre of Activity'),
    (24915, 24925, 500, 'Narrow band modes', 'narrow', 'Digimodes'),
    (24925, 24929, 500, 'Narrow band modes', 'narrow', 'Digimodes, automatically controlled data stations (unattended)'),
    (24929, 24931, '', 'International Beacon Project', 'beacon', 'Beacons exclusively'),
    (24931, 24940, 2700, 'All modes', 'all', 'Digimodes, automatically controlled data stations (unattended)'),
    (24940, 24990, 2700, 'All modes', 'all', '24950 kHz – SSB QRP CoA; 24960 kHz – Digital Voice CoA'),
]), notes=[]))
bands.append(dict(id='10m', label='10 m', title='28.000 – 29.700 kHz', src='hf', unit='kHz', rows=hf([
    (28000, 28070, 200, 'CW', 'cw', '28055 kHz – QRS Centre of Activity; 28060 kHz – QRP Centre of Activity'),
    (28070, 28120, 500, 'Narrow band modes', 'narrow', 'Digimodes'),
    (28120, 28150, 500, 'Narrow band modes', 'narrow', 'Digimodes, automatically controlled data stations (unattended)'),
    (28150, 28190, 500, 'Narrow band modes', 'narrow', ''),
    (28190, 28199, '', 'International Beacon Project', 'beacon', 'Regional time shared beacons, exclusively'),
    (28199, 28201, '', 'International Beacon Project', 'beacon', 'Worldwide time shared beacons, exclusively'),
    (28201, 28225, '', 'International Beacon Project', 'beacon', 'Continuous duty beacons, exclusively'),
    (28225, 28300, 2700, 'All modes', 'all', 'Beacons'),
    (28300, 28320, 2700, 'All modes', 'all', 'Digimodes, automatically controlled data stations (unattended)'),
    (28320, 29000, 2700, 'All modes', 'all', '28330 kHz – Digital Voice CoA; 28360 kHz – SSB QRP CoA; 28680 kHz – Image CoA'),
    (29000, 29100, UA, 'All modes', 'all', ''),
    (29100, 29200, UA, 'All modes', 'fm', 'FM simplex – 10 kHz channels'),
    (29200, 29300, UA, 'All modes', 'all', 'Digimodes, automatically controlled data stations (unattended)'),
    (29300, 29510, UA, 'Satellite Links', 'sat', ''),
    (29510, 29520, '', 'Guard Channel', 'other', ''),
    (29520, 29590, 6000, 'All modes', 'fm', 'FM Repeater input (RH1–RH8)'),
    (29600, 29600, 6000, 'All modes', 'fm', 'FM Calling channel'),
    (29610, 29610, 6000, 'All modes', 'fm', 'FM Simplex Repeater (parrot, input + output)'),
    (29620, 29700, 6000, 'All modes', 'fm', 'FM Repeater output (RH1–RH8)'),
]), notes=[]))

# --------------------------------------------------------------- VHF (MHz)
bands.append(dict(id='6m', label='6 m', title='50 – 54 MHz', src='vhf', unit='MHz', rows=mhz([
    (50.000, 50.100, 500, 'Telegraphy', 'cw', 'Coordinated Beacon Project (50.000–50.010 Region 1, 50.010–50.020 Region 2, 50.020–50.030 Region 3); 50.050 centre of activity; 50.090 intercontinental centre of activity'),
    (50.100, 50.200, 2700, 'SSB and Telegraphy', 'all', '50.100–50.130 intercontinental, centre of activity 50.110; 50.130–50.200 international, centre of activity 50.150'),
    (50.200, 50.300, 2700, 'SSB and Telegraphy', 'all', 'General use; 50.285 crossband'),
    (50.300, 50.400, 2700, 'Narrow band modes, MGM', 'narrow', '50.305 PSK centre of activity; 50.310–50.320 EME centre of activity; 50.320–50.380 MS centre of activity'),
    (50.400, 50.500, 1000, 'MGM and Telegraphy', 'beacon', 'Beacons exclusive (50.401 MHz ±500 Hz WSPR beacons)'),
    (50.500, 52.000, '12 kHz', 'all mode', 'all', '50.510 SSTV; 50.520–50.540 Simplex FM Internet Voice Gateways; 50.550 Image working frequency; 50.600 RTTY (FSK); 50.620–50.750 Digital communications; 50.630 Digital Voice (DV) calling; 51.210–51.390 FM/DV Repeater Inputs; 51.410–51.590 FM/DV Simplex; 51.510 FM calling frequency; 51.810–51.990 FM repeaters output channels', dict(umbrella=True)),
    (50.500, 50.700, 'none', 'all mode', 'all', '50.540–50.580 Simplex FM/DV Internet Voice Gateways; 50.600–50.700 Digital communications, including 50.630 DV calling'),
    (50.700, 50.900, '12 kHz', 'FM/Digital voice', 'fm', '50.710–50.890 FM/DV repeater output channels'),
    (50.900, 51.200, 'none', 'all mode', 'all', 'For wideband digital experiments'),
    (51.200, 51.400, '12 kHz', 'FM/Digital voice', 'fm', '51.210–51.390 FM/DV Repeater Input channels'),
    (51.400, 52.000, 'none', 'all mode', 'fm', '51.410–51.590 FM/DV Simplex; 51.510 FM calling frequency; 51.810–51.990 FM/DV repeaters output channels; for wideband digital experiments'),
    (52.000, 54.000, '500 kHz', 'all mode', 'all', ''),
]), notes=['Das Segment 50,500–52,000 MHz ist in der Quelle zusätzlich in Unterbereiche gegliedert. Die Zeile „übergeordnet“ gibt die Gesamtangabe der Quelle wieder, die Unterzeilen darunter die Einzelsegmente.']))
bands.append(dict(id='4m', label='4 m', title='70 – 70,5 MHz', src='vhf', unit='MHz', rows=mhz([
    (70.000, 70.090, 1000, 'MGM and Telegraphy', 'beacon', 'Coordinated beacons'),
    (70.090, 70.100, 1000, 'MGM and Telegraphy', 'beacon', 'Temporary and personal beacons; 70.091 Personal WSPR beacons'),
    (70.100, 70.250, 2700, 'SSB, Telegraphy, MGM', 'all', '70.185 Crossband centre of activity; 70.200 Centre of activity CW/SSB calling; 70.250 Centre of activity MS'),
    (70.250, 70.294, '12 kHz', 'AM, FM', 'fm', '70.260 AM/FM calling; 70.270 MGM centre of activity'),
    (70.294, 70.500, '12 kHz', 'FM Channels 12,5 kHz spacing', 'fm', '70.3125 digital communications; 70.3250 digital communications; 70.4500 FM calling; 70.4875 digital communications'),
]), notes=[]))
bands.append(dict(id='2m', label='2 m', title='144 – 146 MHz', src='vhf', unit='MHz', rows=mhz([
    (144.000, 144.025, 2700, 'all mode', 'sat', 'satellite downlink only'),
    (144.025, 144.100, 500, 'Telegraphy', 'cw', '144.050 Telegraphy calling'),
    (144.100, 144.150, 500, 'MGM and Telegraphy', 'narrow', '144.100 Random MS; 144.110–144.160 CW and MGM EME'),
    (144.150, 144.400, 2700, 'SSB, Telegraphy, MGM', 'all', '144.195–144.205 Random MS SSB; 144.300 SSB centre of activity'),
    (144.400, 144.490, 500, 'MGM and Telegraphy', 'beacon', 'Beacons exclusive'),
    (144.491, 144.493, 500, 'Personal weak signal MGM, Beacons', 'beacon', 'Experimental MGM'),
    (144.500, 144.794, '20 kHz', 'All mode', 'all', '144.500 Image mode centre (SSTV, Fax, …); 144.600 Data centre of activity (MGM, RTTY, …); 144.750 ATV talk back'),
    (144.794, 144.9625, '12 kHz', 'MGM / Digital communication', 'narrow', '144.800 APRS; 144.8125, 144.8250, 144.8375, 144.8500, 144.8625 DV internet voice gateway'),
    (144.975, 145.194, '12 kHz', 'FM/Digital Voice', 'fm', 'Repeater input exclusive'),
    (145.194, 145.206, '12 kHz', 'FM/Digital Voice', 'sat', 'Space communication'),
    (145.206, 145.5625, '12 kHz', 'FM/Digital Voice', 'fm', '145.2375, 145.2875, 145.3375 FM Internet Voice Gateway; 145.375 digital voice calling; 145.500 FM calling'),
    (145.575, 145.7935, '12 kHz', 'FM/Digital Voice', 'fm', 'Repeater output exclusive'),
    (145.794, 145.806, '12 kHz', 'FM/Digital Voice', 'sat', 'Space communication'),
    (145.806, 146.000, '12 kHz', 'All mode', 'sat', 'Satellite exclusive'),
]), notes=['In dieser Tabelle der IARU ist 144,9625–144,975 MHz nicht belegt. Das DARC-Referat VHF/UHF/SHF führt außerdem einen eigenen 2-m-Bandplan (Stand 08/2017) mit abweichender Detailgliederung.',
    'Unterhalb von 144,0025 MHz soll nicht gesendet werden (Schutzabstand zur Bandkante; Fußnote r, VHF Handbook 10.03).',
    'Für FM-Sprechfunk mit Sonderstationen wie bemannten Raumfahrzeugen: 145,200 MHz Simplex oder 145,200/145,800 MHz im Split (Fußnote p, VHF Handbook 10.03).',
    'Nationale Nutzung in einigen Ländern: 144,630–144,660 MHz Linear-Transponder-Ausgänge, 144,660–144,690 MHz Linear-Transponder-Eingänge (VHF Handbook 10.03).']))

# --------------------------------------------------------------- UHF (MHz)
bands.append(dict(id='70cm', label='70 cm', title='430 – 440 MHz', src='uhf', unit='MHz', rows=mhz([
    (430.000, 431.975, '20 kHz', 'all mode', 'fm', '430.025–430.375 FM repeater output (1.6 MHz shift); 430.400–430.575 digital communications; 430.600–430.925 digital communications repeater channels; 430.925–431.025 multimode channels; 431.050–431.825 repeater input channel freqs (7.6 MHz shift); 431.625–431.975 repeater input channels (1.6 MHz shift)'),
    (432.000, 432.100, 500, 'MGM & Telegraphy', 'cw', '432.050 Telegraphy centre of activity'),
    (432.100, 432.400, 2700, 'MGM, Telegraphy & SSB', 'all', '432.200 SSB centre of activity; 432.350 Microwave talkback centre of activity; 432.370 Meteor Scatter centre of activity'),
    (432.400, 432.490, 500, 'MGM & Telegraphy', 'beacon', 'Beacons exclusive'),
    (432.191, 432.193, 500, 'EMGM', 'other', 'Experimental MGM', dict(quirk='Bereichsangabe so in der Quelle (liegt unterhalb des vorherigen Segments).')),
    (432.500, 432.975, '12 kHz', 'all mode', 'fm', '432.500 New APRS frequency; 432.600–432.9875 Repeater input Region 1 standard, 25 kHz spacing, 2 MHz shift (channel freq 432.600–432.975)'),
    (433.000, 433.375, '12 kHz', 'FM / Digital Voice repeaters', 'fm', 'Repeater input Region 1 standard, 25 kHz spacing, 1.6 MHz shift'),
    (433.400, 433.575, '12 kHz', 'FM / Digital Voice', 'fm', '433.400 SSTV (FM/AFSK); 433.450 Digital Voice calling; 433.500 FM calling'),
    (433.600, 434.000, 'none', 'all mode', 'all', '433.625–433.775 Digital communications channels; 434.000 Centre frequency of digital experiments'),
    (434.000, 434.594, '12 kHz', 'All mode – ATV', 'all', '434.450–434.575 Digital communications channels'),
    (434.594, 434.981, '12 kHz', 'All mode', 'fm', '434.600–434.9875 Repeater output (12.5 kHz spacing, 1.6 or 2 MHz shift)'),
    (435.000, 436.000, 'none', 'Satellite service', 'sat', ''),
    (436.000, 438.000, 'none', 'Satellite service & DATV/data', 'sat', 'DATV/data centre of activity'),
    (438.000, 440.000, 'none', 'All mode', 'all', '438.025–438.175 Digital communication channels; 438.200–438.525 Digital communication repeater channels; 438.550–438.625 Multi mode; 438.650–439.425 Repeater output channels (7.6 MHz shift); 439.800–439.975 Digital communication link channels'),
]), notes=[
    '434,000 MHz: LoRa-Experimente; Datenmodi mit höchstens 125 kHz Bandbreite (Fußnote p, VHF Handbook 10.03).',
    'Seit 01.01.2021 ist analoges ATV/SATV im Band 430–440 MHz nicht mehr vorgesehen; DATV mit geringer Bandbreite bleibt im Bereich 436–438 MHz möglich, dort hat der Amateurfunk-Satellitendienst Vorrang (VHF Handbook 10.03).',
    'Nationale Nutzung in einigen Ländern: 432,500–432,600 MHz Linear-Transponder-Eingänge, 432,600–432,800 MHz Linear-Transponder-Ausgänge (VHF Handbook 10.03).']))

bands.append(dict(id='23cm', label='23 cm', title='1.240 – 1.300 MHz', src='uhf', unit='MHz', rows=mhz([
    (1240.000, 1240.500, 2700, 'all modes', 'other', 'Reserved for the future'),
    (1240.500, 1240.750, 500, 'MGM & Telegraphy', 'beacon', 'Beacons (reserved for the future)'),
    (1240.750, 1241.000, '20 kHz', 'FM / Digital Voice', 'other', 'Reserved for the future'),
    (1241.000, 1243.250, '20 kHz', 'all modes', 'all', '1242.025–1242.250 repeater output; 1242.275–1242.700 repeater output; 1242.725–1243.250 Digital communications'),
    (1243.250, 1260.000, '*', '(D)ATV', 'other', '1258.150–1259.350 Repeater output'),
    (1260.000, 1270.000, '*', 'Satellite service', 'sat', ''),
    (1270.000, 1272.000, '20 kHz', 'all modes', 'all', '1270.025–1270.700 Repeater input; 1270.725–1271.250 Digital communication'),
    (1272.000, 1290.994, '*', '(D)ATV', 'other', ''),
    (1290.994, 1291.481, '20 kHz', 'FM / Digital Voice', 'fm', 'Repeater input, 25 kHz spacing'),
    (1291.494, 1296.000, '*', 'all modes', 'all', '1293.150–1294.350 repeater input R20–R68'),
    (1296.000, 1296.150, 500, 'MGM & Telegraphy', 'cw', '1296.000–1296.025 Moonbounce; 1296.138 PSK31 centre of activity'),
    (1296.150, 1296.800, 2700, 'MGM, Telegraphy & SSB', 'all', '1296.200 Narrow band centre of activity; 1296.400–1296.600 linear transponder input; 1296.500 fax; 1296.600 Narrowband data centre of activity (MGM, RTTY, …); 1296.600–1296.700 linear transponder output; 1296.741–1296.743 experimental MGM (500 Hz); 1296.750–1296.800 local beacons'),
    (1296.800, 1296.994, 500, 'MGM & Telegraphy', 'beacon', 'Beacons exclusive'),
    (1296.994, 1297.481, '20 kHz', 'FM / Digital Voice', 'fm', 'Repeater output, 25 kHz spacing'),
    (1297.494, 1297.981, '20 kHz', 'FM / Digital Voice', 'fm', '1297.500 SM20; 1297.500 centre of FM activity; 1297.725 digital voice calling frequency; 1297.900–1297.975 Simplex FM internet gateways; 1297.975 SM39'),
    (1298.000, 1299.000, '20 kHz', 'all modes', 'all', 'General mixed analogue or digital use, 25 kHz spacing channels (1298.025 RS1 … 1298.975 RS39)'),
    (1299.000, 1299.750, '150 kHz', 'all modes', 'other', '5 × 150 kHz channels for high speed digital data (DD); centres 1299.075, 1299.225, 1299.375, 1299.525, 1299.675 MHz (±75 kHz)'),
    (1299.750, 1300.000, '20 kHz', 'all modes', 'fm', '8 × 25 kHz channels (available for FM/DV use); centres 1299.775–1299.975'),
]), notes=['* Bandbreitengrenzen nach nationalen Vorschriften (Fußnote der Quelle).']))
bands.append(dict(id='13cm', label='13 cm', title='2.300 – 2.450 MHz', src='uhf', unit='MHz', rows=mhz([
    (2300.000, 2320.000, '20 kHz', 'all modes', 'all', '2304–2306 narrow band segment in countries where the 2320–2322 segment is not available; 2308–2310 narrow band segment in HB'),
    (2320.000, 2320.800, 'none', 'all modes', 'all', '2320.000–2320.025 EME; 2320.200 SSB centre of activity; 2320.750–2320.800 local beacons (10 W ERP max)'),
    (2320.800, 2321.000, '', 'MGM & Telegraphy', 'beacon', 'Beacons exclusive'),
    (2321.000, 2322.000, '20 kHz', 'FM / Digital Voice', 'fm', 'Voice simplex and repeaters'),
    (2322.000, 2400.000, 'none', 'all modes', 'all', '2322–2355 ATV; 2355–2365 Digital communications; 2365–2370 Repeaters; 2370–2392 ATV; 2392–2400 Digital communications'),
    (2400.000, 2450.000, '', 'amateur satellite service', 'sat', '2400–2402 narrow band segment in countries where the 2320–2322 segment is not available; 2427–2443 ATV if no satellite uses this segment'),
]), notes=[]))

# --------------------------------------------------------------- SHF (MHz)
bands.append(dict(id='9cm', label='9 cm', title='3.400 – 3.475 MHz', src='shf', unit='MHz', rows=mhz([
    (3400.000, 3400.800, 500, 'MGM & Telegraphy', 'narrow', '3400.100 EME centre of activity; 3400.750–3400.800 local beacons'),
    (3400.800, 3400.995, 500, 'MGM & Telegraphy', 'beacon', 'Beacons only'),
    (3401.000, 3402.000, 2700, 'all modes', 'all', ''),
    (3402.000, 3410.000, 'none', 'all modes', 'sat', 'Satellite downlinks'),
    (3410.000, 3475.000, 'none', 'all modes', 'all', ''),
]), notes=['Die Quelle nennt für das erste Segment „340,800“ als Obergrenze; gemeint ist 3400,800 MHz (passend zum Folgesegment).']))
bands.append(dict(id='6cm', label='6 cm', title='5.650 – 5.850 MHz', src='shf', unit='MHz', rows=mhz([
    (5650.000, 5668.000, 2700, 'all modes', 'sat', 'Amateur satellite service (uplink); 5668.200 narrow band centre of activity (a)'),
    (5668.000, 5670.000, 2700, 'all modes', 'sat', 'Amateur satellite service (uplink)'),
    (5670.000, 5700.000, 'none', 'MGM', 'narrow', ''),
    (5720.000, 5760.000, 'none', 'all modes', 'all', ''),
    (5760.000, 5760.800, 2700, 'all modes', 'all', '5760.200 narrow band centre of activity; 5760.750–5760.800 local beacons'),
    (5760.800, 5760.990, 'none', 'MGM & Telegraphy', 'beacon', 'Beacons only'),
    (5761.000, 5762.000, 2700, 'all modes', 'all', ''),
    (5762.000, 5790.000, 'none', 'all modes', 'all', ''),
    (5790.000, 5850.000, 'none', 'all modes', 'sat', 'Amateur satellite service (downlink)'),
]), notes=[]))
bands.append(dict(id='3cm', label='3 cm', title='10,000 – 10,500 GHz', src='shf', unit='MHz', rows=mhz([
    (10000.000, 10150.000, 'none', 'MGM', 'narrow', ''),
    (10150.000, 10250.000, 'none', 'all modes', 'all', ''),
    (10250.000, 10350.000, 'none', 'MGM', 'narrow', ''),
    (10350.000, 10368.000, 'none', 'all modes', 'all', ''),
    (10368.000, 10368.800, 2700, 'all modes', 'all', '10368.200 narrow band centre of activity; 10368.750–10368.800 local beacons'),
    (10368.800, 10368.990, '', '', 'beacon', 'Beacons only'),
    (10369.000, 10370.000, 2700, 'all modes', 'all', ''),
    (10370.000, 10450.000, '', 'all modes', 'all', ''),
    (10450.000, 10500.000, '', 'all modes', 'sat', 'Amateur satellite service; 10450–10452 narrow band modes in countries where 10368–10370 is not available'),
]), notes=[]))
bands.append(dict(id='1.2cm', label='1,2 cm', title='24,000 – 24,250 GHz', src='shf', unit='MHz', rows=mhz([
    (24000.000, 24048.000, '', 'all modes', 'all', '24025 wideband centre of activity; 24048.2 narrow band centre of activity'),
    (24048.000, 24048.800, 2700, 'all modes', 'sat', 'Amateur satellite service, narrow band modes; 24048.750–24048.800 local beacons'),
    (24048.800, 24048.995, '', 'all modes', 'beacon', 'Beacons only'),
    (24049.000, 24050.000, 2700, 'all modes', 'sat', 'Amateur satellite service, narrow band modes'),
    (24050.000, 24250.000, '', 'all modes', 'all', ''),
]), notes=['Die Quelle nennt die Zentren als „24.025“ und „24.0482“ (GHz); hier in MHz umgerechnet.']))

# ------------------------------------------------------- Microwave (MHz)
bands.append(dict(id='6mm', label='6 mm', title='47,000 – 47,200 GHz', src='uwave', unit='MHz', rows=mhz([
    (47000.000, 47088.000, 'none', 'all modes', 'all', ''),
    (47088.000, 47090.000, 2700, 'all modes', 'all', ''),
    (47090.000, 47200.000, 'none', 'all modes', 'all', ''),
]), notes=[]))
bands.append(dict(id='4mm', label='4 mm', title='75,500 – 81,500 GHz', src='uwave', unit='MHz', rows=mhz([
    (75500.000, 76000.000, 2700, 'all modes', 'sat', 'Amateur satellite service (preferred); 75976.200 preferred narrow band centre of activity'),
    (76000.000, 77500.000, 'none', 'all modes', 'all', '76032.200 narrow band centre of activity in some countries (not preferred)'),
    (77500.000, 77501.000, 2700, 'all modes', 'sat', 'Amateur satellite service; 77500.200 preferred narrow band centre of activity in countries outside the CEPT area'),
    (77501.000, 78000.000, 'none', 'all modes', 'sat', 'Amateur satellite service, preferred segment'),
    (78000.000, 81500.000, 'none', 'all modes', 'all', 'Not preferred segment'),
]), notes=['Die Zuordnung der Zeile „Amateur Satellite Service“ zu den Segmenten ist im Quell-PDF nur durch das Layout erkennbar; bitte im Original prüfen.']))
bands.append(dict(id='2.5mm', label='2,5 mm', title='122,250 – 123,000 GHz', src='uwave', unit='MHz', rows=mhz([
    (122250.000, 122251.000, 2700, 'all modes', 'narrow', 'Narrow band modes'),
    (122251.000, 123000.000, 'none', 'all modes', 'all', ''),
]), notes=[]))
bands.append(dict(id='2mm', label='2 mm', title='134,000 – 141,000 GHz', src='uwave', unit='MHz', rows=mhz([
    (134000.000, 134928.000, 'none', 'all modes', 'sat', 'Amateur satellite service'),
    (134928.000, 134930.000, 2700, 'all modes', 'narrow', '134930 narrow band centre of activity'),
    (134930.000, 136000.000, 'none', 'all modes', 'all', ''),
    (136000.000, 141000.000, 'none', 'all modes', 'all', 'Not preferred segment'),
]), notes=[]))
bands.append(dict(id='1.2mm', label='1,2 mm', title='241,000 – 250,000 GHz', src='uwave', unit='MHz', rows=mhz([
    (241000.000, 248000.000, 'none', 'all modes', 'all', 'Not preferred segment'),
    (248000.000, 248001.000, 'none', 'all modes', 'sat', 'Amateur satellite service and narrow band modes'),
    (248001.000, 250000.000, 'none', 'all modes', 'all', 'Preferred segment'),
]), notes=[]))


sources = {
    'hf': dict(title='IARU Region 1 HF Band Plan', effective='16.10.2020', editor='DF5JL', note='Erstellt nach der Region-1-Konferenz Novi Sad 2020'),
    'vhf': dict(title='IARU Region 1 VHF Band Plan', effective='Dezember 2020 (VGC Novi Sad)', editor='ON4AVJ (02.12.2020)'),
    'uhf': dict(title='IARU Region 1 UHF Band Plan', effective='Dezember 2020 (VGC Novi Sad)', editor='ON4AVJ (PDF vom 18.03.2021)'),
    'shf': dict(title='IARU Region 1 SHF Band Plan', effective='Dezember 2020 (VGC Novi Sad)', editor='ON4AVJ (02.12.2020)'),
    'uwave': dict(title='IARU Region 1 µWave Band Plan', effective='Dezember 2020 (VGC Novi Sad)', editor='ON4AVJ (02.12.2020)'),
}

hf_notes = [
    'Frequenzangaben sind Sendefrequenzen („transmitted frequencies“), nicht die des unterdrückten Trägers.',
    'Seitenband: unter 10 MHz wird LSB empfohlen, ab 10 MHz USB, auf 60 m USB.',
    'CW-Verbindungen sind in allen Bändern außerhalb der Bakensegmente üblich.',
    'AM ist in Telefoniesegmenten möglich, wenn auf Nachbarkanäle Rücksicht genommen wird.',
    'Damit keine Aussendung außerhalb des Bandes erfolgt, sollte die höchste USB-Dial-Einstellung auf 20 m bis 10 m 3 kHz unter der oberen Bandkante liegen.',
    'Contests sollen nicht auf 60 m, 30 m, 17 m und 12 m stattfinden. Nicht-Contester werden gebeten, bei großen Contests auf diese Bänder auszuweichen.',
    'Unbemannte Sendestationen sollen nur unter Operator-Kontrolle aktiviert werden (Ausnahme: mit dem IARU-Region-1-Beacon-Koordinator abgestimmte Baken) und müssen Frequenz- und Bandbreitengrenzen einhalten.',
    'Fernbedienter Betrieb: Er muss von der Regulierungsbehörde des Standortlandes erlaubt sein, und es gilt das dort zugeteilte Rufzeichen.',
]
defs = [
    ('All modes', 'CW, Telefonie und die als Centre of Activity genannten Betriebsarten sowie AM (mit Rücksicht auf Nachbarkanäle).'),
    ('Narrow band modes', 'Alle Betriebsarten bis 500 Hz Bandbreite, einschließlich CW, RTTY, PSK usw.'),
    ('Digimodes', 'Jede digitale Betriebsart innerhalb der passenden Bandbreite, z. B. RTTY, PSK, MFSK.'),
    ('Image modes', 'Analoge oder digitale Bildübertragung innerhalb der passenden Bandbreite, z. B. SSTV, FAX.'),
]

out = dict(sources=sources, hfNotes=hf_notes, definitions=[dict(term=a, text=b) for a, b in defs], bands=bands)
with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print('bands', len(bands), 'segments', sum(len(b['rows']) for b in bands))
