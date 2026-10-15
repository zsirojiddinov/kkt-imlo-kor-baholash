# -*- coding: utf-8 -*-
"""ICITE-FAKT (imlo) — kichik ko'r tekshiruv DEKODI (`kor_qoida.md` bo'yicha; og'ishlar `kor_ogish.md`). READ-ONLY.

    python3 analysis/icite-2026/kor_dekod.py      # -> kor_hukm.json (+ ekranga qisqa jadval)

ASOSIY (kor_korsatma_60.md, har tartib alohida sessiya/chat):
  GPT    — kor_paket_gpt_1_natija.csv (N001–N060) + kor_paket_gpt_2_natija.csv (N061–N120), Temporary Chat
  Claude — kor_paket_claude_1_natija.csv + kor_paket_claude_2_natija.csv, ikki alohida sessiya
QO'SHIMCHA (v0, eski kor_korsatma.md; hukm va mezonga KIRMAYDI):
  Claude v0 — kor_paket_claude_natija_v0_ogish.csv (bitta faylda 120, O1)
  GPT v0    — kor_paket_gpt_{1,2}_natija_v0_ogish.csv (oddiy rejim, Reference chat history, O2)

Javob fayllariga tegilmaydi. Kalit sha256 tekshiriladi. Element javobi `1`/`2`/`tie` kalit orqali OLDIN (normallashtirishsiz)
/ KEYIN (normallashtirish bilan) / TENG ga o'giriladi. Juftlik: ikki tartib bir xil tomon -> o'sha (KEYIN = YAXSHI,
OLDIN = YOMON, TENG = teng), zid -> teng. Sabab–tanlov ziddiyati `kor_sabab_tasnif.json` dan (qo'lda tasnif, javoblarni
o'zgartirmaydi).
"""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

SIKL = Path(__file__).resolve().parent
KALIT_SHA = '0362fe54b5fade5b2a8d16527fedab895d2fb0f4130a481cabf3aa0550c00ee2'
ASOSIY = {'GPT': ['kor_paket_gpt_1_natija.csv', 'kor_paket_gpt_2_natija.csv'],
          'Claude': ['kor_paket_claude_1_natija.csv', 'kor_paket_claude_2_natija.csv']}
QOSHIMCHA = {'GPT_v0': ['kor_paket_gpt_1_natija_v0_ogish.csv', 'kor_paket_gpt_2_natija_v0_ogish.csv'],
             'Claude_v0': ['kor_paket_claude_natija_v0_ogish.csv']}
YOMON_CHEGARA = 6          # 60 juftlikdan <= 10 %
TERS = {'oldin': 'keyin', 'keyin': 'oldin'}


def _kalit():
    b = (SIKL / 'kor_kalit.json').read_bytes()
    assert hashlib.sha256(b).hexdigest() == KALIT_SHA, 'kalit sha256 mos emas'
    return json.loads(b)['qator']


def _paket():
    with open(SIKL / 'kor_paket.csv', encoding='utf-8', newline='') as f:
        return {r['id']: r for r in csv.DictReader(f)}


def _oqi(nom):
    xom = (SIKL / nom).read_bytes()
    with open(SIKL / nom, encoding='utf-8-sig', newline='') as f:      # GPT v0 fayllarida UTF-8 BOM bor (o'qishda)
        q = list(csv.DictReader(f))
    return q, hashlib.sha256(xom).hexdigest()


def tomon(choice, bir):
    """`1`/`2`/`tie` -> oldin/keyin/teng (`bir` — 1-o'rindagi tomon)."""
    c = choice.strip().lower()
    if c == 'tie':
        return 'teng'
    assert c in ('1', '2'), choice
    return bir if c == '1' else TERS[bir]


def model(fayllar, K):
    javob, sha, tartib_sanoq = {}, {}, {}
    for nom in fayllar:
        q, h = _oqi(nom)
        sha[nom] = h
        assert all(r['id'] not in javob for r in q), f'takror id {nom}'
        for r in q:
            javob[r['id']] = r
    assert set(javob) == set(K), f'id lar kalit bilan mos emas: {sorted(set(K) ^ set(javob))[:5]}'
    ids = sorted(K)
    tartib = {1: ids[:60], 2: ids[60:]}
    el = {i: tomon(javob[i]['choice'], K[i]['1']) for i in ids}
    for t, tids in tartib.items():
        c = Counter(el[i] for i in tids)
        tartib_sanoq[t] = {'yaxshi': c['keyin'], 'teng': c['teng'], 'yomon': c['oldin']}
    poz = Counter(javob[i]['choice'].strip().lower() for i in ids)
    juft = {}
    for i in ids:
        juft.setdefault(K[i]['juft'], []).append(i)
    hukm, zid = {}, 0
    for j, (a, b) in sorted(juft.items()):
        ta, tb = el[a], el[b]
        if ta == tb:
            hukm[j] = {'keyin': 'yaxshi', 'oldin': 'yomon', 'teng': 'teng'}[ta]
        else:
            hukm[j] = 'teng'
            zid += 1
    c = Counter(hukm.values())
    eng = max(poz['1'], poz['2']) / len(ids)
    yaroqsiz = eng > 0.95 or zid / len(juft) > 0.5
    return {'sha256': sha, 'tartib': tartib_sanoq,
            'ikki_tartib': {'yaxshi': c['yaxshi'], 'teng': c['teng'], 'yomon': c['yomon']},
            'pozitsiya': dict(poz), 'eng_kop_pozitsiya_%': round(100 * eng, 1),
            'tartib_zid': zid, 'tartib_zid_%': round(100 * zid / len(juft), 1),
            'yaroqsiz': yaroqsiz, 'juftlik': hukm, 'element': el,
            'javob': {i: {'choice': javob[i]['choice'], 'reason': javob[i]['reason']} for i in ids}}


def mezon(s):
    return s['yaxshi'] >= 2 * s['yomon'] and s['yomon'] <= YOMON_CHEGARA


def main():
    K = _kalit()
    P = _paket()
    juftlar = sorted({v['juft'] for v in K.values()})
    jkalit = {v['juft']: v['kalit'] for v in K.values()}
    jturi = {v['juft']: '+'.join(v['turlar']) for v in K.values()}

    def matn(j):
        i = next(i for i in sorted(K) if K[i]['juft'] == j)
        r, bir = P[i], K[i]['1']
        return {'uz': r['uzbek'], 'oldin': r['translation_1'] if bir == 'oldin' else r['translation_2'],
                'keyin': r['translation_2'] if bir == 'oldin' else r['translation_1']}

    M = {m: model(f, K) for m, f in {**ASOSIY, **QOSHIMCHA}.items()}
    g, c = M['GPT']['juftlik'], M['Claude']['juftlik']
    kel = [j for j in juftlar if g[j] == c[j]]
    umumiy = Counter(g[j] for j in kel)
    umumiy = {'yaxshi': umumiy['yaxshi'], 'teng': umumiy['teng'], 'yomon': umumiy['yomon'],
              'kelishilmagan': len(juftlar) - len(kel)}
    yaroqli = [m for m in ASOSIY if not M[m]['yaroqsiz']]
    matritsa = Counter(f"{g[j]}|{c[j]}" for j in juftlar)
    el_kel = sum(M['GPT']['element'][i] == M['Claude']['element'][i] for i in K)
    yomon_ids = sorted({j for m in ASOSIY for j in juftlar if M[m]['juftlik'][j] == 'yomon'})
    yomon = [dict(juft=j, kalit=jkalit[j], tur=jturi[j], GPT=g[j], Claude=c[j], **matn(j),
                  element={m: {i: M[m]['javob'][i] for i in sorted(K) if K[i]['juft'] == j} for m in ASOSIY})
             for j in yomon_ids]
    sabab = json.loads((SIKL / 'kor_sabab_tasnif.json').read_text(encoding='utf-8')) \
        if (SIKL / 'kor_sabab_tasnif.json').exists() else None
    qoshimcha = {}
    for m in QOSHIMCHA:
        a = m.split('_')[0]
        qoshimcha[m] = {'ikki_tartib': M[m]['ikki_tartib'], 'tartib': M[m]['tartib'], 'yaroqsiz': M[m]['yaroqsiz'],
                        'tartib_zid': M[m]['tartib_zid'], 'eng_kop_pozitsiya_%': M[m]['eng_kop_pozitsiya_%'],
                        'mezon_yakka': mezon(M[m]['ikki_tartib']),
                        'asosiy_bilan_juftlik_aynan': sum(M[m]['juftlik'][j] == M[a]['juftlik'][j] for j in juftlar),
                        'asosiy_bilan_element_aynan': sum(M[m]['element'][i] == M[a]['element'][i] for i in K)}
    v0g, v0c = M['GPT_v0']['juftlik'], M['Claude_v0']['juftlik']
    v0kel = Counter(v0g[j] for j in juftlar if v0g[j] == v0c[j])
    qoshimcha['umumiy_v0'] = {'yaxshi': v0kel['yaxshi'], 'teng': v0kel['teng'], 'yomon': v0kel['yomon'],
                              'kelishilmagan': sum(v0g[j] != v0c[j] for j in juftlar)}
    out = {'kalit_sha256': KALIT_SHA,
           'asosiy': {m: {k: M[m][k] for k in ('sha256', 'tartib', 'ikki_tartib', 'pozitsiya', 'eng_kop_pozitsiya_%',
                                               'tartib_zid', 'tartib_zid_%', 'yaroqsiz')} | {'mezon_yakka': mezon(M[m]['ikki_tartib'])}
                      for m in ASOSIY},
           'yaroqli': yaroqli,
           'kelishuv': {'juftlik_aynan': len(kel), 'element_aynan': el_kel, 'matritsa_GPT|Claude': dict(matritsa)},
           'umumiy': umumiy, 'mezon': {'qoida': 'yaxshi >= 2 x yomon VA yomon <= 6 (umumiy hukm)',
                                       'natija': mezon(umumiy)},
           'tur_kesimi': {t: dict(Counter(f"{g[j]}|{c[j]}" for j in juftlar if jturi[j] == t)) for t in sorted(set(jturi.values()))},
           'yomon': yomon, 'sabab_tanlov_zid': sabab,
           'qoshimcha_v0': {**qoshimcha, 'sha256': {m: M[m]['sha256'] for m in QOSHIMCHA}},
           'juftlik': {j: {'kalit': jkalit[j], 'tur': jturi[j], **{m: M[m]['juftlik'][j] for m in M}} for j in juftlar}}
    (SIKL / 'kor_hukm.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for m in M:
        print(m, M[m]['tartib'], M[m]['ikki_tartib'], 'zid', M[m]['tartib_zid'], 'poz', M[m]['eng_kop_pozitsiya_%'],
              'yaroqsiz', M[m]['yaroqsiz'])
    print('umumiy', umumiy, 'mezon', mezon(umumiy), '| kelishuv juft', len(kel), 'element', el_kel)
    print('yomon', [(y['juft'], y['kalit'], y['GPT'], y['Claude']) for y in yomon])


if __name__ == '__main__':
    main()
