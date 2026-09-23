param(
    [string]$Package = "com.gsr.gs25",
    [string]$StockMenu = "420 2170",
    [int]$DelaySeconds = 2
)

$ErrorActionPreference = "Stop"

Write-Host "[1/5] Checking ADB"
adb devices
if ($LASTEXITCODE -ne 0) {
    throw "adb is not installed or is not on PATH."
}

$devices = adb devices
$authorized = $devices | Select-String -Pattern "\sdevice$"
if (-not $authorized) {
    throw "No authorized Android device/emulator found. Run 'adb devices' and approve USB debugging on the device."
}

Write-Host "[2/5] Launching $Package"
adb shell monkey -p $Package -c android.intent.category.LAUNCHER 1
Start-Sleep -Seconds $DelaySeconds

Write-Host "[3/5] Device resolution"
adb shell wm size

Write-Host "[4/5] Opening inventory menu"
$xy = $StockMenu -split "\s+"
if ($xy.Count -ne 2) {
    throw "StockMenu must look like 420 2170"
}
adb shell input tap $xy[0] $xy[1]
Start-Sleep -Seconds $DelaySeconds

Write-Host "[5/5] Dumping current UI hierarchy"
New-Item -ItemType Directory -Force data\android | Out-Null
adb shell uiautomator dump /sdcard/window.xml
adb pull /sdcard/window.xml data\android\window.xml

Write-Host ""
Write-Host "Saved: data\android\window.xml"
Write-Host "Next: inspect the UI hierarchy and calibrate product/list coordinates."
