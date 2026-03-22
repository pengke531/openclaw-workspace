$env:ANTHROPIC_BASE_URL = "http://www.claudecodeserver.top/api"
$env:ANTHROPIC_AUTH_TOKEN = "sk_4f99b0f81b70afdb62137239037f7e562e77fbda002d4d3ae3881615aef71d25"
Write-Host "Testing direct API..."
$body = @{
    model = "claude-3-5-sonnet-20241022"
    max_tokens = 100
    messages = @(@{role="user"; content="Say hello"})
} | ConvertTo-Json

$r = Invoke-WebRequest -Uri "http://www.claudecodeserver.top/api/v1/messages" `
    -Headers @{
        "x-api-key" = $env:ANTHROPIC_AUTH_TOKEN
        "anthropic-version" = "2023-06-01"
        "Content-Type" = "application/json"
    } `
    -Method Post `
    -Body $body `
    -TimeoutSec 15

Write-Host "Status: $($r.StatusCode)"
Write-Host $r.Content
