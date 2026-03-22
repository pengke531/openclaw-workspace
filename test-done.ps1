$headers = @{
    'Authorization' = 'local-dev-no-auth-needed'
    'Content-Type' = 'application/json'
    'X-Paperclip-Run-Id' = 'dc9224f1-a8b3-412d-b13e-85996f595b1f'
}
$body = '{"status":"done","comment":"Checked all 6 agents: 1 running (CEO-嬴政), 5 idle (normal for wake-on-demand). All status normal."}'
$response = Invoke-WebRequest -Uri 'http://127.0.0.1:3100/api/issues/02b1973d-13f9-47c2-82ff-e0ec26a3acf1' -UseBasicParsing -Headers $headers -Method Patch -Body $body
Write-Host "Status:" $response.StatusCode
$response.Content | Out-File -FilePath "C:\Users\itach\.openclaw\workspace\done_output.txt" -Encoding utf8
