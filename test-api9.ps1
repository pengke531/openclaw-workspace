$headers = @{
    'Authorization' = 'local-dev-no-auth-needed'
    'Content-Type' = 'application/json'
}
$response = Invoke-WebRequest -Uri 'http://127.0.0.1:3100/api/agents/me' -UseBasicParsing -Headers $headers -Method Get
Write-Host $response.Content
