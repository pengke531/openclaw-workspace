$headers = @{
    'Authorization' = 'Bearer local-dev-no-auth-needed'
    'Content-Type' = 'application/json'
}

$response = Invoke-RestMethod -Uri 'http://127.0.0.1:3100/api/agents/me' -Headers $headers -Method Get
$response | ConvertTo-Json -Depth 10
