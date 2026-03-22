# Test API connection with different auth methods
$baseUrl = "http://www.claudecodeserver.top/api"
$key = "sk_4f99b0f81b70afdb62137239037f7e562e77fbda002d4d3ae3881615aef71d25"

$headers = @{
    "x-api-key" = $key
    "User-Agent" = "claude-code/2.1.80"
}

try {
    Write-Host "Testing with x-api-key header..."
    $r = Invoke-WebRequest -Uri "$baseUrl/v1/models" -Headers $headers -TimeoutSec 10
    Write-Host "Status: $($r.StatusCode)"
    Write-Host $r.Content
} catch {
    Write-Host "x-api-key error: $($_.Exception.Response.StatusCode.value__)"
    Write-Host $_.Exception.Message
}

Write-Host ""
Write-Host "Testing with Bearer token..."
$headers2 = @{
    "Authorization" = "Bearer $key"
    "User-Agent" = "claude-code/2.1.80"
}

try {
    $r2 = Invoke-WebRequest -Uri "$baseUrl/v1/models" -Headers $headers2 -TimeoutSec 10
    Write-Host "Status: $($r2.StatusCode)"
    Write-Host $r2.Content
} catch {
    Write-Host "Bearer error: $($_.Exception.Response.StatusCode.value__)"
}

Write-Host ""
Write-Host "Testing with sk-ant- format..."
$headers3 = @{
    "x-api-key" = "sk-ant-api03-$key"
    "User-Agent" = "claude-code/2.1.80"
}

try {
    $r3 = Invoke-WebRequest -Uri "$baseUrl/v1/models" -Headers $headers3 -TimeoutSec 10
    Write-Host "Status: $($r3.StatusCode)"
    Write-Host $r3.Content
} catch {
    Write-Host "sk-ant format error: $($_.Exception.Response.StatusCode.value__)"
}
