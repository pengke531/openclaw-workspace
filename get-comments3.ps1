$headers = @{
    'Authorization' = 'local-dev-no-auth-needed'
    'Content-Type' = 'application/json'
}
$response = Invoke-WebRequest -Uri 'http://127.0.0.1:3100/api/issues/02b1973d-13f9-47c2-82ff-e0ec26a3acf1/comments' -UseBasicParsing -Headers $headers -Method Get
$response.Content | Out-File -FilePath "C:\Users\itach\.openclaw\workspace\comments3.txt" -Encoding utf8
Write-Host "Status:" $response.StatusCode
