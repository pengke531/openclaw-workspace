$body = '{"status":"done","comment":"No description found in issue"}'
$r = Invoke-WebRequest -Uri 'http://127.0.0.1:3100/api/issues/7b1a421f-f5db-497b-be73-68a5e6dd2699' -Method PATCH -Headers @{'Authorization'='local-dev-no-auth-needed'; 'Content-Type'='application/json'} -Body $body -UseBasicParsing
Write-Host "Status:" $r.StatusCode
Write-Host "Content:" $r.Content
