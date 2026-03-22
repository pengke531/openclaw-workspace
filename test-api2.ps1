$headers = @{
    'Authorization' = 'local-dev-no-auth-needed'
}
try {
    $response = Invoke-WebRequest -Uri 'http://127.0.0.1:3100/api/agents/me' -UseBasicParsing -Headers $headers -ErrorAction Stop
    Write-Output $response.Content
} catch {
    Write-Output "Error: $_"
    Write-Output $_.Exception.Response.StatusCode
}
