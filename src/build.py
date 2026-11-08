"""Membangun semua halaman latihan dari src/semester-*/soal.py.

Jalankan dari folder repo:  python3 src/build.py
Tidak butuh paket tambahan (cukup Python 3.8+).

Hasil:
  index.html                      halaman utama: daftar semester
  semester-N/index.html           daftar mata kuliah semester N
  semester-N/soal/<KODE>.html     halaman latihan tiap mata kuliah
"""
import glob, hashlib, html, importlib.util, json, os, re

# ---------------------------------------------------------------- Pengaturan
# Link halaman Saweria publik (bukan /admin). Kosongkan untuk menyembunyikan.
SAWERIA = "https://saweria.co/himisbah"
# Media sosial pembuat. Kosongkan yang tidak dipakai; tombolnya otomatis hilang.
INSTAGRAM = "https://instagram.com/himisbah_"
TIKTOK = "https://www.tiktok.com/@himisbah"
LINKEDIN = "https://www.linkedin.com/in/himisbah"
# Link repo GitHub, ditampilkan di bagian bawah halaman.
REPO = "https://github.com/babanmisbahudin/latihan-ujian-ut-sistem-informasi"
PRODI = "Sistem Informasi"
# Pemegang hak cipta dan tahun, ditampilkan di bagian bawah setiap halaman.
PEMILIK = "Baban Misbahudin"
TAHUN = "2026"
# ----------------------------------------------------------------------------

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)

GAYA = """:root{--bg:#f4f6f9;--card:#fff;--ink:#16202c;--mut:#5b6878;--line:#dde3ea;--pri:#0b5cad;--pri2:#e8f1fb;--ok:#17803d;--bad:#c02b2b;--mid:#a86b00;--track:#e6ebf1;--shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.08)}
@media (prefers-color-scheme:dark){:root{--bg:#10141a;--card:#19202a;--ink:#e8edf3;--mut:#9ea9b7;--line:#2c3542;--pri:#6db1f5;--pri2:#16263a;--ok:#5fd38a;--bad:#ff8a8a;--mid:#f0b54a;--track:#262f3b;--shadow:none}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:880px;margin:auto;padding:24px 16px 56px}
a{color:var(--pri)}a:focus-visible,button:focus-visible{outline:2px solid var(--pri);outline-offset:2px;border-radius:6px}
.crumb{font-size:.88rem;color:var(--mut);display:flex;gap:6px;flex-wrap:wrap}.crumb a{text-decoration:none}.crumb a:hover{text-decoration:underline}
.hero{padding:8px 0 4px}.eyebrow{display:inline-block;font-size:.8rem;font-weight:600;letter-spacing:.02em;color:var(--pri);background:var(--pri2);border-radius:99px;padding:3px 10px}
h1{font-size:clamp(1.6rem,4vw,2.2rem);line-height:1.2;margin:10px 0 6px;letter-spacing:-.01em}
.lead{color:var(--mut);margin:0;max-width:60ch}
h2{font-size:1.1rem;margin:32px 0 12px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:20px}
@media (max-width:560px){.stats{grid-template-columns:repeat(2,1fr)}}
.stat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;box-shadow:var(--shadow)}
.stat b{display:block;font-size:1.4rem;font-variant-numeric:tabular-nums;line-height:1.2}.stat span{font-size:.82rem;color:var(--mut)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.card{position:relative;display:flex;flex-direction:column;gap:4px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;color:var(--ink);text-decoration:none;box-shadow:var(--shadow);transition:border-color .15s,transform .15s}
.card:hover{border-color:var(--pri);transform:translateY(-1px)}
.code{align-self:flex-start;font-size:.75rem;font-weight:700;letter-spacing:.03em;color:var(--pri);background:var(--pri2);border-radius:6px;padding:2px 8px}
.card .nama{font-size:1.05rem;font-weight:650;line-height:1.35;margin-top:4px}
.card .meta{font-size:.84rem;color:var(--mut)}
.card .isi{font-size:.84rem;color:var(--mut);margin-top:auto;padding-top:10px}
.card .go{font-size:.86rem;font-weight:600;color:var(--pri);margin-top:8px}
.est{font-size:1.35rem;font-weight:700;font-variant-numeric:tabular-nums}
.bar{height:6px;background:var(--track);border-radius:9px;overflow:hidden;margin:6px 0 4px}.bar i{display:block;height:100%;border-radius:9px}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;counter-reset:s}
@media (max-width:640px){.steps{grid-template-columns:1fr}}
.step{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;box-shadow:var(--shadow)}
.step::before{counter-increment:s;content:counter(s);display:inline-flex;width:26px;height:26px;border-radius:50%;align-items:center;justify-content:center;background:var(--pri);color:#fff;font-weight:700;font-size:.85rem;margin-bottom:6px}
@media (prefers-color-scheme:dark){.step::before{color:#0d1a26}}
.step b{display:block}.step span{font-size:.88rem;color:var(--mut)}
.creator{display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin-top:32px;box-shadow:var(--shadow)}
.creator p{margin:0;font-size:.92rem;color:var(--mut);max-width:42ch}.creator p b{color:var(--ink)}
.links{display:flex;flex-wrap:wrap;gap:8px}
.btn{display:inline-flex;align-items:center;gap:8px;min-height:42px;padding:8px 14px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--ink);text-decoration:none;font-weight:600;font-size:.9rem}
.btn:hover{border-color:var(--pri)}.btn svg{width:18px;height:18px;flex:none}
.btn.saweria{background:#f5a524;border-color:#f5a524;color:#1c1300}
footer{margin-top:28px;padding-top:16px;border-top:1px solid var(--line);font-size:.82rem;color:var(--mut);display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:space-between;align-items:flex-start}
footer p{margin:0 0 6px;max-width:70ch}footer b{color:var(--ink);font-weight:600}"""

IKON = {
    "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
    "tiktok": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 3h3a4 4 0 0 0 4 4v3a7 7 0 0 1-4-1.3V15a6 6 0 1 1-6-6v3.2A2.8 2.8 0 1 0 14 15z"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4 3.5a2 2 0 1 1 0 4 2 2 0 0 1 0-4zM2.5 9h3v12h-3zM9 9h2.9v1.7h.1c.4-.8 1.4-1.9 3.2-1.9 3.4 0 4 2.2 4 5.1V21h-3v-6.2c0-1.5 0-3.3-2-3.3s-2.3 1.6-2.3 3.2V21H9z"/></svg>',
    "saweria": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 9h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5zM17 10h1.5a2.5 2.5 0 0 1 0 5H17M8 3v3M12 3v3"/></svg>',
}

# Membaca ringkasan progres dari localStorage (diisi oleh halaman latihan) lalu menampilkannya di kartu.
SKRIP = """<script>
const baca=k=>{try{return (JSON.parse(localStorage.getItem('latihan_ut_'+k))||{}).ringkas||null}catch(e){return null}};
const warna=v=>v>=80?'var(--ok)':v>=65?'var(--mid)':'var(--bad)';
for(const a of document.querySelectorAll('a.card[data-kode]')){
 const kode=a.dataset.kode.split(',');const rs=kode.map(baca).filter(r=>r&&r.A>0);const box=a.querySelector('.isi');
 if(!rs.length){box.textContent='Belum mulai';continue}
 const siap=rs.filter(r=>r.cukup);const A=rs.reduce((s,r)=>s+r.A,0);const N=+a.dataset.n;
 const bar=document.createElement('div');bar.className='bar';const i=document.createElement('i');i.style.width=Math.min(100,Math.round(A/N*100))+'%';bar.append(i);
 const s=document.createElement('div');s.textContent=A+'/'+N+' soal dijawab';
 if(!siap.length){i.style.background='var(--pri)';s.textContent+=' · perkiraan muncul setelah 20';box.replaceChildren(bar,s);continue}
 const est=Math.round(siap.reduce((x,r)=>x+r.est,0)/siap.length);const w=warna(est);i.style.background=w;
 const e=document.createElement('div');e.className='est';e.style.color=w;e.textContent=(kode.length>1?'Rata-rata ':'Perkiraan ')+est;
 box.replaceChildren(e,bar,s)}
</script>"""


def pembuat():
    tombol = []
    for nama, url, kelas in (("Instagram", INSTAGRAM, "instagram"), ("TikTok", TIKTOK, "tiktok"),
                             ("LinkedIn", LINKEDIN, "linkedin")):
        if url:
            tombol.append(f'<a class="btn" href="{html.escape(url)}" target="_blank" rel="noopener">{IKON[kelas]}{nama}</a>')
    if SAWERIA:
        tombol.append(f'<a class="btn saweria" href="{html.escape(SAWERIA)}" target="_blank" rel="noopener">{IKON["saweria"]}Dukung via Saweria</a>')
    if not tombol:
        return ""
    return ('<aside class="creator" aria-label="Tentang pembuat"><p><b>Latihan ini gratis.</b> '
            'Kalau bermanfaat, ikuti pembuatnya untuk kabar semester berikutnya, atau dukung secara sukarela.</p>'
            f'<div class="links">{"".join(tombol)}</div></aside>')


def kaki(repo=""):
    """Keterangan hak cipta, lisensi, dan penafian di bagian bawah halaman."""
    return (
        '<footer class="kaki"><div>'
        f'<p><b>© {TAHUN} {html.escape(PEMILIK)}.</b> Kode berlisensi '
        '<a href="https://opensource.org/license/mit" target="_blank" rel="noopener">MIT</a>; '
        'soal dan esai berlisensi '
        '<a href="https://creativecommons.org/licenses/by-nc/4.0/deed.id" target="_blank" rel="noopener">CC BY-NC 4.0</a> '
        '(boleh dibagikan dengan mencantumkan sumber, tidak untuk dijual).</p>'
        '<p>Latihan <b>tidak resmi</b> dan tidak berafiliasi dengan Universitas Terbuka. Nama Universitas Terbuka '
        'dan isi Buku Materi Pokok (BMP) adalah milik Universitas Terbuka; soal di sini ditulis ulang, bukan salinan BMP, '
        'dan <b>bukan bocoran soal ujian</b>. Disediakan apa adanya tanpa jaminan; jika berbeda, ikuti BMP dan tutor Anda.</p>'
        '<p>Privasi: tidak ada akun dan tidak ada data yang dikirim. Progres dan perkiraan nilai hanya tersimpan di browser Anda.</p>'
        f'</div>{repo}</footer>')


def halaman(judul, kepala, isi, judul_tab=None):
    repo = f'<a href="{html.escape(REPO)}" target="_blank" rel="noopener">Kode sumber di GitHub</a>' if REPO else ""
    return f"""<!doctype html>
<html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(judul_tab or judul)}</title>
<meta name="description" content="Latihan soal ujian Universitas Terbuka program studi {html.escape(PRODI)}: pilihan ganda, esai, dan perkiraan nilai. Tidak resmi.">
<style>
{GAYA}
</style></head><body><main>
{kepala}
{isi}
{pembuat()}
{kaki(repo)}
</main>
{SKRIP}
</body></html>
"""


# Gaya footer untuk halaman latihan (memakai token warna template).
KAKI_LATIHAN = ('<style>.kaki{margin-top:28px;padding-top:14px;border-top:1px solid var(--line);font-size:.8rem;color:var(--mut)}'
                '.kaki p{margin:0 0 6px}.kaki b{color:var(--ink);font-weight:600}</style>')


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
        out = (tpl.replace("__TITLE__", html.escape(f"Latihan {kode} {nama}"))
                  .replace("__SEMESTER__", f"Semester {nomor}").replace("__DATA__", data)
                  .replace("</main>", KAKI_LATIHAN + kaki() + "</main>"))
        open(os.path.join(keluar, "soal", f"{kode}.html"), "w", encoding="utf-8").write(out)
        rows.append((kode, nama, len(daftar), len(esai)))
        print(f"  {kode}: {len(daftar)} soal, {len(esai)} esai")
    kartu = "\n".join(
        f'<a class="card" href="soal/{k}.html" data-kode="{k}" data-n="{q}"><span class="code">{k}</span>'
        f'<span class="nama">{html.escape(n)}</span><span class="meta">{q} soal pilihan ganda · {e} esai</span>'
        f'<div class="isi">Belum mulai</div><span class="go">Mulai latihan →</span></a>' for k, n, q, e in rows)
    tq, te = sum(r[2] for r in rows), sum(r[3] for r in rows)
    kepala = (f'<nav class="crumb" aria-label="Navigasi"><a href="../index.html">Beranda</a><span>/</span><span>Semester {nomor}</span></nav>'
              f'<header class="hero"><span class="eyebrow">{html.escape(PRODI)}</span><h1>Semester {nomor}</h1>'
              f'<p class="lead">{len(rows)} mata kuliah · {tq} soal pilihan ganda · {te} latihan esai. '
              'Pilih mata kuliah untuk mulai berlatih.</p></header>')
    isi = f'<h2>Mata kuliah</h2>\n<div class="grid">\n{kartu}\n</div>'
    open(os.path.join(keluar, "index.html"), "w", encoding="utf-8").write(
        halaman(f"Semester {nomor}", kepala, isi, f"Semester {nomor} · Latihan Ujian UT {PRODI}"))
    return int(nomor), rows


def main():
    tpl = open(os.path.join(SRC, "template.html"), encoding="utf-8").read()
    semua = []
    for folder in sorted(glob.glob(os.path.join(SRC, "semester-*")), key=lambda p: int(p.rsplit("-", 1)[1])):
        if not os.path.isfile(os.path.join(folder, "soal.py")):
            continue
        print(os.path.basename(folder))
        semua.append(bangun_semester(folder, tpl))
    tq = sum(r[2] for _, rows in semua for r in rows)
    te = sum(r[3] for _, rows in semua for r in rows)
    tm = sum(len(rows) for _, rows in semua)
    kartu = "\n".join(
        f'<a class="card" href="semester-{n}/index.html" data-kode="{",".join(r[0] for r in rows)}" data-n="{sum(r[2] for r in rows)}">'
        f'<span class="code">SEMESTER {n}</span><span class="nama">Semester {n}</span>'
        f'<span class="meta">{len(rows)} mata kuliah · {sum(r[2] for r in rows)} soal · {sum(r[3] for r in rows)} esai</span>'
        f'<div class="isi">Belum mulai</div><span class="go">Lihat mata kuliah →</span></a>' for n, rows in semua)
    kepala = (f'<header class="hero"><span class="eyebrow">Universitas Terbuka · {html.escape(PRODI)}</span>'
              '<h1>Latihan Ujian</h1>'
              '<p class="lead">Latihan soal pilihan ganda dan esai per sesi tutorial, lengkap dengan simulasi berwaktu, '
              'kartu hafalan, dan perkiraan nilai. Gratis, bisa dipakai di HP, tanpa daftar akun.</p>'
              f'<div class="stats"><div class="stat"><b>{len(semua)}</b><span>semester</span></div>'
              f'<div class="stat"><b>{tm}</b><span>mata kuliah</span></div>'
              f'<div class="stat"><b>{tq}</b><span>soal pilihan ganda</span></div>'
              f'<div class="stat"><b>{te}</b><span>latihan esai</span></div></div></header>')
    isi = ('<h2>Pilih semester</h2>\n<div class="grid">\n' + kartu + '\n</div>'
           '<h2>Cara belajar yang disarankan</h2><div class="steps">'
           '<div class="step"><b>Latihan per sesi</b><span>Kerjakan sesi demi sesi; penjelasan muncul setelah menjawab.</span></div>'
           '<div class="step"><b>Ulangi yang salah</b><span>Setiap hari, ulangi soal yang pernah salah sampai semuanya benar.</span></div>'
           '<div class="step"><b>Simulasi berwaktu</b><span>Menjelang ujian, ukur kesiapan dengan simulasi dan pantau perkiraan nilai.</span></div></div>')
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(
        halaman("Latihan Ujian", kepala, isi, f"Latihan Ujian UT · {PRODI}"))
    print(f"Total: {len(semua)} semester, {tq} soal")


if __name__ == "__main__":
    main()
