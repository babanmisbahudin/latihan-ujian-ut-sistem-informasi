"""Membangun semua halaman latihan dari src/semester-*/soal.py.

Jalankan dari folder repo:  python3 src/build.py
Tidak butuh paket tambahan (cukup Python 3.8+).

Hasil:
  index.html                      daftar semester
  semester-N/index.html           daftar mata kuliah semester N
  semester-N/soal/<KODE>.html     halaman latihan tiap mata kuliah
"""
import glob, hashlib, html, importlib.util, json, os, re

# Link halaman Saweria publik (bukan /admin), misalnya "https://saweria.co/namaanda".
# Biarkan kosong untuk menyembunyikan tombol dukungan.
SAWERIA = "https://saweria.co/himisbah"

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)

GAYA = """:root{--bg:#f6f7f9;--card:#fff;--ink:#1c2430;--mut:#5f6b7a;--line:#d9dee5;--pri:#0b5cad;--ok:#17803d;--bad:#c02b2b;--mid:#a86b00;--track:#e7ebf0}
@media (prefers-color-scheme:dark){:root{--bg:#12161c;--card:#1b222b;--ink:#e8ecf1;--mut:#a3aebb;--line:#333d49;--pri:#6db1f5;--ok:#5fd38a;--bad:#ff8a8a;--mid:#f0b54a;--track:#2a333f}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:760px;margin:auto;padding:16px 16px 48px}h1{font-size:1.4rem;margin:.3rem 0}p{color:var(--mut)}a{color:var(--pri)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px;margin-top:16px}
.card{display:flex;flex-direction:column;gap:2px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;color:var(--ink);text-decoration:none}
.card:hover,.card:focus-visible{border-color:var(--pri);outline:none}.card b{color:var(--pri)}.card small{color:var(--mut)}
.est{font-size:1.5rem;font-weight:700;font-variant-numeric:tabular-nums;margin-top:6px}
.bar{height:6px;background:var(--track);border-radius:9px;overflow:hidden}.bar i{display:block;height:100%}
.dukung{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between;background:var(--card);border:1px dashed var(--line);border-radius:12px;padding:12px 14px;margin-top:20px}
.dukung p{margin:0;font-size:.92rem}.dukung a{display:inline-block;background:#f5a524;color:#1c1300;font-weight:700;text-decoration:none;border-radius:8px;padding:10px 14px}
.dukung a:hover,.dukung a:focus-visible{outline:2px solid var(--pri);outline-offset:2px}"""

# Membaca ringkasan progres dari localStorage (diisi oleh halaman latihan) lalu menampilkannya di kartu.
SKRIP = """<script>
const baca=k=>{try{return (JSON.parse(localStorage.getItem('latihan_ut_'+k))||{}).ringkas||null}catch(e){return null}};
const warna=v=>v>=80?'var(--ok)':v>=65?'var(--mid)':'var(--bad)';
for(const a of document.querySelectorAll('a.card[data-kode]')){
 const kode=a.dataset.kode.split(',');const rs=kode.map(baca).filter(r=>r&&r.A>0);const box=a.querySelector('.isi');
 if(!rs.length){box.textContent='Belum mulai';continue}
 const siap=rs.filter(r=>r.cukup);const A=rs.reduce((s,r)=>s+r.A,0);const N=+a.dataset.n;
 if(!siap.length){box.textContent=A+' soal dijawab · perkiraan muncul setelah 20';continue}
 const est=Math.round(siap.reduce((s,r)=>s+r.est,0)/siap.length);const w=warna(est);
 const e=document.createElement('div');e.className='est';e.style.color=w;e.textContent=(kode.length>1?'Rata-rata ':'Perkiraan ')+est;
 const bar=document.createElement('div');bar.className='bar';const i=document.createElement('i');i.style.width=Math.min(100,Math.round(A/N*100))+'%';i.style.background=w;bar.append(i);
 const s=document.createElement('small');s.textContent=A+'/'+N+' soal dijawab'+(kode.length>1?' · '+siap.length+' dari '+kode.length+' MK punya perkiraan':'');
 box.replaceWith(e,bar,s)}
</script>"""


def halaman(judul, isi, kembali=""):
    return f"""<!doctype html>
<html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(judul)}</title>
<style>
{GAYA}
</style></head><body><main>
{kembali}<h1>{html.escape(judul)}</h1>
{isi}
{dukungan()}
<p style="margin-top:20px;font-size:.9rem">Perkiraan nilai dihitung dari latihan Anda sendiri dan tersimpan di browser ini. Angkanya kasar, bukan jaminan nilai ujian.</p>
</main>
{SKRIP}
</body></html>
"""


def dukungan():
    if not SAWERIA:
        return ""
    return ('<aside class="dukung" aria-label="Dukung pembuat"><p>Latihan ini gratis. Kalau bermanfaat, '
            'Anda bisa mendukung pembuatnya secara sukarela.</p>'
            f'<a href="{html.escape(SAWERIA)}" target="_blank" rel="noopener">☕ Dukung via Saweria</a></aside>')


def muat(path):
    spec = importlib.util.spec_from_file_location("soal_" + os.path.basename(os.path.dirname(path)).replace("-", "_"), path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def periksa(kode, item):
    sesi, soal, opsi, kunci, alasan = item
    if not (isinstance(sesi, int) and soal and len(opsi) >= 2 and 0 <= kunci < len(opsi)):
        raise ValueError(f"{kode}: format soal tidak valid -> {soal[:60]!r}")
    if len(set(opsi)) != len(opsi):
        raise ValueError(f"{kode}: ada opsi kembar -> {soal[:60]!r}")


def bangun_semester(folder_src, tpl):
    nomor = re.search(r"semester-(\d+)$", folder_src).group(1)
    m = muat(os.path.join(folder_src, "soal.py"))
    keluar = os.path.join(ROOT, f"semester-{nomor}")
    os.makedirs(os.path.join(keluar, "soal"), exist_ok=True)
    rows = []
    for kode, nama in m.MK.items():
        daftar = []
        for item in m.SOAL.get(kode, []):
            periksa(kode, item)
            sesi, soal, opsi, kunci, alasan = item
            daftar.append(dict(g=f"Sesi {sesi}", src="Latihan", q=soal, a=opsi, k=kunci, w=alasan))
        daftar.sort(key=lambda x: int(x["g"].split()[1]))
        for x in daftar:
            x["id"] = hashlib.md5((x["q"] + "|" + x["a"][x["k"]]).encode()).hexdigest()[:10]
        if len({x["id"] for x in daftar}) != len(daftar):
            raise ValueError(f"{kode}: ada soal kembar")
        esai = m.ESAI.get(kode, [])
        data = json.dumps(dict(kode=kode, q=daftar, esai=esai), ensure_ascii=False).replace("</", "<\\/")
        out = tpl.replace("__TITLE__", html.escape(f"Latihan {kode} {nama}")).replace("__DATA__", data)
        open(os.path.join(keluar, "soal", f"{kode}.html"), "w", encoding="utf-8").write(out)
        rows.append((kode, nama, len(daftar), len(esai)))
        print(f"  {kode}: {len(daftar)} soal, {len(esai)} esai")
    kartu = "\n".join(
        f'<a class="card" href="soal/{k}.html" data-kode="{k}" data-n="{q}"><b>{k}</b><span>{html.escape(n)}</span>'
        f'<small>{q} soal · {e} esai</small><small class="isi">Belum mulai</small></a>' for k, n, q, e in rows)
    tq, te = sum(r[2] for r in rows), sum(r[3] for r in rows)
    isi = f'<p>{tq} soal pilihan ganda dan {te} latihan esai. Tidak resmi; bukan bocoran soal ujian.</p>\n<div class="grid">\n{kartu}\n</div>'
    open(os.path.join(keluar, "index.html"), "w", encoding="utf-8").write(
        halaman(f"Semester {nomor}", isi, '<a href="../index.html">← Semua semester</a>'))
    return int(nomor), rows


def main():
    tpl = open(os.path.join(SRC, "template.html"), encoding="utf-8").read()
    semua = []
    for folder in sorted(glob.glob(os.path.join(SRC, "semester-*")), key=lambda p: int(p.rsplit("-", 1)[1])):
        if not os.path.isfile(os.path.join(folder, "soal.py")):
            continue
        print(os.path.basename(folder))
        semua.append(bangun_semester(folder, tpl))
    kartu = "\n".join(
        f'<a class="card" href="semester-{n}/index.html" data-kode="{",".join(r[0] for r in rows)}" data-n="{sum(r[2] for r in rows)}">'
        f'<b>Semester {n}</b><span>{len(rows)} mata kuliah</span><small>{sum(r[2] for r in rows)} soal · {sum(r[3] for r in rows)} esai</small>'
        f'<small class="isi">Belum mulai</small></a>' for n, rows in semua)
    tq = sum(r[2] for _, rows in semua for r in rows)
    isi = (f'<p>Program studi Sistem Informasi · {len(semua)} semester · {tq} soal. '
           'Latihan tidak resmi, bukan bocoran soal ujian.</p>\n<div class="grid">\n' + kartu + '\n</div>')
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(
        halaman("Latihan Ujian Universitas Terbuka · Sistem Informasi", isi))
    print(f"Total: {len(semua)} semester, {tq} soal")


if __name__ == "__main__":
    main()
