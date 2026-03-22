$headers = @{
    'Authorization' = 'local-dev-no-auth-needed'
    'Content-Type' = 'application/json'
    'X-Paperclip-Run-Id' = '21ab18bd-c5cb-4718-90c7-057000ab2a18'
}
$body = '{"agentId":"22b2f285-56c1-4181-a189-7e95771ca2bb","expectedStatuses":["todo","backlog","blocked"]}'
$response = Invoke-WebRequest -Uri 'http://127.0.0.1:3100/api/issues/02b1973d-13f9-47c2-82ff-e0ec26a3acf1/checkout' -UseBasicParsing -Headers $headers -Method Post -Body $body
Write-Host "Status:" $response.StatusCode
$response.Content | Out-File -FilePath "C:\Users\itach\.openclaw\workspace\checkout2.txt" -Encoding utf8
