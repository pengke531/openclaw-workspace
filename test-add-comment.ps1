$headers = @{
    'Authorization' = 'local-dev-no-auth-needed'
    'Content-Type' = 'application/json'
    'X-Paperclip-Run-Id' = 'dc9224f1-a8b3-412d-b13e-85996f595b1f'
}
$body = '{"body":"Agent状态检查完成:\n\n| Agent | 状态 | 最后心跳 |\n|-------|------|----------|\n| CEO-嬴政 | running | 06:56:48 |\n| 文案-苏轼 | idle | 06:52:57 |\n| 设计-唐寅 | idle | 03:57:15 |\n| 技术-墨子 | idle | 03:56:58 |\n| 客服-西施 | idle | 03:56:51 |\n| 产品-孔明 | idle | 03:57:05 |\n\n所有Agent状态正常。idle状态表示等待唤醒（wake-on-demand），running表示当前正在执行任务。"}'
$response = Invoke-WebRequest -Uri 'http://127.0.0.1:3100/api/issues/02b1973d-13f9-47c2-82ff-e0ec26a3acf1/comments' -UseBasicParsing -Headers $headers -Method Post -Body $body
Write-Host "Status:" $response.StatusCode
$response.Content | Out-File -FilePath "C:\Users\itach\.openclaw\workspace\comment_output.txt" -Encoding utf8
