## Testing the Live API Endpoint

The service is deployed and live at the following URL:
**`https://bitspeed-f5yp.onrender.com`**


The following commands use `Invoke-WebRequest` for Windows PowerShell.

```powershell
# Set your live URL once
$liveUrl = "https://bitspeed-f5yp.onrender.com"

# Test Case 0: Health Check
Invoke-WebRequest -Uri $liveUrl

# Test Case 1: Create First Primary
Invoke-WebRequest -Uri "$liveUrl/identify" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"email": "george@hillvalley.edu", "phoneNumber": "919191"}'

# Test Case 2: Create Second Primary
Invoke-WebRequest -Uri "$liveUrl/identify" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"email": "biffsucks@hillvalley.edu", "phoneNumber": "717171"}'

# Test Case 3: Add Secondary
Invoke-WebRequest -Uri "$liveUrl/identify" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"email": "george@hillvalley.edu", "phoneNumber": "555-NEW-PHONE"}'

# Test Case 4: Merge Identities
Invoke-WebRequest -Uri "$liveUrl/identify" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"email": "george@hillvalley.edu", "phoneNumber": "717171"}'

# Test Case 5: Confirm Merge
Invoke-WebRequest -Uri "$liveUrl/identify" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"email": "biffsucks@hillvalley.edu"}'
