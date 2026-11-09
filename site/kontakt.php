<?php
// Kontaktformular capeeshee.com: nimmt die Anfrage entgegen und leitet sie per E-Mail an info@capeeshee.com weiter.
// Es wird nichts gespeichert. Schutz gegen Spam: Honeypot-Feld, Mindestzeit, einfache Drosselung pro IP.
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

const EMPFAENGER = 'info@capeeshee.com';
const ABSENDER   = 'info@capeeshee.com';   // muss eine Adresse der eigenen Domain sein (Strato)

function antwort($ok, $text, $code = 200) {
  http_response_code($code);
  echo json_encode(['ok' => $ok, 'text' => $text], JSON_UNESCAPED_UNICODE);
  exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') antwort(false, 'Ungültige Anfrage.', 405);

// Nur Anfragen von der eigenen Website
$herkunft = $_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? '');
if ($herkunft !== '' && !preg_match('~^https?://(www\.)?capeeshee\.com(/|$)~i', $herkunft)
    && !preg_match('~^https?://(127\.0\.0\.1|localhost)(:\d+)?(/|$)~i', $herkunft)) {
  antwort(false, 'Ungültige Anfrage.', 403);
}

$feld = function ($n, $max) {
  $v = trim((string)($_POST[$n] ?? ''));
  if (function_exists('mb_substr')) $v = mb_substr($v, 0, $max, 'UTF-8'); else $v = substr($v, 0, $max);
  return $v;
};
$name  = $feld('name', 120);
$email = $feld('email', 160);
$text  = $feld('message', 5000);
$falle = $feld('website', 200);          // Honeypot: Menschen sehen das Feld nicht
$zeit  = (int)($_POST['t'] ?? 0);         // Zeitpunkt, zu dem das Formular geladen wurde (ms)

// Spam leise verwerfen, damit Bots keine Rückmeldung bekommen
if ($falle !== '') antwort(true, 'Danke! Ihre Nachricht ist bei uns angekommen.');
if ($zeit > 0 && (microtime(true) * 1000 - $zeit) < 3000) antwort(true, 'Danke! Ihre Nachricht ist bei uns angekommen.');

// Pflichtfelder prüfen
$name  = preg_replace('/[\r\n\t]+/', ' ', $name);
$email = preg_replace('/[\r\n\t ]+/', '', $email);
if ($name === '' || $email === '' || $text === '') antwort(false, 'Bitte füllen Sie Name, E-Mail und Nachricht aus.', 422);
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) antwort(false, 'Bitte prüfen Sie Ihre E-Mail-Adresse.', 422);

// Drosselung: höchstens 5 Nachrichten pro IP und Stunde (nur gehashte IP, wird nach einer Stunde verworfen)
$dir = sys_get_temp_dir() . '/capeeshee_kf';
@mkdir($dir, 0700, true);
$schluessel = $dir . '/' . hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . date('YmdH'));
$anzahl = is_file($schluessel) ? (int)file_get_contents($schluessel) : 0;
if ($anzahl >= 5) antwort(false, 'Sie haben bereits mehrere Nachrichten gesendet. Bitte versuchen Sie es später erneut oder schreiben Sie an info@capeeshee.com.', 429);
@file_put_contents($schluessel, (string)($anzahl + 1));
foreach (glob($dir . '/*') ?: [] as $f) { if (filemtime($f) < time() - 7200) @unlink($f); }

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
if (!$ok) antwort(false, 'Die Nachricht konnte leider nicht gesendet werden. Bitte schreiben Sie uns direkt an info@capeeshee.com.', 500);

antwort(true, 'Danke! Ihre Nachricht ist bei uns angekommen. Wir melden uns schnellstmöglich bei Ihnen.');
