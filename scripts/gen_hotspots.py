#!/usr/bin/env python3
"""Generates src/data/hotspots.json: frequencies of activity per band and mode.

Every entry carries a source key (see SOURCES). Only values that can be traced
to a source are listed; never add a value without one.

  iaru   : IARU Region 1 band plans (centre of activity / calling frequency),
           identical to the transcription in scripts/gen_bandplan.py
  darc17 : DARC DL-Rundspruch 33/2017 (DF5JL, DARC HF-Referat): FT8 dial
           frequencies of WSJT-X v1.8 for 160 m to 10 m

Not included on purpose (no verified source yet): FT4, WSPR, FT8 on 60 m, 6 m
and 2 m.

Entry format: (band id, frequency, type, text)
  frequency: kHz for HF bands, MHz for all others (as printed in the source)
"""
import json, os

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'src', 'data', 'hotspots.json')
PLAN = os.path.join(ROOT, 'src', 'data', 'bandplan.json')

SOURCES = {
    'iaru': 'IARU Region 1 Bandplan (HF 16.10.2020, VHF/UHF/SHF Dezember 2020)',
    'darc17': 'DARC DL-Rundspruch 33/2017 (DF5JL, HF-Referat): FT8-Dial-Frequenzen',
}

TYPES = {
    'cw': 'CW',
    'qrp': 'QRP',
    'digital': 'Digimodes',
    'image': 'SSTV / Bild',
    'dv': 'Digital Voice',
    'ssb': 'SSB',
    'fm': 'FM',
    'dx': 'DX',
    'emergency': 'Notfunk',
    'aprs': 'APRS',
    'weak': 'Weak Signal',
}

FT8 = 'FT8, Dial-Frequenz (USB)'

# (band, frequency, type, text, source)
H = 'iaru'
D = 'darc17'
rows = [
    # ---- 160 m (kHz)
    ('160m', 1836, 'qrp', 'CW QRP Centre of Activity', H),
    ('160m', 1840, 'digital', FT8, D),
    # ---- 80 m
    ('80m', 3555, 'cw', 'CW QRS Centre of Activity', H),
    ('80m', 3560, 'qrp', 'CW QRP Centre of Activity', H),
    ('80m', 3573, 'digital', FT8, D),
    ('80m', 3630, 'dv', 'Digital Voice Centre of Activity', H),
    ('80m', 3690, 'qrp', 'SSB QRP Centre of Activity', H),
    ('80m', 3735, 'image', 'Image Centre of Activity', H),
    ('80m', 3760, 'emergency', 'Region 1 Emergency Centre of Activity', H),
    # ---- 40 m
    ('40m', 7030, 'qrp', 'CW QRP Centre of Activity', H),
    ('40m', 7070, 'dv', 'Digital Voice Centre of Activity', H),
    ('40m', 7074, 'digital', FT8, D),
    ('40m', 7090, 'qrp', 'SSB QRP Centre of Activity', H),
    ('40m', 7110, 'emergency', 'Region 1 Emergency Centre', H),
    ('40m', 7165, 'image', 'Image Centre of Activity', H),
    # ---- 30 m
    ('30m', 10116, 'qrp', 'CW QRP Centre of Activity', H),
    ('30m', 10136, 'digital', FT8, D),
    # ---- 20 m
    ('20m', 14055, 'cw', 'QRS Centre of Activity', H),
    ('20m', 14060, 'qrp', 'CW QRP Centre of Activity', H),
    ('20m', 14074, 'digital', FT8, D),
    ('20m', 14130, 'dv', 'Digital Voice Centre of Activity', H),
    ('20m', 14195, 'dx', 'Priority for DX-peditions (±5 kHz)', H),
    ('20m', 14230, 'image', 'Image Centre of Activity', H),
    ('20m', 14285, 'qrp', 'SSB QRP Centre of Activity', H),
    ('20m', 14300, 'emergency', 'Global Emergency Centre of Activity', H),
    # ---- 17 m
    ('17m', 18086, 'qrp', 'CW QRP Centre of Activity', H),
    ('17m', 18100, 'digital', FT8, D),
    ('17m', 18130, 'qrp', 'SSB QRP Centre of Activity', H),
    ('17m', 18150, 'dv', 'Digital Voice Centre of Activity', H),
    ('17m', 18160, 'emergency', 'Emergency Centre of Activity', H),
    # ---- 15 m
    ('15m', 21055, 'cw', 'QRS Centre of Activity', H),
    ('15m', 21060, 'qrp', 'CW QRP Centre of Activity', H),
    ('15m', 21074, 'digital', FT8, D),
    ('15m', 21180, 'dv', 'Digital Voice Centre of Activity', H),
    ('15m', 21285, 'qrp', 'SSB QRP Centre of Activity', H),
    ('15m', 21340, 'image', 'Image Centre of Activity', H),
    ('15m', 21360, 'emergency', 'Global Emergency Centre of Activity', H),
    # ---- 12 m
    ('12m', 24906, 'qrp', 'CW QRP Centre of Activity', H),
    ('12m', 24915, 'digital', FT8, D),
    ('12m', 24950, 'qrp', 'SSB QRP Centre of Activity', H),
    ('12m', 24960, 'dv', 'Digital Voice Centre of Activity', H),
    # ---- 10 m
    ('10m', 28055, 'cw', 'QRS Centre of Activity', H),
    ('10m', 28060, 'qrp', 'CW QRP Centre of Activity', H),
    ('10m', 28074, 'digital', FT8, D),
    ('10m', 28330, 'dv', 'Digital Voice Centre of Activity', H),
    ('10m', 28360, 'qrp', 'SSB QRP Centre of Activity', H),
    ('10m', 28680, 'image', 'Image Centre of Activity', H),
    ('10m', 29600, 'fm', 'FM Calling channel', H),
    # ---- 6 m (MHz)
    ('6m', 50.050, 'cw', 'Telegraphy Centre of Activity', H),
    ('6m', 50.090, 'dx', 'Intercontinental Centre of Activity (CW)', H),
    ('6m', 50.110, 'dx', 'Intercontinental SSB Centre of Activity (DX-Anruf)', H),
    ('6m', 50.150, 'ssb', 'International SSB/CW Centre of Activity', H),
    ('6m', 50.305, 'digital', 'PSK Centre of Activity', H),
    ('6m', 50.510, 'image', 'SSTV', H),
    ('6m', 50.600, 'digital', 'RTTY (FSK)', H),
    ('6m', 50.630, 'dv', 'Digital Voice (DV) calling', H),
    ('6m', 51.510, 'fm', 'FM calling frequency', H),
    # ---- 4 m
    ('4m', 70.200, 'ssb', 'Centre of Activity CW/SSB calling', H),
    ('4m', 70.250, 'weak', 'Centre of Activity Meteor Scatter', H),
    ('4m', 70.260, 'fm', 'AM/FM calling', H),
    ('4m', 70.450, 'fm', 'FM calling', H),
    # ---- 2 m
    ('2m', 144.050, 'cw', 'Telegraphy calling', H),
    ('2m', 144.100, 'weak', 'Random MS', H),
    ('2m', 144.300, 'ssb', 'SSB Centre of Activity', H),
    ('2m', 144.500, 'image', 'Image mode centre (SSTV, Fax, …)', H),
    ('2m', 144.600, 'digital', 'Data centre of activity (MGM, RTTY, …)', H),
    ('2m', 144.800, 'aprs', 'APRS', H),
    ('2m', 145.375, 'dv', 'Digital voice calling', H),
    ('2m', 145.500, 'fm', 'FM calling', H),
    # ---- 70 cm
    ('70cm', 432.050, 'cw', 'Telegraphy Centre of Activity', H),
    ('70cm', 432.200, 'ssb', 'SSB Centre of Activity', H),
    ('70cm', 432.370, 'weak', 'Meteor Scatter Centre of Activity', H),
    ('70cm', 432.500, 'aprs', 'New APRS frequency', H),
    ('70cm', 433.400, 'image', 'SSTV (FM/AFSK)', H),
    ('70cm', 433.450, 'dv', 'Digital Voice calling', H),
    ('70cm', 433.500, 'fm', 'FM calling', H),
    # ---- 23 cm
    ('23cm', 1296.200, 'ssb', 'Narrow band centre of activity', H),
    ('23cm', 1296.500, 'image', 'Fax', H),
    ('23cm', 1296.600, 'digital', 'Narrowband data centre of activity (MGM, RTTY, …)', H),
    ('23cm', 1297.500, 'fm', 'Centre of FM activity', H),
    ('23cm', 1297.725, 'dv', 'Digital voice calling frequency', H),
    # ---- 13 cm / 6 cm / 3 cm
    ('13cm', 2320.200, 'ssb', 'SSB Centre of Activity', H),
    ('6cm', 5760.200, 'ssb', 'Narrow band centre of activity', H),
    ('3cm', 10368.200, 'ssb', 'Narrow band centre of activity', H),
]


def main():
    plan = json.load(open(PLAN, encoding='utf-8'))
    bands = {b['id']: b for b in plan['bands']}
    out = []
    for band, freq, typ, text, src in rows:
        assert typ in TYPES and src in SOURCES, (band, freq, typ, src)
        b = bands[band]
        mhz = round(freq / 1000, 6) if b['unit'] == 'kHz' else freq
        lo = min(r['f'] for r in b['rows'])
        hi = max(r['t'] for r in b['rows'])
        assert lo <= mhz <= hi, f'{band} {freq} outside {lo}-{hi}'
        out.append(dict(band=band, f=mhz, type=typ, text=text, src=src))
    out.sort(key=lambda e: e['f'])
    data = dict(sources=SOURCES, types=TYPES, entries=out)
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    print(f'{len(out)} entries -> {os.path.normpath(OUT)}')


if __name__ == '__main__':
    main()
