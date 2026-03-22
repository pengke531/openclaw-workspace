$headers = @{
    "Authorization" = "Bearer test-token"
    "Content-Type" = "application/json"
}
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:3100/api/agents/me" -Headers $headers -Method Get
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
