$headers = @{
    'Authorization' = 'Bearer local-dev-no-auth-needed'
}
$response = Invoke-WebRequest -Uri 'http://127.0.0.1:3100/GEN/api/agents/me' -UseBasicParsing -Headers $headers -ErrorAction Stop
Write-Output $response.Content
