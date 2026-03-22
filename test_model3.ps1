$baseUrlHttp = "http://www.claudecodeserver.top/api"
$baseUrlHttps = "https://www.claudecodeserver.top/api"
$key = "sk_4f99b0f81b70afdb62137239037f7e562e77fbda002d4d3ae3881615aef71d25"

$headers = @{
    "x-api-key" = $key
    "anthropic-version" = "2023-06-01"
    "Content-Type" = "application/json"
    "User-Agent" = "claude-code/2.1.80"
    "Accept" = "application/json"
}

# Test GET /v1/models
Write-Host "=== GET /v1/models (HTTP) ==="
try {
    $r = [Microsoft.PowerShell.Commands.WebRequestExtensions]::InvokeWebRequest(
        (New-Object System.Net.WebClient),
        [System.Uri]"$baseUrlHttp/v1/models",
        "GET",
        $null,
        $headers,
        $null,
        $null,
        @(),
        $null
    )
} catch {
    Write-Host "Status: $($_.Exception.Response.StatusCode.value__)"
}

Write-Host ""
Write-Host "=== POST /v1/messages with correct body ==="
$body = '{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 10,
  "messages": [{"role": "user", "content": "hi"}]
}'

try {
    $r = Invoke-WebRequest -Uri "$baseUrlHttp/v1/messages" `
        -Headers $headers `
        -Method Post `
        -Body $body `
        -TimeoutSec 10
    Write-Host "OK: $($r.StatusCode)"
} catch {
    Write-Host "FAIL: $($_.Exception.Response.StatusCode.value__)"
}
