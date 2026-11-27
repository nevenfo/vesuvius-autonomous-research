"""EXP-018 — sélection des segments d'entraînement de reader-v2-LO (règles `select()` de reader-v2 `scripts/v2_run.py`).

Usage : python experiments/EXP-018/select.py <out.json>
Objets du corpus natif v2 de reader-v2 SAUF 0500P2, 0009B (objets de test) et 0841 (tenu à l'écart) :
0139, 0814, 0343P, 0172, mêmes sous-chaînes de résolution, plafonds et exclusions que v2_run.py ; les segments
« holdout » de v2_run (n_holdout) restent hors entraînement. Taille du surface-volume niveau 0 lue dans .zarray.
"""
import json, sys, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

S3 = 'https://vesuvius-challenge-open-data.s3.amazonaws.com/'
NS = {'s': 'http://s3.amazonaws.com/doc/2006-03-01/'}
OBJECTS = {  # copie de v2_run.py OBJECTS (scroll, sv, map, cap, n_holdout, exclusions)
    '0139': ('PHerc0139', '9.362um', '2.399um', 20, 0,
             ['20260215000000', '20260206000001', '20260220000000', '20260422000000', '20250108000004',
              '-w035_', '-w039_', '-w040_', '-w041_', '-w044_']),
    '0814': ('PHerc0814', '9.362um', '2.399um', 8, 0, ['46527']),
    '0343P': ('PHerc0343P', '8.64um', '2.215um', 8, 2, []),
    '0172': ('PHerc0172', '7.91um', '7.91um', 6, 2, []),
}


def ls(prefix):
    subs, files, tok = [], [], None
    while True:
        q = {'list-type': '2', 'prefix': prefix, 'delimiter': '/'}
        if tok:
            q['continuation-token'] = tok
        x = ET.fromstring(urllib.request.urlopen(S3 + '?' + urllib.parse.urlencode(q)).read())
        subs += [e.text for e in x.findall('s:CommonPrefixes/s:Prefix', NS)]
        files += [(c.find('s:Key', NS).text, int(c.find('s:Size', NS).text)) for c in x.findall('s:Contents', NS)]
        t = x.find('s:NextContinuationToken', NS)
        if t is None:
            return subs, files
        tok = t.text


def main(out):
    rows = []
    for obj, (scroll, svk, mapk, cap, nhold, excl) in OBJECTS.items():
        sel = []
        for s in ls(f'{scroll}/segments/')[0]:
            name = s.rstrip('/').split('/')[-1]
            if any(e in name for e in excl):
                continue
            sv = [x for x in ls(s + 'surface-volumes/')[0] if svk in x and x.endswith('.zarr/')]
            maps = [(k, sz) for k, sz in ls(s + 'ink-detection/')[1] if k.endswith('.tif') and mapk in k]
            if not sv or not maps:
                continue
            maps.sort(key=lambda t: ('new_canon' not in t[0], t[0]))
            za = json.loads(urllib.request.urlopen(S3 + urllib.parse.quote(sv[0] + '0/.zarray')).read())
            n = 1
            for d in za['shape']:
                n *= d
            sel.append({'obj': obj, 'scroll': scroll, 'seg': name, 'id': name[:40], 'sv': sv[0].rstrip('/'),
                        'sv_shape': za['shape'], 'sv_gb': round(n / 1e9, 2), 'map': maps[0][0], 'map_size': maps[0][1]})
            if len(sel) >= cap:
                break
        for i, r in enumerate(sel):
            r['role'] = 'holdout' if i >= len(sel) - nhold else 'train'
        rows += sel
        print(obj, len(sel), sum(r['role'] == 'train' for r in sel), round(sum(r['sv_gb'] for r in sel), 1), 'GB', flush=True)
    json.dump(rows, open(out, 'w'), indent=1)
    print('total', len(rows), round(sum(r['sv_gb'] for r in rows), 1), 'GB (non compressé)')


if __name__ == '__main__':
    main(sys.argv[1])
