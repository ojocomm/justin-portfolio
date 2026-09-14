<?php
// Contactformulier justinnorman.nl — mailt naar info@justinnorman.nl.
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

$TO   = 'info@justinnorman.nl';
$FROM = 'noreply@justinnorman.nl';   // afzender op eigen domein voor betrouwbare aflevering

function out(int $code, bool $ok, string $msg): void {
    http_response_code($code);
    echo json_encode(['ok' => $ok, 'message' => $msg], JSON_UNESCAPED_UNICODE);
    exit;
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') out(405, false, 'Alleen POST.');

// Alleen vanaf de eigen site
$origin = $_SERVER['HTTP_ORIGIN'] ?? $_SERVER['HTTP_REFERER'] ?? '';
if ($origin !== '' && !preg_match('~^https?://(www\.)?justinnorman\.nl(/|$)~', $origin)) out(403, false, 'Ongeldige herkomst.');

$f = fn(string $k, int $max) => trim(mb_substr((string)($_POST[$k] ?? ''), 0, $max));
$fname = $f('fname', 80); $lname = $f('lname', 80); $email = $f('email', 200);
$phone = $f('phone', 40);  $msg   = $f('message', 4000);

// Spam: honeypot ingevuld of formulier binnen 3 seconden verstuurd
if ($f('website', 100) !== '') out(200, true, 'Bedankt, je bericht is verstuurd.');
$ts = (int)($_POST['ts'] ?? 0);
if ($ts <= 0 || time() - $ts < 3) out(200, true, 'Bedankt, je bericht is verstuurd.');

if ($fname === '' || $lname === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) out(422, false, 'Vul de verplichte velden in (naam en een geldig e-mailadres).');
if (preg_match('/[\r\n]/', $fname . $lname . $email . $phone)) out(422, false, 'Ongeldige invoer.');

$name = "$fname $lname";
$subject = 'Contact via justinnorman.nl - ' . $name;
$body = "Naam: $name\nE-mail: $email\nTelefoon: " . ($phone !== '' ? $phone : '-') .
        "\n\nBericht:\n" . ($msg !== '' ? $msg : '-') .
        "\n\n--\nVerstuurd via het contactformulier op " . date('d-m-Y H:i') . ' vanaf IP ' . ($_SERVER['REMOTE_ADDR'] ?? '?');

$encName = '=?UTF-8?B?' . base64_encode($name) . '?=';
$headers = [
    'From: =?UTF-8?B?' . base64_encode('Contactformulier justinnorman.nl') . "?= <$FROM>",
    "Reply-To: $encName <$email>",
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: justinnorman.nl-contact',
];
$sent = @mail($TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers), "-f$FROM");
if (!$sent) out(500, false, 'Versturen is niet gelukt. Mail direct naar info@justinnorman.nl.');
out(200, true, 'Bedankt, je bericht is verstuurd. Ik reageer zo snel mogelijk.');
