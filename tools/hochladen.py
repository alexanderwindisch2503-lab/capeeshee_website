#!/usr/bin/env python3
"""Lädt den Ordner site/ per SFTP auf den Webspace (wie lftp mirror -R, ohne Löschen).
Zugangsdaten nur aus den Umgebungsvariablen SFTP_HOST, SFTP_USER, SFTP_PASSWORD, SFTP_PATH."""
import os, stat, sys, time
import paramiko

QUELLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')

def verbinden(e):
    for versuch in range(3):
        try:
            t = paramiko.Transport((e['SFTP_HOST'], 22))
            t.banner_timeout = 30
            t.connect(username=e['SFTP_USER'], password=e['SFTP_PASSWORD'])
            return t, paramiko.SFTPClient.from_transport(t)
        except Exception as x:
            print(f'Verbindung fehlgeschlagen ({x}), neuer Versuch …', flush=True)
            time.sleep(5 * (versuch + 1))
    sys.exit('Keine Verbindung zum Webspace möglich')

def ordner(s, pfad, bekannt):
    if pfad in bekannt or pfad in ('', '/'):
        return
    ordner(s, os.path.dirname(pfad), bekannt)
    try:
        if not stat.S_ISDIR(s.stat(pfad).st_mode):
            sys.exit(f'{pfad} ist kein Ordner')
    except IOError:
        s.mkdir(pfad)
    bekannt.add(pfad)

def main():
    e = os.environ
    ziel = e['SFTP_PATH'].rstrip('/')
    if ziel in ('', '.', '~'):
        sys.exit('SFTP_PATH darf nicht das Hauptverzeichnis sein')
    t, s = verbinden(e)
    bekannt, n = set(), 0
    for wurzel, _, dateien in os.walk(QUELLE):
        rel = os.path.relpath(wurzel, QUELLE)
        zordner = ziel if rel == '.' else f'{ziel}/{rel}'
        ordner(s, zordner, bekannt)
        for d in sorted(dateien):
            for versuch in range(3):
                try:
                    s.put(os.path.join(wurzel, d), f'{zordner}/{d}')
                    break
                except Exception as x:
                    if versuch == 2:
                        raise
                    print(f'Wiederhole {rel}/{d} ({x})', flush=True)
                    s.close(); t.close(); t, s = verbinden(e)
            n += 1
            print(f'Hochgeladen: {os.path.normpath(os.path.join(rel, d))}', flush=True)
    s.close(); t.close()
    print(f'Fertig: {n} Dateien hochgeladen, nichts gelöscht')

if __name__ == '__main__':
    main()
