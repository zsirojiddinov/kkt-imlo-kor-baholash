# O'zbekcha imlo normallashtirish: yakuniy ko'r juftlik baholash materiallari

Maqola: «O'zbekcha imlo normallashtirish» (o'zbekcha nusxa), 2.6-bo'lim (usul), 3.4-bo'lim va 5-jadval (natija),
B ilova (ko'rsatma). Bu arxiv 5-jadvaldagi sonlarni, Koen κ va Gwet AC1 ni qayta hisoblash uchun.

Barcha fayllar loyiha repozitoriyasidan (`analysis/icite-2026/`) **o'zgartirmasdan, bayt-aynan** nusxa olingan.
Har fayl repozitoriyadagi commit qilingan blob bilan tekshirildi (2026-10-15). Fayl nomlari ham asl holida qoldirilgan.

## Tizim holati

| | |
|---|---|
| Baholash sanasi | 2026-10-08 |
| Tarjima tizimi | production `2026.10.08-49` (kod commiti `31f5252`) |
| Lug'at bazasi (DB) md5 | `9d3adf8d` (`9d3adf8d40dab7d68963c020bbf08d45`) |
| Normallashtirish | IMLO-2 qatlami (`KKT_IMLO_A`), sukut bo'yicha yoqiq |
| Hovuz | ishlab chiqish to'plami E2119 (2 119 gap). Normallashtirish tarjimani o'zgartirgan 174 gapdan tasodifiy 60 tasi tanlangan |
| Tanlov turlari | A1a + A1b — 39; faqat A1a — 20; A1a + A5a — 1 |

E2119 — sozlash (development) to'plami, sinov to'plami emas.

## Baholovchilar

| | model | qanday |
|---|---|---|
| GPT | **GPT-6 Luna** (OpenAI). Nom ChatGPT interfeysida ko'rsatilgani bo'yicha olingan. Vaqtinchalik chat jurnal qoldirmaydi, shuning uchun texnik identifikator qayd etilmagan | ChatGPT Go obunasi, Temporary Chat (xotira va chat tarixisiz), standart sozlamalar. Har tartib alohida chatda |
| Claude | **`claude-opus-5-5`** (Claude Opus 5.5, Anthropic). Identifikator sessiya transkriptidan olingan | Claude Code. Har tartib alohida sessiyada; sessiya faqat ko'rsatma va bitta element fayliga kira olgan |

**Claude sessiyalari transkriptlari bu arxivga kirmaydi**, chunki ularda lokal fayl yo'llari va shaxsiy ma'lumot bor.
Ular **so'rov bo'yicha** taqdim etiladi.

## Fayllar

### 1. Element fayllari (ikki tartib, har biri 60 element)

| fayl | mazmuni |
|---|---|
| `kor_paket_gpt_1.csv` | 1-tartib, `N001`–`N060` |
| `kor_paket_gpt_2.csv` | 2-tartib, `N061`–`N120`. Xuddi o'sha 60 juftlik: tarjimalar o'rni almashgan, elementlar qayta aralashtirilgan |

Nomdagi `gpt` tarixiy: ikkala baholovchi ham aynan shu ikki faylni olgan (Claude sessiyalarida fayllar
`kor_paket_1.csv` / `kor_paket_2.csv` deb nomlangan, sha256 aynan).

Ustunlar: `id`, `uzbek` (o'zbekcha manba gap; **normallashtirilgan** matn), `translation_1`, `translation_2`
(ikki inglizcha tarjima). Ulardan biri normallashtirishsiz, biri normallashtirish bilan olingan. Qaysi biri qaysi
ekanini va qoida turini faqat kalit ko'rsatadi.

### 2. Kalit

| fayl | mazmuni |
|---|---|
| `kor_kalit.json` | kalit |
| `kor_kalit.sha256` | kalitning SHA-256 xeshi |

`kor_kalit.json` → `meta`:
- `seed` — `2736072208` (manbasi `os.urandom`, paket qurish paytida olingan);
- `hovuz` 174, `tanlov` 60, `min_oraliq` 10 (2-tartibda bir juftlik ikki tartib orasida kamida 10 o'rin siljigan);
- `tomon`: `oldin` = normallashtirishsiz, `keyin` = normallashtirish bilan;
- `tanlangan` — tanlangan 60 gapning korpusdagi kaliti;
- `sha256` — paket fayllarining xeshlari.

`meta.baholovchilar` maydoni kalit qurilgan paytdagi rejani yozadi: Claude to'liq 120 elementli faylni bitta
sessiyada olishi kerak edi. Bu reja keyin o'zgartirildi, pastdagi «Chetga olingan birinchi o'tkazish» ga qarang.
Kalit faylining o'zi o'zgartirilmagan.

`kor_kalit.json` → `qator` (har element `N001`–`N120` uchun):
- `juft` — juftlik ID si (`NJ001`–`NJ060`). Har juftlik bitta 1-tartib va bitta 2-tartib elementida uchraydi;
- `kalit` — manba gapning korpusdagi ID si (`2119:<manba>|<raqam>`);
- `turlar` — gapga qo'llangan normallashtirish qoidasi turi (`A1a`, `A1b`, `A5a`; maqola A ilovasi);
- `1` — 1-o'rindagi (`translation_1`) tarjima qaysi tomon: `keyin` bo'lsa normallashtirish bilan, `oldin` bo'lsa
  normallashtirishsiz.

**Xesh tekshiruvi (2026-10-15):** `kor_kalit.json` ning SHA-256 xeshi qayta hisoblandi:
`0362fe54b5fade5b2a8d16527fedab895d2fb0f4130a481cabf3aa0550c00ee2`. Bu `0a81be2` commitidagi
(2026-10-08 15:46 +05) `kor_kalit.sha256` qiymati bilan **MOS**. Kalit birinchi baholash javobi olinishidan oldin
commit qilingan. Javoblar keyinroq commit qilingan: `5dcfa0f` 17:27, `4b9ebb3` 17:38, `972baca` 17:45.

### 3. Baholovchi javoblari (asosiy natija)

| fayl | baholovchi | tartib | qator oxiri |
|---|---|---|---|
| `kor_paket_gpt_1_natija.csv` | GPT | 1 | LF |
| `kor_paket_gpt_2_natija.csv` | GPT | 2 | CRLF (asl holida saqlangan) |
| `kor_paket_claude_1_natija.csv` | Claude | 1 | LF |
| `kor_paket_claude_2_natija.csv` | Claude | 2 | LF |

Ustunlar: `id` (element ID si), `choice` (`1`, `2` yoki `tie`), `reason` (baholovchi bergan sabab, ko'pi bilan
15 so'z). Fayllar xom baytda saqlangan, hech qanday tozalash qilinmagan.

### 4. Ko'rsatma va qoida

| fayl | mazmuni |
|---|---|
| `kor_korsatma_60.md`, `.sha256` | asosiy natijada ishlatilgan ko'rsatma (= maqola B ilovasi), sha256 `3c51df0c…` |
| `kor_qoida.md` | dekod va qabul mezoni. Baholashdan oldin, kalit bilan bitta commitda yozilgan (`0a81be2`). Faylda dastlabki reja ham bor (3-band: Claude uchun 120 elementli bitta fayl). Bu reja o'zgargan, 4-bo'limga qarang |

Ko'rsatma matni (B ilova):

> You are evaluating machine translations from Uzbek to English. For each item you get an Uzbek source sentence
> and two English translations. Decide which translation conveys the meaning of the Uzbek sentence more
> accurately and reads more acceptably as English. Meaning errors (wrong/missing/added content, wrong
> negation, tense or who-did-what-to-whom, wrong relation between the clauses of the sentence) weigh more than
> fluency. Both translations are often poor; judge which one is better, not whether it is good. Answer `1`, `2`,
> or `tie` (use `tie` only if they are equally good or equally bad). Judge every item independently.
> Output CSV with header `id,choice,reason` — one row per item, reason at most 15
> words. Do not skip items.

GPT chatlarida bu matndan keyin qo'shimcha qoidalar berilgan:
- faylda 60 element bor;
- id lar fayldagidek saqlansin, qayta raqamlanmasin;
- javobda aniq 60 qator bo'lsin;
- javob yuklab olinadigan CSV fayl bo'lsin;
- har qatorda sabab tanlovga mos ekani tekshirilsin.

Claude sessiyalariga xuddi shu qoidalar o'zbek tilida berilgan.

### 5. Hisob skripti va natijasi

| fayl | mazmuni |
|---|---|
| `kor_dekod.py` | dekod: element javobi → tomon → juftlik hukmi, yaroqlilik, kelishuv matritsasi, umumiy hukm, mezon. 5-jadvaldagi barcha sonlar shundan chiqadi |
| `kor_hukm.json` | skript natijasi |
| `kor_sabab_tasnif.json` | sabab–tanlov mosligining qo'lda tasnifi (skript o'qiydi). Ziddiyat soni 0 |

Ishga tushirish: `python3 kor_dekod.py`. Skript Python 3 standart kutubxonasini ishlatadi. U o'zi turgan papkadan
o'qiydi va `kor_hukm.json` ni qayta yozadi. Repozitoriyadagi tuzilishda barcha fayllar bitta papkada edi. Shuning
uchun avval `discarded_run1/` dagi fayllarni yuqori papkaga nusxalang. Skript ularni qo'shimcha (v0) natija uchun ham
o'qiydi, 120 elementli `kor_paket.csv` ni esa misol matnlari uchun o'qiydi. Kalit xeshi skript ichida tekshiriladi
(`assert`). 2026-10-15 da skript nusxada qayta yurgizildi: `kor_hukm.json` **bayt-aynan** qayta hosil bo'ldi.

**κ va AC1 uchun alohida skript yo'q.** Ular `kor_hukm.json` → `kelishuv.matritsa_GPT|Claude` dagi 3×3 jadvaldan
qo'lda hisoblangan. Hisobda har baholovchining 60 juftlik bo'yicha uch toifali hukmi olingan (yaxshi / teng / yomon;
5-jadvaldagi «Juftliklar, ikki tartib» ustuni).

| | GPT \\ Claude: yaxshi | teng | yomon |
|---|--:|--:|--:|
| **yaxshi** | 40 | 2 | 0 |
| **teng** | 10 | 3 | 1 |
| **yomon** | 2 | 1 | 1 |

Hisob:
- p_o = 44/60 = 0,733.
- Koen κ: p_e = Σ p_GPT(k)·p_Claude(k) = 0,632, shundan κ = (p_o − p_e)/(1 − p_e) = **0,275**.
- Gwet AC1: π_k = (p_GPT(k) + p_Claude(k))/2, p_e = Σ π_k(1 − π_k)/(K − 1) = 0,178 (K = 3), shundan
  AC1 = **0,676**.

2026-10-15 da shu formulalar bilan qayta hisoblandi va qiymatlar mos keldi.

### Qayta hisoblanadigan natija (5-jadval)

| baholovchi | 1-tartib | 2-tartib | juftliklar, ikki tartib | tartib ziddiyati | eng ko'p pozitsiya | yaroqli |
|---|---|---|---|---|---|---|
| GPT | 47 : 0 : 13 | 51 : 0 : 9 | 42 : 14 : 4 | 14 (23,3 %) | 55,0 % | ha |
| Claude | 55 : 3 : 2 | 52 : 6 : 2 | 52 : 6 : 2 | 3 (5,0 %) | 46,7 % | ha |
| kelishilgan | | | 40 : 3 : 1 (16 tasi kelishilmagan) | | | |

Jadvaldagi uchlik: normallashtirishsiz chiqishga nisbatan yaxshi : teng : yomon.

## Dekod va qabul mezoni

Qoida baholashdan oldin belgilangan (`kor_qoida.md`).

- Element javobi kalit orqali tomonga o'giriladi: `keyin` → yaxshi, `oldin` → yomon, `tie` → teng.
- Juftlik hukmi: ikki tartib bir xil tomonni bersa, hukm o'sha tomon. Javoblar zid bo'lsa (qarama-qarshi tanlov
  yoki tanlov bilan `tie`), hukm **teng**.
- **Yaroqsizlik:** javoblarning 95 % dan ortig'i bitta pozitsiyaga tushsa yoki juftliklarning 50 % dan ortig'ida
  tartiblar zid bo'lsa, baholovchi yaroqsiz sanaladi.
- **Qabul mezoni** ikkala baholovchi kelishgan juftliklarga qo'llanadi: **yaxshi ≥ 2 × yomon VA yomon ≤ 6/60**.
  Natija: 40 : 3 : 1, mezon bajarildi.

## Chetga olingan birinchi o'tkazish (`discarded_run1/`)

Maqola 2.6-bo'limidan:

> Birinchi o'tkazish dizaynga mos kelmagani uchun dekoddan oldin chetga olindi: unda Claude ikkala tartibni bitta
> faylda olgan va takrorlangan gaplarni bir-biriga moslaganini o'zi aytgan, GPT chatlarida esa chat tarixiga kirish
> bor edi. Qaror va sabab repozitoriyada og'ish sifatida qayd etilgan; birinchi o'tkazishning natijalari faqat
> qo'shimcha sifatida keltiriladi.

Sabablar batafsil:
- **Claude (og'ish O1).** Claude bitta sessiyada `kor_paket.csv` ni oldi: 120 element, ikkala tartib bitta faylda.
  U 61–120 qatorlarni 1–60 dagi juftliklarga moslab baholaganini o'zi oshkor qildi. Natijada ikki tartib mustaqil
  emas: tartib ziddiyati 0.
- **GPT (og'ish O2).** GPT birinchi o'tkazishni oddiy rejimda qildi, «Reference chat history» yoqilgan edi. Shuning
  uchun ikki chat bir-biridan mustaqil ekani kafolatlanmaydi.

Ikkala qaror ham dekoddan oldin qabul qilingan (commitlar `5dcfa0f`, `4b9ebb3`). Birinchi o'tkazish eski ko'rsatma
bilan qilingan (`kor_korsatma.md`, sha256 `e37f4dfe…`). Undagi «— every source sentence occurs more than once»
jumlasi asosiy o'tkazish ko'rsatmasida (`kor_korsatma_60.md`) olib tashlangan. Qolgan matn so'zma-so'z bir xil.

| fayl | mazmuni |
|---|---|
| `kor_paket.csv`, `.sha256` | Claude birinchi o'tkazishda olgan 120 elementli fayl (`N001`–`N120`, ikkala tartib). Kalit va ID lar asosiy natijadagi bilan bir xil |
| `kor_korsatma.md`, `.sha256` | birinchi o'tkazish ko'rsatmasi |
| `kor_paket_claude_natija_v0_ogish.csv` | Claude, 120 qator, bitta sessiya |
| `kor_paket_gpt_1_natija_v0_ogish.csv` | GPT, 1-tartib. CRLF, UTF-8 BOM bilan (asl holida) |
| `kor_paket_gpt_2_natija_v0_ogish.csv` | GPT, 2-tartib |

Ustunlar asosiy javob fayllaridagi bilan bir xil (`id,choice,reason`).

Qo'shimcha natija (`kor_hukm.json` → `qoshimcha_v0`): GPT v0 36 : 22 : 2, Claude v0 52 : 3 : 5. Kelishilgan
juftliklarda 36 yaxshi, 2 teng, 1 yomon (21 tasi kelishilmagan). Bu natija umumiy hukmga va mezonga kirmaydi.

## Yaxlitlik

`MANIFEST.sha256` arxivdagi har fayl uchun SHA-256 xeshini beradi (o'zidan tashqari). Tekshirish:
`shasum -a 256 -c MANIFEST.sha256` yoki `sha256sum -c MANIFEST.sha256`.
