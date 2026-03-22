$baseUrl = "http://www.claudecodeserver.top/api"
$key = "sk_4f99b0f81b70afdb62137239037f7e562e77fbda002d4d3ae3881615aef71d25"

# Test different auth methods
$tests = @(
    @{name="x-api-key"; headers=@{"x-api-key"=$key;"anthropic-version"="2023-06-01"}},
    @{name="Bearer sk_"; headers=@{"Authorization"="Bearer $key";"anthropic-version"="2023-06-01"}},
    @{name="api-key header"; headers=@{"api-key"=$key;"anthropic-version"="2023-06-01"}}
)

$body = @{
    model = "claude-3-5-sonnet-20241022"
    max_tokens = 50
    messages = @(@{role="user"; content="hi"})
} | ConvertTo-Json

foreach ($t in $tests) {
    Write-Host "=== $($t.name) ==="
    try {
        $r = Invoke-WebRequest -Uri "$baseUrl/v1/messages" `
            -Headers $t.headers `
            -Method Post `
            -Body $body `
            -TimeoutSec 10
        Write-Host "OK: $($r.StatusCode) - $($r.Content.Substring(0, [Math]::Min(200, $r.Content.Length)))"
    } catch {
        Write-Host "FAIL: $($_.Exception.Response.StatusCode.value__)"
    }
    Write-Host ""
}
