<?php
/*
 * Referenzen jetzt abgleichen: startet den GitHub-Workflow "Referenzen-Vorschauen erzeugen".
 * Zugangsdaten stehen in referenzen/_konfig.php (nicht im Code, nicht öffentlich abrufbar):
 *
 *   <?php return ['passwort' => '...', 'token' => 'github_pat_...'];
 */
session_set_cookie_params(['lifetime' => 0, 'path' => '/referenzen/', 'secure' => true, 'httponly' => true, 'samesite' => 'Strict']);
session_start();
header('X-Robots-Tag: noindex, nofollow');
header('X-Frame-Options: DENY');
header('Cache-Control: no-store');

const REPO = 'alexanderwindisch2503-lab/capeeshee_website';
const WORKFLOW = 'referenzen.yml';

$konfigDatei = __DIR__ . '/_konfig.php';
$k = is_file($konfigDatei) ? include $konfigDatei : null;
$bereit = is_array($k) && !empty($k['passwort']) && !empty($k['token']);

function gh($methode, $pfad, $token, $daten = null) {
  $url = 'https://api.github.com/repos/' . REPO . $pfad;
  $kopf = ['Authorization: Bearer ' . $token, 'Accept: application/vnd.github+json', 'X-GitHub-Api-Version: 2022-11-28', 'User-Agent: capeeshee-abgleich'];
  $body = $daten === null ? null : json_encode($daten);
  if ($body !== null) $kopf[] = 'Content-Type: application/json';
  if (function_exists('curl_init')) {
    $c = curl_init($url);
    curl_setopt_array($c, [CURLOPT_CUSTOMREQUEST => $methode, CURLOPT_HTTPHEADER => $kopf, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 20]);
    if ($body !== null) curl_setopt($c, CURLOPT_POSTFIELDS, $body);
    $antwort = curl_exec($c);
    $code = (int)curl_getinfo($c, CURLINFO_HTTP_CODE);
    curl_close($c);
  } else {
    $ctx = stream_context_create(['http' => ['method' => $methode, 'header' => implode("\r\n", $kopf), 'content' => $body ?? '', 'ignore_errors' => true, 'timeout' => 20]]);
    $antwort = @file_get_contents($url, false, $ctx);
    $code = isset($http_response_header[0]) && preg_match('/\s(\d{3})\s/', $http_response_header[0], $m) ? (int)$m[1] : 0;
  }
  return [$code, $antwort ? json_decode($antwort, true) : null];
}

if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(16));
$meldung = ''; $art = '';
$angemeldet = !empty($_SESSION['ok']);

if ($bereit && $_SERVER['REQUEST_METHOD'] === 'POST' && hash_equals($_SESSION['csrf'], (string)($_POST['csrf'] ?? ''))) {
  if (isset($_POST['passwort'])) {
    if (hash_equals((string)$k['passwort'], (string)$_POST['passwort'])) {
      session_regenerate_id(true); $_SESSION['ok'] = 1; $angemeldet = true;
    } else {
      sleep(2); $meldung = 'Das Passwort stimmt nicht.'; $art = 'fehler';
    }
  } elseif ($angemeldet && isset($_POST['abgleichen'])) {
    [$code] = gh('POST', '/actions/workflows/' . WORKFLOW . '/dispatches', $k['token'], ['ref' => 'main']);
    if ($code === 204) { $meldung = 'Der Abgleich ist gestartet. In ein bis drei Minuten sind neue Arbeiten online.'; $art = 'ok'; $_SESSION['gestartet'] = time(); }
    else { $meldung = 'Start nicht möglich (Code ' . $code . '). Bitte den Zugangsschlüssel prüfen.'; $art = 'fehler'; }
  } elseif (isset($_POST['abmelden'])) {
    $_SESSION = []; session_destroy(); header('Location: abgleich.php'); exit;
  }
}

$laeufe = [];
if ($bereit && $angemeldet) {
  [$code, $d] = gh('GET', '/actions/workflows/' . WORKFLOW . '/runs?per_page=5', $k['token']);
  if ($code === 200 && !empty($d['workflow_runs'])) $laeufe = $d['workflow_runs'];
}
$laeuft = false;
foreach ($laeufe as $l) if ($l['status'] !== 'completed') $laeuft = true;
if (!$laeuft && !empty($_SESSION['gestartet']) && time() - $_SESSION['gestartet'] < 20) $laeuft = true;

function zeit($iso) {
  $t = new DateTime($iso); $t->setTimezone(new DateTimeZone('Europe/Berlin'));
  return $t->format('d.m.Y, H:i') . ' Uhr';
}
function status($l) {
  if ($l['status'] !== 'completed') return ['läuft gerade', 'laeuft'];
  return $l['conclusion'] === 'success' ? ['erfolgreich', 'ok'] : ['fehlgeschlagen', 'fehler'];
}
$e = function ($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); };
?><!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>Referenzen abgleichen · Capeeshee</title>
<?php if ($laeuft): ?><meta http-equiv="refresh" content="15"><?php endif; ?>
<link rel="stylesheet" href="../fonts.css">
<style>
:root{--ink:#303133;--text:#5f6164;--muted:#8a8c8f;--line:#e6e1dc;--red:#9e4015;--bg:#f8f4f0;color-scheme:light}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;background:var(--bg);color:var(--text);font-family:Yantramanav,system-ui,sans-serif;font-weight:300;font-size:17px;line-height:1.5;display:flex;align-items:flex-start;justify-content:center;padding:clamp(24px,8vh,80px) max(16px,env(safe-area-inset-right,0px)) 40px max(16px,env(safe-area-inset-left,0px))}
main{width:100%;max-width:520px;background:#fff;padding:clamp(24px,5vw,40px)}
.logo{display:block;width:180px;margin-bottom:28px}
h1{font-family:Poppins,sans-serif;font-weight:800;font-size:30px;letter-spacing:-.03em;line-height:1.1;color:var(--ink);margin:0 0 10px}
p{margin:0 0 18px}
label{display:block;font-size:13px;text-transform:uppercase;letter-spacing:.14em;color:var(--muted);margin-bottom:8px}
input[type=password]{width:100%;font:inherit;font-weight:400;padding:12px 14px;border:1px solid var(--line);border-radius:4px;margin-bottom:16px}
button{font:600 15px "Titillium Web",Poppins,sans-serif;letter-spacing:.08em;text-transform:uppercase;border:0;border-radius:4px;background:var(--red);color:#fff;padding:16px 22px;cursor:pointer;width:100%}
button:hover{background:#8c3024}
button[disabled]{opacity:.55;cursor:wait}
.klein{background:none;color:var(--muted);width:auto;padding:0;font-size:12px;margin-top:22px}
.klein:hover{background:none;color:var(--red)}
.m{padding:12px 14px;border-radius:4px;margin-bottom:18px;font-weight:400}
.m.ok{background:#eef4e8;color:#2f5a1f}.m.fehler{background:#f8e4df;color:#8c3024}
ul{list-style:none;margin:26px 0 0;padding:0;border-top:1px solid var(--line)}
li{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-bottom:1px solid var(--line);font-size:15px}
.s{font-weight:500}.s.ok{color:#2f5a1f}.s.fehler{color:#8c3024}.s.laeuft{color:var(--red)}
h2{font-size:13px;text-transform:uppercase;letter-spacing:.14em;color:var(--muted);font-weight:400;margin:30px 0 0}
</style>
</head>
<body>
<main>
  <img class="logo" src="../img/logo-capeeshee.svg" alt="Capeeshee">
  <h1>Referenzen abgleichen</h1>
<?php if (!$bereit): ?>
  <p>Diese Seite ist noch nicht eingerichtet. Es fehlt die Datei <b>_konfig.php</b> mit Passwort und Zugangsschlüssel im Ordner referenzen.</p>
<?php elseif (!$angemeldet): ?>
  <p>Bitte melden Sie sich an.</p>
  <?php if ($meldung): ?><div class="m <?= $art ?>"><?= $e($meldung) ?></div><?php endif; ?>
  <form method="post">
    <input type="hidden" name="csrf" value="<?= $e($_SESSION['csrf']) ?>">
    <label for="pw">Passwort</label>
    <input id="pw" type="password" name="passwort" autocomplete="current-password" required autofocus>
    <button type="submit">Anmelden</button>
  </form>
<?php else: ?>
  <p>Neue oder geänderte Dateien im Ordner referenzen werden umgewandelt und erscheinen danach auf capeeshee.com. Automatisch passiert das jede Nacht gegen 3 Uhr.</p>
  <?php if ($meldung): ?><div class="m <?= $art ?>"><?= $e($meldung) ?></div><?php endif; ?>
  <form method="post">
    <input type="hidden" name="csrf" value="<?= $e($_SESSION['csrf']) ?>">
    <button type="submit" name="abgleichen" value="1"<?= $laeuft ? ' disabled' : '' ?>><?= $laeuft ? 'Abgleich läuft …' : 'Jetzt abgleichen' ?></button>
  </form>
  <?php if ($laeufe): ?>
  <h2>Letzte Abgleiche</h2>
  <ul>
    <?php foreach ($laeufe as $l): [$txt, $cls] = status($l); ?>
    <li><span><?= $e(zeit($l['created_at'])) ?><?= $l['event'] === 'schedule' ? ' · nachts' : '' ?></span><span class="s <?= $cls ?>"><?= $e($txt) ?></span></li>
    <?php endforeach; ?>
  </ul>
  <?php endif; ?>
  <form method="post"><input type="hidden" name="csrf" value="<?= $e($_SESSION['csrf']) ?>"><button class="klein" type="submit" name="abmelden" value="1">Abmelden</button></form>
<?php endif; ?>
</main>
</body>
</html>
