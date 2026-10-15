# ICITE-FAKT (imlo) — kichik ko'r tekshiruv: dekod va talqin qoidasi (BAHOLASHDAN OLDIN; foydalanuvchi, 2026-10-08)

Kalit `kor_kalit.json` (sha256 `0362fe54b5fade5b2a8d16527fedab895d2fb0f4130a481cabf3aa0550c00ee2`) va paketlar shu qoida
bilan bitta commitda, javoblar olinishidan OLDIN. Paket qurish: `kor.py paket` (seed kalitda; `--seed` bilan bayt-aynan
qayta quriladi).

1. **Savol:** 2 119 da IMLO-2 normallashtirish (`KKT_IMLO_A`) tarjimani o'zgartirgan 174 gapdan tasodifiy 60 tasida
   «normallashtirish bilan» (KEYIN) tarjima «normallashtirishsiz» (OLDIN) dan yaxshimi? Hovuz va tanlov:
   `imlo_radius.json` → `tarjima_ozgardi`, `kor_kalit.json` → `meta.tanlangan`. Tanlovda tur: A1a+A1b 39 · A1a 20 ·
   A1a+A5a 1.
2. **Maqomi:** O'LCHOV (ICITE fakt varag'i uchun), darvoza EMAS — kod qarori shu natijaga bog'lanmaydi. 2 119 —
   tuning/ochiq to'plam, «test» deb yozilmaydi.
3. **Baholovchilar:** GPT — `kor_paket_gpt_1.csv` (1-tartib, 60) va `kor_paket_gpt_2.csv` (2-tartib, 60), alohida
   suhbatlarda; Claude — `kor_paket.csv` (to'liq 120), yangi sessiya / subagent, faqat paket + ko'rsatma. Gemini kirmaydi
   (sinov-3 `xulosa.md` §1.2). Ko'rsatma ikkalasiga bir xil: `kor_korsatma.md` (= `oldin-keyin-1/korsatma.md`). Paketdagi
   o'zbekcha manba — normallashgan matn.
4. **Dekod, har model alohida:** element javobi `1` / `2` / `tie` kalit orqali OLDIN / KEYIN / TENG ga o'giriladi.
   Juftlik hukmi: ikki tartib bir xil tomonni bersa — o'sha (KEYIN = **yaxshi**, OLDIN = **yomon**, TENG = teng); zid bo'lsa
   — **teng**.
5. **Yaroqsizlik (hukmdan OLDIN):** javoblarning > 95 % i bir pozitsiyada (`1` yoki `2`) YOKI juftliklarning > 50 % ida
   ikki tartib zid → model YAROQSIZ, umumiy hukmga kirmaydi (natijasi alohida yoziladi).
6. **Umumiy hukm:** ikkala yaroqli model kelishgan juftliklar; kelishmaganlar «kelishilmagan» deb alohida sanaladi.
   Bitta model yaroqsiz bo'lsa — qolgan modelning hukmi, bu qayd bilan.
7. **MEZON (foydalanuvchi):** **yaxshi ≥ 2 × yomon VA yomon ≤ 10 %** (60 juftlikdan ≤ 6). Ikkalasi bajarilsa —
   «normallashtirish yaxshilaydi», aks holda «aralash». Mezon umumiy hukmga qo'llanadi. Har model natijasi alohida
   yoziladi.
8. **Qo'shimcha kesim (faqat ma'lumot, talqin yo'q):** tur (`A1a+A1b` / `A1a` / `A1a+A5a`) va 8-misol mexanizmi
   (`data/domain_disambiguation.json` dagi apostrofli kalitlar: `bo'lim`, `ko'z`, `o'rin`, `yo'l`) — tanlangan gaplar
   orasida bo'lsa.
9. Javob fayllari `kor_paket_*_natija.*` nomi bilan shu papkaga qo'yiladi. Asl javobga tegilmaydi, tozalash bo'lsa
   alohida faylda va qayd bilan.
