$headers = @{
    'Authorization' = 'local-dev-no-auth-needed'
    'Content-Type' = 'application/json'
}
# Try getting agents
$response = Invoke-WebRequest -Uri 'http://127.0.0.1:3100/api/companies/5ed280b5-c784-4b88-8c39-f344c7b88fe8/agents' -UseBasicParsing -Headers $headers -Method Get
$response.Content | Out-File -FilePath "C:\Users\itach\.openclaw\workspace\agents_output.txt" -Encoding utf8
Write-Host "Status:" $response.StatusCode
