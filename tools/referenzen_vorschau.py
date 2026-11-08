#!/usr/bin/env python3
"""Erzeugt Vorschaubilder für die Capeeshee-Referenzen.

Liest referenzen/<Kunde>/<Bereich>/[<Serie>/]<Datei> und legt zu jeder Quelldatei
<Ordner>/_vorschau/<Dateiname>/ an: meta.json plus Bilder (und bei Videos video.mp4).

  PDF           Seiten nach Dateiname (_s8, _s1-2,7, _alle; Standard 4), auf Endformat (TrimBox) beschnitten, CMYK -> RGB
  PPT/PPTX/ODP  über LibreOffice nach PDF, dann wie PDF
  Bilder        verkleinert, CMYK -> RGB, Drehung aus EXIF
  Videos        Webfassung (H.264, max. 1280 px breit) und Vorschaubild

Nur neue oder geänderte Dateien werden verarbeitet (Größe, Änderungszeit, Seitenauswahl in meta.json).
Vorschauen zu gelöschten Dateien werden entfernt.

Aufruf:
  python3 referenzen_vorschau.py --lokal /pfad/zu/referenzen
  python3 referenzen_vorschau.py --sftp            (Zugang aus SFTP_HOST, SFTP_USER, SFTP_PASSWORD, SFTP_PATH)
"""
import argparse, io, json, os, re, shutil, stat, subprocess, sys, tempfile
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = 400_000_000
VERSION = 1
FULL = 2000      # lange Seite Großansicht
THUMB = 720      # lange Seite Kachel
STANDARD_SEITEN = 4
MAX_GROESSE = 1_500_000_000

PDF = {'.pdf'}
OFFICE = {'.ppt', '.pptx', '.odp'}
BILD = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.tif', '.tiff'}
VIDEO = {'.mp4', '.mov', '.m4v', '.avi', '.mkv', '.wmv', '.mpg', '.mpeg'}
QUELLEN = PDF | OFFICE | BILD | VIDEO


def zeig(n):
    """Dateinamen lesbar ausgeben, auch wenn sie nicht in UTF-8 gespeichert sind (z. B. Umlaute aus Windows-FTP)."""
    raw = n.encode('utf-8', 'surrogateescape')
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return raw.decode('cp1252', 'replace')


def _paramiko_namen_tolerant():
    """paramiko erwartet UTF-8-Dateinamen. Andere Bytes (Windows-Umlaute) werden verlustfrei durchgereicht."""
    import paramiko
    mods = [getattr(paramiko, m) for m in ('util', 'message', 'sftp_client', 'sftp_attr', 'sftp', 'py3compat') if hasattr(paramiko, m)]
    def mk(name, orig):
        if name == 'u':
            def f(s, encoding='utf8'):
                if isinstance(s, bytes):
                    return s.decode('utf-8', 'surrogateescape')
                return orig(s) if not isinstance(s, str) else s
        else:
            def f(s, *a, **k):
                if isinstance(s, str):
                    return s.encode('utf-8', 'surrogateescape')
                return orig(s, *a, **k)
        return f
    for m in mods:
        for name in ('u', 'b', 'asbytes'):
            orig = getattr(m, name, None)
            if callable(orig) and not getattr(orig, '_cap', False):
                f = mk(name, orig); f._cap = True
                setattr(m, name, f)


def sichtbar(n):
    return bool(n) and n[0] not in '._'


# ---------- Dateisysteme ----------
class Lokal:
    def __init__(self, root):
        self.root = root.rstrip('/')
    def p(self, rel):
        return os.path.join(self.root, rel) if rel else self.root
    def liste(self, rel):
        out = []
        try:
            for n in os.listdir(self.p(rel)):
                st = os.stat(os.path.join(self.p(rel), n))
                out.append((n, stat.S_ISDIR(st.st_mode), st.st_size, int(st.st_mtime)))
        except FileNotFoundError:
            pass
        return out
    def lesen(self, rel):
        try:
            with open(self.p(rel), 'rb') as f:
                return f.read()
        except FileNotFoundError:
            return None
    def holen(self, rel, ziel):
        shutil.copyfile(self.p(rel), ziel)
    def ablegen(self, quelle, rel):
        os.makedirs(os.path.dirname(self.p(rel)), exist_ok=True)
        shutil.copyfile(quelle, self.p(rel))
    def schreiben(self, rel, daten):
        os.makedirs(os.path.dirname(self.p(rel)), exist_ok=True)
        with open(self.p(rel), 'wb') as f:
            f.write(daten)
    def ordner_loeschen(self, rel):
        shutil.rmtree(self.p(rel), ignore_errors=True)


class Sftp:
    def __init__(self, host, user, pw, root):
        import paramiko
        _paramiko_namen_tolerant()
        self.t = paramiko.Transport((host, 22))
        self.t.connect(username=user, password=pw)
        self.s = paramiko.SFTPClient.from_transport(self.t)
        self.root = root.rstrip('/')
    def p(self, rel):
        return f'{self.root}/{rel}' if rel else self.root
    def liste(self, rel):
        try:
            return [(a.filename, stat.S_ISDIR(a.st_mode), a.st_size, int(a.st_mtime)) for a in self.s.listdir_attr(self.p(rel))]
        except IOError:
            return []
    def lesen(self, rel):
        try:
            with self.s.open(self.p(rel), 'rb') as f:
                return f.read()
        except IOError:
            return None
    def holen(self, rel, ziel):
        self.s.get(self.p(rel), ziel)
    def _mkdirs(self, rel):
        teile, cur = rel.split('/'), self.root
        for t in teile:
            cur = f'{cur}/{t}'
            try:
                self.s.stat(cur)
            except IOError:
                self.s.mkdir(cur)
    def ablegen(self, quelle, rel):
        self._mkdirs(os.path.dirname(rel))
        self.s.put(quelle, self.p(rel))
    def schreiben(self, rel, daten):
        self._mkdirs(os.path.dirname(rel))
        with self.s.open(self.p(rel), 'wb') as f:
            f.write(daten)
    def ordner_loeschen(self, rel):
        def rm(path):
            for a in self.s.listdir_attr(path):
                q = f'{path}/{a.filename}'
                if stat.S_ISDIR(a.st_mode):
                    rm(q)
                else:
                    self.s.remove(q)
            self.s.rmdir(path)
        try:
            rm(self.p(rel))
        except IOError:
            pass


# ---------- Seitenauswahl ----------
def seiten_spec(dateiname):
    stem = os.path.splitext(dateiname)[0]
    m = re.search(r'_(s[\d,\-]+|alle)$', stem, re.I)
    return m.group(1).lower() if m else f's{STANDARD_SEITEN}'


def seiten_aus_spec(spec, anzahl):
    if spec == 'alle':
        return list(range(1, anzahl + 1))
    body = spec[1:]
    if re.fullmatch(r'\d+', body):
        return list(range(1, min(int(body), anzahl) + 1))
    out = []
    for teil in body.split(','):
        if '-' in teil:
            a, b = teil.split('-', 1)
            if a.isdigit() and b.isdigit():
                out += range(int(a), int(b) + 1)
        elif teil.isdigit():
            out.append(int(teil))
    out = [p for p in dict.fromkeys(out) if 1 <= p <= anzahl]
    return out or [1]


# ---------- Umwandlung ----------
def sichern(img, ordner, nr):
    img = ImageOps.exif_transpose(img)
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGBA')
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[-1])
        img = bg
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    full = img.copy(); full.thumbnail((FULL, FULL), Image.LANCZOS)
    th = img.copy(); th.thumbnail((THUMB, THUMB), Image.LANCZOS)
    fn, tn = f'{nr:03d}.jpg', f'{nr:03d}_t.jpg'
    full.save(os.path.join(ordner, fn), 'JPEG', quality=85, optimize=True, progressive=True)
    th.save(os.path.join(ordner, tn), 'JPEG', quality=80, optimize=True, progressive=True)
    return {'full': fn, 'thumb': tn, 'w': full.width, 'h': full.height}


def boxen(pdf, seite):
    out = subprocess.run(['pdfinfo', '-f', str(seite), '-l', str(seite), '-box', pdf], capture_output=True, text=True).stdout
    b = {}
    for z in out.splitlines():
        m = re.match(r'Page\s+\d+\s+(MediaBox|CropBox|TrimBox):\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)', z)
        if m:
            b[m.group(1)] = tuple(float(x) for x in m.groups()[1:])
    return b


def pdf_seiten(pdf):
    r = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True)
    m = re.search(r'^Pages:\s+(\d+)', r.stdout, re.M)
    if m:
        return int(m.group(1))
    with open(pdf, 'rb') as f:
        kopf = f.read(16)
    groesse = os.path.getsize(pdf)
    raise RuntimeError(f'PDF nicht lesbar ({groesse} Bytes, Anfang {kopf!r}): {r.stderr.strip()[:300]}')


def pdf_umwandeln(pdf, spec, ordner):
    n = pdf_seiten(pdf)
    items = []
    for i, s in enumerate(seiten_aus_spec(spec, n), 1):
        b = boxen(pdf, s)
        media = b.get('MediaBox')
        trim = b.get('TrimBox') or b.get('CropBox') or media
        if not media:
            continue
        lang = max(trim[2] - trim[0], trim[3] - trim[1]) or 1
        dpi = max(36, min(300, int(FULL * 1.15 * 72 / lang)))
        base = os.path.join(ordner, f'_seite{s}')
        subprocess.run(['pdftoppm', '-f', str(s), '-l', str(s), '-r', str(dpi), '-png', '-singlefile', pdf, base], check=True, capture_output=True)
        img = Image.open(base + '.png')
        k = dpi / 72.0
        x0 = (trim[0] - media[0]) * k; y0 = (media[3] - trim[3]) * k
        x1 = (trim[2] - media[0]) * k; y1 = (media[3] - trim[1]) * k
        box = (max(0, round(x0)), max(0, round(y0)), min(img.width, round(x1)), min(img.height, round(y1)))
        if box[2] - box[0] > 10 and box[3] - box[1] > 10:
            img = img.crop(box)
        items.append(sichern(img, ordner, i))
        os.remove(base + '.png')
    return {'type': 'dokument' if len(items) > 1 else 'bild', 'items': items}


def office_umwandeln(datei, spec, ordner, tmp):
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp, datei], check=True, capture_output=True, timeout=600)
    pdf = os.path.join(tmp, os.path.splitext(os.path.basename(datei))[0] + '.pdf')
    r = pdf_umwandeln(pdf, spec, ordner)
    r['type'] = 'praesentation'
    return r


def bild_umwandeln(datei, ordner):
    img = Image.open(datei)
    img.seek(0)
    return {'type': 'bild', 'items': [sichern(img, ordner, 1)]}


def video_umwandeln(datei, ordner):
    vid = os.path.join(ordner, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', datei, '-vf', "scale='min(1280,iw)':-2", '-c:v', 'libx264', '-preset', 'veryfast',
                    '-crf', '26', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', vid], check=True, capture_output=True, timeout=3600)
    png = os.path.join(ordner, '_poster.png')
    dauer = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', vid], capture_output=True, text=True).stdout.strip()
    ss = '1' if not dauer or float(dauer) > 2 else '0'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', ss, '-i', vid, '-frames:v', '1', png], check=True, capture_output=True)
    it = sichern(Image.open(png), ordner, 1)
    os.remove(png)
    return {'type': 'video', 'items': [it], 'video': 'video.mp4'}


# ---------- Durchlauf ----------
def quellen(fs):
    """Liefert (ordner_rel, dateiname, groesse, mtime) aller Quelldateien und die Liste aller Ordner mit Dateien."""
    funde, ordner = [], []
    def datei_ordner(rel):
        eintraege = fs.liste(rel)
        ordner.append((rel, {n for n, d, *_ in eintraege if not d}))
        for n, d, g, m in eintraege:
            if not d and sichtbar(n) and os.path.splitext(n)[1].lower() in QUELLEN:
                funde.append((rel, n, g, m))
        return eintraege
    for k, kd, *_ in fs.liste(''):
        if not kd or not sichtbar(k):
            continue
        for b, bd, *_ in fs.liste(k):
            if bd and b == '_kachel':
                datei_ordner(f'{k}/{b}')   # eigene Kachelbilder
                continue
            if not bd or not sichtbar(b):
                continue
            for e, ed, *_ in datei_ordner(f'{k}/{b}'):
                if ed and sichtbar(e):
                    datei_ordner(f'{k}/{b}/{e}')
    return funde, ordner


def verarbeiten(fs, nur_pruefen=False):
    funde, ordner = quellen(fs)
    neu = fehler = 0
    for rel, name, groesse, mtime in funde:
        vrel = f'{rel}/_vorschau/{name}'
        spec = seiten_spec(name)
        alt = fs.lesen(f'{vrel}/meta.json')
        if alt:
            try:
                a = json.loads(alt)
                if a.get('v') == VERSION and a.get('size') == groesse and a.get('mtime') == mtime and a.get('spec', spec) == spec:
                    continue
            except ValueError:
                pass
        if groesse > MAX_GROESSE:
            print(f'Übersprungen (zu groß): {zeig(rel)}/{zeig(name)}'); continue
        print(f'Erzeuge Vorschau: {zeig(rel)}/{zeig(name)}', flush=True)
        if nur_pruefen:
            continue
        ext = os.path.splitext(name)[1].lower()
        with tempfile.TemporaryDirectory() as tmp:
            quelle = os.path.join(tmp, 'quelle' + ext)
            ziel = os.path.join(tmp, 'out'); os.makedirs(ziel)
            try:
                fs.holen(f'{rel}/{name}', quelle)
                if ext in PDF:
                    r = pdf_umwandeln(quelle, spec, ziel)
                elif ext in OFFICE:
                    r = office_umwandeln(quelle, spec, ziel, tmp)
                elif ext in VIDEO:
                    r = video_umwandeln(quelle, ziel)
                else:
                    r = bild_umwandeln(quelle, ziel)
                if not r['items']:
                    raise RuntimeError('keine Seiten erzeugt')
                fs.ordner_loeschen(vrel)
                for f in sorted(os.listdir(ziel)):
                    fs.ablegen(os.path.join(ziel, f), f'{vrel}/{f}')
                meta = dict(r, v=VERSION, src=zeig(name), size=groesse, mtime=mtime, spec=spec)
                fs.schreiben(f'{vrel}/meta.json', json.dumps(meta).encode())
                neu += 1
            except Exception as e:  # eine kaputte Datei soll den Rest nicht aufhalten
                fehler += 1
                print(f'::warning::Vorschau fehlgeschlagen für {zeig(rel)}/{zeig(name)}: {e}', flush=True)
    # Vorschauen ohne Quelldatei entfernen
    entfernt = 0
    for rel, dateien in ordner:
        for n, d, *_ in fs.liste(f'{rel}/_vorschau'):
            if d and n not in dateien:
                print(f'Entferne alte Vorschau: {zeig(rel)}/_vorschau/{zeig(n)}')
                if not nur_pruefen:
                    fs.ordner_loeschen(f'{rel}/_vorschau/{n}')
                entfernt += 1
    print(f'Fertig: {len(funde)} Dateien, {neu} neu erzeugt, {entfernt} entfernt, {fehler} Fehler')
    return fehler


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--lokal')
    g.add_argument('--sftp', action='store_true')
    ap.add_argument('--pruefen', action='store_true', help='nur anzeigen, nichts ändern')
    a = ap.parse_args()
    if a.lokal:
        fs = Lokal(a.lokal)
    else:
        e = os.environ
        root = e['SFTP_PATH'].rstrip('/') + '/referenzen'
        fs = Sftp(e['SFTP_HOST'], e['SFTP_USER'], e['SFTP_PASSWORD'], root)
    verarbeiten(fs, a.pruefen)


if __name__ == '__main__':
    main()
