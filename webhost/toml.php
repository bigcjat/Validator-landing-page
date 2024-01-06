<?php
// Enable CORS
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');

// You can change these values
$allowedIPAddress = '0.0.0.0'; // Replace with your validator IP address
$apiKey = 'key'; // Set your API key here, this can be anything you want
$filePath = '.well-known/xahau.toml'; // File path relitive to this PHP script. Change xahau.toml to xrp-ledger.toml if you are using the Mainnet

// Get the client's IP address
$clientIPAddress = $_SERVER['REMOTE_ADDR'];

// Check if the client's IP address matches the allowed IP address
if ($clientIPAddress !== $allowedIPAddress) {
    // If not, exit the script with an unauthorized error message
    http_response_code(401); // Set HTTP response code to 401 Unauthorized
    die('Error: Unauthorized access');
}

if (!isset($_GET['apiKey']) || $_GET['apiKey'] !== $apiKey) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

$inputData = json_decode(file_get_contents('php://input'), true);

if (!$inputData || !isset($inputData['STATUS']) || !isset($inputData['AMENDMENTS'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid input data']);
    exit;
}

function updateTomlFile($filePath, $statusData, $amendmentsData) {
    $fileContent = file_get_contents($filePath);
    $updatedContent = preg_replace(
        '/\[\[STATUS\]\].*?\[\[AMENDMENTS\]\]/s',
        "[[STATUS]]\n$statusData\n[[AMENDMENTS]]",
        $fileContent
    );
    $updatedContent = preg_replace(
        '/\[\[AMENDMENTS\]\].*?(?=\[\[|\Z)/s',
        "[[AMENDMENTS]]\n$amendmentsData",
        $updatedContent
    );
    file_put_contents($filePath, $updatedContent);
}

updateTomlFile($filePath, $inputData['STATUS'], $inputData['AMENDMENTS']);

echo json_encode(['success' => 'File updated successfully']);

