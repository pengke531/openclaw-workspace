$endpoints = @(
    "/api",
    "/api/v1",
    "/api/v1/agents/me",
    "/GEN/api/agents/me",
    "/api/GEN/agents/me"
)

foreach ($endpoint in $endpoints) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:3100$endpoint" -UseBasicParsing -ErrorAction Stop
        Write-Output "$endpoint : $($response.StatusCode) - $($response.Content.Substring(0, [Math]::Min(100, $response.Content.Length)))"
    } catch {
        Write-Output "$endpoint : $($_.Exception.Response.StatusCode)"
    }
}
