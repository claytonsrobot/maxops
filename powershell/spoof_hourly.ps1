# Define sample data
$data = @{
    "timestamp" = "2025-03-05T13:00:00"
    "flow_rate" = 120.5
    "cod" = 38.1
    "water_quality" = "good"
}

# Send POST request to the FastAPI endpoint
$response = Invoke-RestMethod -Uri "http://localhost:8000/submit-hourly" -Method POST -Body $data -ContentType "application/x-www-form-urlencoded"

# Output response from server
Write-Host "Server response: $($response | ConvertTo-Json -Depth 10)"
