<?php
// Kontaktformular capeeshee.com: nimmt die Anfrage entgegen und leitet sie per E-Mail an info@capeeshee.com weiter.
// Es werden keine Anfragen gespeichert.
//
// Schutz gegen Spam (für Besucher unsichtbar):
//  1. Honeypot-Feld, das nur Bots ausfüllen
//  2. Rechenaufgabe (Proof of Work nach dem ALTCHA-Prinzip, selbst gehostet, ohne Cookies und Drittanbieter):
//     GET kontakt.php?aufgabe=1 liefert eine signierte Aufgabe, der Browser löst sie im Hintergrund.
//     Jede Lösung gilt nur einmal und nur zwischen 3 Sekunden und 2 Stunden nach dem Abruf (ersetzt die alte Zeitprüfung).
//  3. Inhaltsfilter: viele Links, HTML- oder BBCode-Links, überwiegend fremde Schriftzeichen
//  4. Drosselung: höchstens 3 Nachrichten pro IP und Stunde (nur gehashte IP, nach zwei Stunden verworfen)
// Bots bekommen trotzdem eine Erfolgsmeldung. Abgewiesene Versuche werden nur mit Datum und Grund
// (ohne Namen, Adressen oder Inhalte) in _cache/kontakt/protokoll.log vermerkt.
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

const EMPFAENGER   = 'info@capeeshee.com';
const ABSENDER     = 'info@capeeshee.com';   // muss eine Adresse der eigenen Domain sein (Strato)
const AUFGABE_MAX  = 60000;                  // Schwierigkeit der Rechenaufgabe (im Schnitt ca. 0,5 bis 1,5 Sekunden im Browser)
const MIN_SEKUNDEN = 3;
const MAX_SEKUNDEN = 7200;
const PRO_STUNDE   = 3;
const DANKE        = 'Danke! Ihre Nachricht ist bei uns angekommen. Wir melden uns schnellstmöglich bei Ihnen.';

function antwort($ok, $text, $code = 200, $extra = []) {
  http_response_code($code);
  echo json_encode(['ok' => $ok, 'text' => $text] + $extra, JSON_UNESCAPED_UNICODE);
  exit;
}

// Arbeitsordner auf dem Server (wird beim Veröffentlichen nicht überschrieben, ist von außen gesperrt)
function ordner() {
  static $dir = null;
  if ($dir !== null) return $dir;
  $dir = __DIR__ . '/_cache/kontakt';
  if (!is_dir($dir)) @mkdir($dir, 0700, true);
  if (!is_dir($dir) || !is_writable($dir)) {
    $dir = sys_get_temp_dir() . '/capeeshee_kf';
    if (!is_dir($dir)) @mkdir($dir, 0700, true);
  } else {
    $sperre = dirname($dir) . '/.htaccess';
    if (!is_file($sperre)) @file_put_contents($sperre, "Require all denied\n<IfModule !mod_authz_core.c>\n  Deny from all\n</IfModule>\n");
  }
  return $dir;
}

// Geheimer Schlüssel zum Signieren der Aufgaben, wird beim ersten Aufruf auf dem Server erzeugt
function schluessel() {
  $datei = ordner() . '/schluessel.php';
  if (is_file($datei)) {
    $k = include $datei;
    if (is_string($k) && strlen($k) >= 32) return $k;
  }
  $k = bin2hex(random_bytes(32));
  @file_put_contents($datei, "<?php return '" . $k . "';\n", LOCK_EX);
  @chmod($datei, 0600);
  return $k;
}

function protokoll($grund) {
  $datei = ordner() . '/protokoll.log';
  if (is_file($datei) && filesize($datei) > 300000) {
    $zeilen = file($datei);
    @file_put_contents($datei, implode('', array_slice($zeilen, -2000)), LOCK_EX);
  }
  @file_put_contents($datei, date('Y-m-d H:i:s') . "\t" . $grund . "\n", FILE_APPEND | LOCK_EX);
}

// Spam leise verwerfen, damit Bots nicht lernen, welche Prüfung greift
function verwerfen($grund) {
  protokoll('abgewiesen: ' . $grund);
  antwort(true, DANKE);
}

// Nur Anfragen von der eigenen Website
$herkunft = $_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? '');
$eigen = $herkunft === '' || preg_match('~^https?://(www\.)?capeeshee\.com(/|$)~i', $herkunft)
      || preg_match('~^https?://(127\.0\.0\.1|localhost)(:\d+)?(/|$)~i', $herkunft);

// Aufgabe ausgeben
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'GET' && isset($_GET['aufgabe'])) {
  if (!$eigen) antwort(false, 'Ungültige Anfrage.', 403);
  $salz = bin2hex(random_bytes(12)) . '.' . time();
  $zahl = random_int(0, AUFGABE_MAX);
  $aufgabe = hash('sha256', $salz . $zahl);
  echo json_encode([
    'algorithm' => 'SHA-256',
    'challenge' => $aufgabe,
    'salt'      => $salz,
    'maxnumber' => AUFGABE_MAX,
    'signature' => hash_hmac('sha256', $aufgabe, schluessel()),
  ]);
  exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') antwort(false, 'Ungültige Anfrage.', 405);
if (!$eigen) antwort(false, 'Ungültige Anfrage.', 403);

$feld = function ($n, $max) {
  $v = trim((string)($_POST[$n] ?? ''));
  if (function_exists('mb_substr')) $v = mb_substr($v, 0, $max, 'UTF-8'); else $v = substr($v, 0, $max);
  return $v;
};
$name  = $feld('name', 120);
$email = $feld('email', 160);
$text  = $feld('message', 5000);
$falle = $feld('website', 200);          // Honeypot: Menschen sehen das Feld nicht

// 1. Honeypot
if ($falle !== '') verwerfen('Honeypot');

// Pflichtfelder prüfen
$name  = preg_replace('/[\r\n\t]+/', ' ', $name);
$email = preg_replace('/[\r\n\t ]+/', '', $email);
if ($name === '' || $email === '' || $text === '') antwort(false, 'Bitte füllen Sie Name, E-Mail und Nachricht aus.', 422);
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) antwort(false, 'Bitte prüfen Sie Ihre E-Mail-Adresse.', 422);

// 2. Rechenaufgabe prüfen
$loesung = json_decode((string)($_POST['pow'] ?? ''), true);
if (!is_array($loesung) || !isset($loesung['salt'], $loesung['number'], $loesung['signature'])
    || !is_string($loesung['salt']) || !is_string($loesung['signature']) || !is_numeric($loesung['number'])) {
  verwerfen('ohne Rechenaufgabe');
}
$salz = $loesung['salt'];
$zahl = (int)$loesung['number'];
$aufgabe = hash('sha256', $salz . $zahl);
if (!preg_match('/^[0-9a-f]{24}\.(\d{10})$/', $salz, $m) || $zahl < 0 || $zahl > AUFGABE_MAX
    || !hash_equals(hash_hmac('sha256', $aufgabe, schluessel()), $loesung['signature'])) {
  verwerfen('Rechenaufgabe falsch');
}
$alter = time() - (int)$m[1];
if ($alter < MIN_SEKUNDEN) verwerfen('zu schnell abgeschickt');
if ($alter > MAX_SEKUNDEN) antwort(false, 'Die Seite war sehr lange geöffnet. Bitte senden Sie noch einmal.', 409, ['neu' => true]);
// Jede Lösung nur einmal
$benutzt = ordner() . '/b_' . substr(hash('sha256', $salz), 0, 32);
if (is_file($benutzt)) antwort(false, 'Bitte senden Sie noch einmal.', 409, ['neu' => true]);
@file_put_contents($benutzt, '1');

// 3. Inhaltsfilter (bewusst großzügig, damit keine echte Anfrage verloren geht)
$links = preg_match_all('~(https?://|www\.)~i', $text);
if ($links > 2) verwerfen('mehr als 2 Links');
if (preg_match('~(https?://|www\.)~i', $name)) verwerfen('Link im Namen');
if (preg_match('~<a\s|\[url|\[link=~i', $text)) verwerfen('HTML- oder BBCode-Link');
$buchstaben = preg_match_all('/\p{L}/u', $text);
$fremd = preg_match_all('/[\p{Cyrillic}\p{Han}\p{Hiragana}\p{Katakana}\p{Hangul}\p{Arabic}\p{Thai}\p{Hebrew}]/u', $text . ' ' . $name);
if ($buchstaben > 0 && $fremd / $buchstaben > 0.3) verwerfen('fremde Schriftzeichen');

// 4. Drosselung: höchstens 3 Nachrichten pro IP und Stunde (nur gehashte IP)
$schluesselIp = ordner() . '/ip_' . hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . date('YmdH'));
$anzahl = is_file($schluesselIp) ? (int)file_get_contents($schluesselIp) : 0;
if ($anzahl >= PRO_STUNDE) {
  protokoll('gedrosselt');
  antwort(false, 'Sie haben bereits mehrere Nachrichten gesendet. Bitte versuchen Sie es später erneut oder schreiben Sie an info@capeeshee.com.', 429);
}
@file_put_contents($schluesselIp, (string)($anzahl + 1));

// Aufräumen: Drosselung und benutzte Aufgaben nach zwei Stunden löschen
foreach (array_merge(glob(ordner() . '/ip_*') ?: [], glob(ordner() . '/b_*') ?: []) as $f) {
  if (filemtime($f) < time() - 7200) @unlink($f);
}

// E-Mail zusammenstellen
$betreff = 'Anfrage über capeeshee.com von ' . $name;
$betreffKodiert = '=?UTF-8?B?' . base64_encode($betreff) . '?=';
$nameKodiert = '=?UTF-8?B?' . base64_encode($name) . '?=';
$inhalt = "Neue Anfrage über das Kontaktformular auf capeeshee.com\n\n"
        . "Name:   $name\n"
        . "E-Mail: $email\n"
        . "Datum:  " . date('d.m.Y H:i') . " Uhr\n\n"
        . "Nachricht:\n" . $text . "\n\n"
        . "--\nAntworten Sie einfach auf diese E-Mail, die Antwort geht direkt an $email.\n";

$kopf  = "From: Website Capeeshee <" . ABSENDER . ">\r\n";
$kopf .= "Reply-To: $nameKodiert <$email>\r\n";
$kopf .= "MIME-Version: 1.0\r\n";
$kopf .= "Content-Type: text/plain; charset=UTF-8\r\n";
$kopf .= "Content-Transfer-Encoding: 8bit\r\n";
$kopf .= "X-Mailer: capeeshee.com Kontaktformular";

$ok = @mail(EMPFAENGER, $betreffKodiert, $inhalt, $kopf, '-f' . ABSENDER);
if (!$ok) {
  protokoll('Versand fehlgeschlagen');
  antwort(false, 'Die Nachricht konnte leider nicht gesendet werden. Bitte schreiben Sie uns direkt an info@capeeshee.com.', 500);
}
protokoll('gesendet');
antwort(true, DANKE);
