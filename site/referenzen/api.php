<?php
/*
 * Capeeshee Referenzen: liest die Ordnerstruktur und liefert sie als JSON.
 *
 *   referenzen/<Kunde>/<Bereich>/<Datei>
 *   referenzen/<Kunde>/<Bereich>/<Serie>/<Dateien>   (Unterordner = eine Arbeit mit mehreren Varianten)
 *   referenzen/<Kunde>/info.txt                       (Name, Branche, Ort, Zeitraum, Text)
 *
 * Vorschaubilder legt der Umwandlungs-Automatismus in <Ordner>/_vorschau/<Dateiname>/ ab
 * (meta.json + Bilder). Bilder ohne Vorschau werden direkt angezeigt, PDFs, Präsentationen
 * und Videos erscheinen erst, wenn ihre Vorschau erzeugt ist.
 */

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

$BASE = __DIR__;
$CACHE_DIR = $BASE . '/_cache';
$CACHE_FILE = $CACHE_DIR . '/index.json';
$CACHE_SEC = 300;

// Feste Bereiche in fester Reihenfolge. Schlüssel = Ordnername ohne Umlaute, klein, nur Buchstaben/Ziffern.
$BEREICHE = [
  'logo' => 'Logo',
  'markenhandbuch' => 'Markenhandbuch',
  'geschaeftsausstattung' => 'Geschäftsausstattung',
  'briefpapier' => 'Briefpapier',
  'visitenkarten' => 'Visitenkarten',
  'broschueren' => 'Broschüren',
  'flyer' => 'Flyer',
  'plakate' => 'Plakate',
  'anzeigen' => 'Anzeigen',
  'praesentationen' => 'Präsentationen',
  'verpackung' => 'Verpackung',
  'speisekarten' => 'Speisekarten',
  'tischkarten' => 'Tischkarten',
  'leitsystem' => 'Leitsystem',
  'beschilderung' => 'Beschilderung',
  'fahrzeugbeschriftung' => 'Fahrzeugbeschriftung',
  'messestand' => 'Messestand',
  'website' => 'Website',
  'onlineshop' => 'Online-Shop',
  'socialmedia' => 'Social Media',
  'onlinewerbung' => 'Online-Werbung',
  'fernsehspot' => 'Fernsehspot',
  'video' => 'Video',
  'fotografie' => 'Fotografie',
];

// Frühere oder andere Namen für denselben Bereich
$ALIAS = ['corporatedesign' => 'markenhandbuch', 'styleguide' => 'markenhandbuch', 'cdmanual' => 'markenhandbuch', 'gestaltungsrichtlinien' => 'markenhandbuch'];

$QUELLEN = ['pdf','ppt','pptx','odp','jpg','jpeg','png','webp','gif','tif','tiff','mp4','mov','m4v','avi','mkv','wmv','mpg','mpeg'];
$DIREKT = ['jpg','jpeg','png','webp','gif'];

if (empty($_GET['neu']) && is_file($CACHE_FILE) && (time() - filemtime($CACHE_FILE)) < $CACHE_SEC) {
  readfile($CACHE_FILE);
  exit;
}

function schluessel($s) {
  $s = mb_strtolower($s, 'UTF-8');
  $s = strtr($s, ['ä' => 'ae', 'ö' => 'oe', 'ü' => 'ue', 'ß' => 'ss']);
  return preg_replace('/[^a-z0-9]/', '', $s);
}
function utf8($s) {
  return mb_check_encoding($s, 'UTF-8') ? $s : mb_convert_encoding($s, 'UTF-8', 'Windows-1252');
}
function titel($name, $istDatei = true) {
  $s = utf8($name);
  if ($istDatei) $s = preg_replace('/\.[A-Za-z0-9]{2,5}$/', '', $s);
  $s = preg_replace('/^\d+[\s_\-.]+/', '', $s);                 // Reihenfolge-Nummer vorn
  $s = preg_replace('/_(s[\d,\-]+|alle)$/i', '', $s);            // Seitenauswahl hinten
  $s = preg_replace('/[_\-]+/', ' ', $s);
  return trim(preg_replace('/\s+/', ' ', $s));
}
function ordnungswert($name) {
  return preg_match('/^(\d+)/', $name, $m) ? (int)$m[1] : 100000;
}
function url($rel) {
  return 'referenzen/' . implode('/', array_map('rawurlencode', explode('/', $rel)));
}
function sichtbar($name) {
  return $name !== '' && $name[0] !== '.' && $name[0] !== '_';
}
function eintraege($dir) {
  $a = @scandir($dir);
  if (!$a) return [];
  $a = array_values(array_filter($a, 'sichtbar'));
  usort($a, function ($x, $y) {
    $o = ordnungswert($x) <=> ordnungswert($y);
    return $o ?: strnatcasecmp($x, $y);
  });
  return $a;
}
function eintraege_alle($dir) {
  $a = @scandir($dir);
  if (!$a) return [];
  $a = array_values(array_filter($a, function ($n) { return $n !== '' && $n[0] !== '.'; }));
  usort($a, function ($x, $y) { return (ordnungswert($x) <=> ordnungswert($y)) ?: strnatcasecmp($x, $y); });
  return $a;
}
function info($datei) {
  $r = [];
  if (!is_file($datei)) return $r;
  foreach (preg_split('/\r\n|\r|\n/', utf8((string)file_get_contents($datei))) as $z) {
    if (preg_match('/^\s*([A-Za-zÄÖÜäöü]+)\s*:\s*(.*?)\s*$/u', $z, $m)) $r[schluessel($m[1])] = $m[2];
  }
  return $r;
}

// Eine Quelldatei in eine Liste von Vorschau-Elementen übersetzen.
function elemente($absDir, $relDir, $datei) {
  global $QUELLEN, $DIREKT;
  $ext = strtolower(pathinfo($datei, PATHINFO_EXTENSION));
  if (!in_array($ext, $QUELLEN, true)) return null;
  $metaDatei = "$absDir/_vorschau/$datei/meta.json";
  $vrel = "$relDir/_vorschau/$datei";
  if (is_file($metaDatei)) {
    $roh = (string)file_get_contents($metaDatei);
    $m = json_decode($roh, true);
    if (!is_array($m)) $m = json_decode(preg_replace('/\\\\ud[89a-f][0-9a-f]{2}/i', '', $roh), true);  // alte Einträge mit kaputten Zeichen
    if (is_array($m) && !empty($m['items'])) {
      $out = ['typ' => $m['type'] ?? 'bild', 'items' => []];
      foreach ($m['items'] as $it) {
        $out['items'][] = ['t' => url("$vrel/" . $it['thumb']), 'f' => url("$vrel/" . $it['full']), 'w' => $it['w'] ?? null, 'h' => $it['h'] ?? null];
      }
      if (!empty($m['video'])) $out['video'] = url("$vrel/" . $m['video']);
      return $out;
    }
  }
  if (in_array($ext, $DIREKT, true)) {
    $u = url("$relDir/$datei");
    $g = @getimagesize("$absDir/$datei");
    return ['typ' => 'bild', 'items' => [['t' => $u, 'f' => $u, 'w' => $g[0] ?? null, 'h' => $g[1] ?? null]]];
  }
  return null; // Vorschau noch nicht erzeugt
}

$kunden = [];
foreach (eintraege($BASE) as $kOrdner) {
  $kAbs = "$BASE/$kOrdner";
  if (!is_dir($kAbs)) continue;
  $inf = info("$kAbs/info.txt");
  $bereiche = [];
  foreach (eintraege($kAbs) as $bOrdner) {
    $bAbs = "$kAbs/$bOrdner";
    if (!is_dir($bAbs)) continue;
    $arbeiten = [];
    foreach (eintraege($bAbs) as $e) {
      $eAbs = "$bAbs/$e";
      $rel = "$kOrdner/$bOrdner";
      if (is_dir($eAbs)) {                       // Serie: alle Dateien im Unterordner = eine Arbeit
        $items = []; $typ = 'bild'; $video = null;
        foreach (eintraege($eAbs) as $d) {
          if (!is_file("$eAbs/$d")) continue;
          $el = elemente($eAbs, "$rel/$e", $d);
          if (!$el) continue;
          $items = array_merge($items, $el['items']);
          if ($el['typ'] === 'video' && !$video) { $video = $el['video'] ?? null; $typ = 'video'; }
        }
        if ($items) { $a = ['titel' => titel($e, false), 'typ' => count($items) > 1 ? 'serie' : $typ, 'items' => $items]; if ($video && count($items) === 1) $a['video'] = $video; $arbeiten[] = $a; }
      } elseif (is_file($eAbs)) {
        $el = elemente($bAbs, $rel, $e);
        if ($el) $arbeiten[] = array_merge(['titel' => titel($e)], $el);
      }
    }
    if (!$arbeiten) continue;
    $k = schluessel(titel($bOrdner, false));
    if (isset($ALIAS[$k])) $k = $ALIAS[$k];
    if (isset($bereiche[$k])) $bereiche[$k]['arbeiten'] = array_merge($bereiche[$k]['arbeiten'], $arbeiten);  // "Broschüren" und "Broschueren" zusammenführen
    else $bereiche[$k] = ['key' => $k, 'name' => $BEREICHE[$k] ?? titel($bOrdner, false), 'arbeiten' => $arbeiten];
  }
  if (!$bereiche) continue;
  $bereiche = array_values($bereiche);
  // Eigene Kachelbilder für die Projektkachel: Ordner _kachel im Kundenordner (1 oder 4 Bilder)
  $kachel = [];
  if (is_dir("$kAbs/_kachel")) {
    foreach (eintraege("$kAbs/_kachel") as $d) {
      if (!is_file("$kAbs/_kachel/$d")) continue;
      $el = elemente("$kAbs/_kachel", "$kOrdner/_kachel", $d);
      if ($el) foreach ($el['items'] as $it) $kachel[] = $it['t'];
    }
  }
  // Gesamtleistungen aus info.txt ("Leistung: Corporate Design, Website-Relaunch"),
  // Corporate Design automatisch bei Logo plus mindestens drei weiteren Bereichen
  $leistungen = [];
  foreach (preg_split('/\s*[,;]\s*/', (string)($inf['leistung'] ?? ($inf['leistungen'] ?? ''))) as $l) if (trim($l) !== '') $leistungen[] = trim($l);
  $hatLogo = false; foreach ($bereiche as $b) if ($b['key'] === 'logo') $hatLogo = true;
  $istCD = false; foreach ($leistungen as $l) if (schluessel($l) === 'corporatedesign') $istCD = true;
  if (!$istCD && $hatLogo && count($bereiche) >= 4 && !isset($inf['leistung'])) array_unshift($leistungen, 'Corporate Design');
  $kunden[] = [
    'id' => schluessel(titel($kOrdner, false)),
    'name' => ($inf['name'] ?? '') ?: titel($kOrdner, false),
    'branche' => $inf['branche'] ?? '',
    'ort' => $inf['ort'] ?? '',
    'zeitraum' => $inf['zeitraum'] ?? ($inf['jahre'] ?? ''),
    'text' => $inf['text'] ?? '',
    'leistungen' => $leistungen,
    'logoreihe' => in_array(schluessel($inf['logoreihe'] ?? ''), ['ja', 'yes', '1', 'x'], true),
    'reihenfolge' => is_numeric($inf['reihenfolge'] ?? null) ? (int)$inf['reihenfolge'] : null,
    'kachel' => array_slice($kachel, 0, 8),
    'bereiche' => $bereiche,
  ];
}

// Bereiche in fester Reihenfolge, unbekannte alphabetisch dahinter
$reihe = array_flip(array_keys($BEREICHE));
$zaehl = [];
foreach ($kunden as &$k) {
  usort($k['bereiche'], function ($a, $b) use ($reihe) {
    $x = $reihe[$a['key']] ?? 1000; $y = $reihe[$b['key']] ?? 1000;
    return ($x <=> $y) ?: strnatcasecmp($a['name'], $b['name']);
  });
  foreach ($k['bereiche'] as $b) {
    if (!isset($zaehl[$b['key']])) $zaehl[$b['key']] = ['key' => $b['key'], 'name' => $b['name'], 'anzahl' => 0];
    $zaehl[$b['key']]['anzahl'] += count($b['arbeiten']);
  }
}
unset($k);
$kategorien = array_values($zaehl);
usort($kategorien, function ($a, $b) use ($reihe) {
  $x = $reihe[$a['key']] ?? 1000; $y = $reihe[$b['key']] ?? 1000;
  return ($x <=> $y) ?: strnatcasecmp($a['name'], $b['name']);
});
// Gleiche Leistung in unterschiedlicher Schreibweise vereinheitlichen (erste Schreibweise gilt)
$lname = [];
foreach ($kunden as &$k) {
  $neu = [];
  foreach ($k['leistungen'] as $l) { $s = schluessel($l); if (!isset($lname[$s])) $lname[$s] = $l; if (!in_array($lname[$s], $neu, true)) $neu[] = $lname[$s]; }
  $k['leistungen'] = $neu;
}
unset($k);
// Sortierung: Reihenfolge aus info.txt, dann Corporate Design, dann Anzahl der Bereiche
usort($kunden, function ($a, $b) {
  $ra = $a['reihenfolge'] ?? PHP_INT_MAX; $rb = $b['reihenfolge'] ?? PHP_INT_MAX;
  if ($ra !== $rb) return $ra <=> $rb;
  $ca = in_array('corporatedesign', array_map('schluessel', $a['leistungen']), true) ? 0 : 1;
  $cb = in_array('corporatedesign', array_map('schluessel', $b['leistungen']), true) ? 0 : 1;
  return ($ca <=> $cb) ?: (count($b['bereiche']) <=> count($a['bereiche'])) ?: strnatcasecmp($a['name'], $b['name']);
});

// Kundenlogos für die Logoreihe: referenzen/_kundenlogos/<Name>.svg|png|jpg
$logos = [];
foreach (eintraege_alle("$BASE/_kundenlogos") as $d) {
  $ext = strtolower(pathinfo($d, PATHINFO_EXTENSION));
  if (!in_array($ext, ['svg', 'png', 'jpg', 'jpeg', 'webp'], true)) continue;
  $logos[] = ['name' => titel($d), 'url' => url("_kundenlogos/$d")];
}

$json = json_encode(['stand' => date('c'), 'kategorien' => $kategorien, 'kunden' => $kunden, 'logos' => $logos], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
if (!is_dir($CACHE_DIR)) @mkdir($CACHE_DIR, 0755);
if (is_dir($CACHE_DIR)) @file_put_contents($CACHE_FILE, $json, LOCK_EX);
echo $json;
