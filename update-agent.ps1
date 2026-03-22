$sushiContent = Get-Content "C:\Users\itach\.openclaw\agents\sushi\AGENT.md" -Raw
$body = @{
    capabilities = $sushiContent
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://127.0.0.1:3100/api/agents/a2f55acd-a294-4f31-a613-a8512cba4c22" -Method PATCH -Body $body -ContentType "application/json"
