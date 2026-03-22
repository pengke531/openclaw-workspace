try {
    $response = Invoke-WebRequest -Uri 'http://127.0.0.1:3100/api/' -UseBasicParsing -ErrorAction Stop
    Write-Output $response.Content
} catch {
    Write-Output $_.Exception.Message
}
