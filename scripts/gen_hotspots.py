#!/usr/bin/env python3
"""Generates src/data/hotspots.json: frequencies of activity per band and mode.

Every entry carries a source key (see SOURCES). Only values that can be traced
to a source are listed; never add a value without one.

  iaru  : IARU Region 1 band plans (centre of activity / calling frequency),
          identical to the transcription in scripts/gen_bandplan.py
  wsjtx : WSJT-X Working Frequencies table (defaults), exported with
          Settings > Frequencies > Save as .qrg.json and stored in
          scripts/data/wsjtx_3.2.1_frequencies.json (FT8, FT4, WSPR, FT2, FST4,
          FST4W, JT65, JT9, JT4, Q65, MSK144, Echo). Region 1 view: rows for
          region "All" and "Region 1"; for FT8, FT4 and FT2 only the preferred
          (default) frequency per band.

Cross-checks done: FT8 160 m to 10 m agree with DARC DL-Rundspruch 33/2017
(DF5JL); FT4 10.140 and 14.080 MHz agree with the WSJT-X 2.7.0 User Guide.

Not included: WSPR on 6 m (WSJT-X lists 50.293 MHz for Region 2 and 3 only),
FT8/FT4/FT2 alternates that are not preferred, FreqCal (calibration
stations), JTTY and the QO-100 transponder rows.

Entry format of the handwritten rows: (band id, frequency, type, text, source)
  frequency: kHz for HF bands, MHz for all others (as printed in the source)
"""
import json, os

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'src', 'data', 'hotspots.json')
PLAN = os.path.join(ROOT, 'src', 'data', 'bandplan.json')

SOURCES = {
    'iaru': dict(
        short='IARU R1',
        level='Bandplan',
        text='IARU Region 1 Bandplan (HF 16.10.2020, VHF/UHF/SHF Dezember 2020)',
    ),
    'wsjtx': dict(
        short='WSJT-X 3.2.1',
        level='Primärquelle',
        text='WSJT-X 3.2.1 (Build 261001), Tabelle „Working Frequencies“ (Standardwerte), exportiert am 12.10.2026; '
        'FT8 160 m bis 10 m zusätzlich durch DARC DL-Rundspruch 33/2017 bestätigt',
    ),
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


# (band, frequency, type, text, source)
H = 'iaru'
rows = [
    # ---- 160 m (kHz)
    ('160m', 1836, 'qrp', 'CW QRP Centre of Activity', H),
    # ---- 80 m
    ('80m', 3555, 'cw', 'CW QRS Centre of Activity', H),
    ('80m', 3560, 'qrp', 'CW QRP Centre of Activity', H),
    ('80m', 3630, 'dv', 'Digital Voice Centre of Activity', H),
    ('80m', 3690, 'qrp', 'SSB QRP Centre of Activity', H),
    ('80m', 3735, 'image', 'Image Centre of Activity', H),
    ('80m', 3760, 'emergency', 'Region 1 Emergency Centre of Activity', H),
    # ---- 40 m
    ('40m', 7030, 'qrp', 'CW QRP Centre of Activity', H),
    ('40m', 7070, 'dv', 'Digital Voice Centre of Activity', H),
    ('40m', 7090, 'qrp', 'SSB QRP Centre of Activity', H),
    ('40m', 7110, 'emergency', 'Region 1 Emergency Centre', H),
    ('40m', 7165, 'image', 'Image Centre of Activity', H),
    # ---- 30 m
    ('30m', 10116, 'qrp', 'CW QRP Centre of Activity', H),
    # ---- 20 m
    ('20m', 14055, 'cw', 'QRS Centre of Activity', H),
    ('20m', 14060, 'qrp', 'CW QRP Centre of Activity', H),
    ('20m', 14130, 'dv', 'Digital Voice Centre of Activity', H),
    ('20m', 14195, 'dx', 'Priority for DX-peditions (±5 kHz)', H),
    ('20m', 14230, 'image', 'Image Centre of Activity', H),
    ('20m', 14285, 'qrp', 'SSB QRP Centre of Activity', H),
    ('20m', 14300, 'emergency', 'Global Emergency Centre of Activity', H),
    # ---- 17 m
    ('17m', 18086, 'qrp', 'CW QRP Centre of Activity', H),
    ('17m', 18130, 'qrp', 'SSB QRP Centre of Activity', H),
    ('17m', 18150, 'dv', 'Digital Voice Centre of Activity', H),
    ('17m', 18160, 'emergency', 'Emergency Centre of Activity', H),
    # ---- 15 m
    ('15m', 21055, 'cw', 'QRS Centre of Activity', H),
    ('15m', 21060, 'qrp', 'CW QRP Centre of Activity', H),
    ('15m', 21180, 'dv', 'Digital Voice Centre of Activity', H),
    ('15m', 21285, 'qrp', 'SSB QRP Centre of Activity', H),
    ('15m', 21340, 'image', 'Image Centre of Activity', H),
    ('15m', 21360, 'emergency', 'Global Emergency Centre of Activity', H),
    # ---- 12 m
    ('12m', 24906, 'qrp', 'CW QRP Centre of Activity', H),
    ('12m', 24950, 'qrp', 'SSB QRP Centre of Activity', H),
    ('12m', 24960, 'dv', 'Digital Voice Centre of Activity', H),
    # ---- 10 m
    ('10m', 28055, 'cw', 'QRS Centre of Activity', H),
    ('10m', 28060, 'qrp', 'CW QRP Centre of Activity', H),
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
    ('6m', 50.401, 'digital', 'WSPR-Baken (±500 Hz)', H),
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


WSJTX = os.path.join(os.path.dirname(__file__), 'data', 'wsjtx_3.2.1_frequencies.json')


def wsjtx_entries(bands):
    data = json.load(open(WSJTX, encoding='utf-8'))
    out = []
    for r in data['frequencies']:
        if r['region'] not in ('All', 'Region 1'):
            continue
        if r['mode'] in ('FT8', 'FT4', 'FT2') and not r['preferred']:
            continue
        mhz = r['mhz']
        hit = [
            b for b in bands.values()
            if min(x['f'] for x in b['rows']) <= mhz <= max(x['t'] for x in b['rows'])
        ]
        assert len(hit) == 1, (r, [b['id'] for b in hit])
        suffix = ' (Region 1)' if r['region'] == 'Region 1' else ''
        extra = f" ({r['description']})" if r['description'] else ''
        typ = 'digital' if r['mode'] in ('FT8', 'FT4', 'FT2', 'WSPR') else 'weak'
        label = 'Echo-Test (EME)' if r['mode'] == 'Echo' else f"{r['mode']}, Dial-Frequenz (USB)"
        out.append(dict(band=hit[0]['id'], f=mhz, type=typ, text=f"{label}{extra}{suffix}", src='wsjtx'))
    return out


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
    out.extend(wsjtx_entries(bands))
    out.sort(key=lambda e: (e['f'], e['text']))
    data = dict(sources=SOURCES, types=TYPES, entries=out)
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    print(f'{len(out)} entries -> {os.path.normpath(OUT)}')


if __name__ == '__main__':
    main()
