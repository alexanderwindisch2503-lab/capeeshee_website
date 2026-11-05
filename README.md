# capeeshee.com

Website der Agentur Capeeshee.

- `site/` – die fertige Website (wird 1:1 veröffentlicht)
- Jeder Push auf `main` veröffentlicht automatisch per SFTP auf den Strato-Webspace (siehe `.github/workflows/deploy.yml`).
- Benötigte Repository-Secrets: `SFTP_HOST`, `SFTP_USER`, `SFTP_PASSWORD`, `SFTP_PATH`.
- Bis zum offiziellen Start: `robots.txt` und `noindex` verhindern die Aufnahme bei Google.
