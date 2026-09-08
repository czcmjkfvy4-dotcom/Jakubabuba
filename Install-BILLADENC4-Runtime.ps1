Add-Type -AssemblyName System.Windows.Forms
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$required = @("VCMI_lib.dll", "VCMI_server.exe", "VCMI_client.exe")
foreach ($file in $required) {
    if (-not (Test-Path -LiteralPath (Join-Path $scriptDir $file))) {
        [System.Windows.Forms.MessageBox]::Show("Missing runtime file: $file", "BILLADENC4 Runtime")
        exit 1
    }
}

$runningVcmi = Get-Process -Name "VCMI_client", "VCMI_server", "VCMI_launcher" -ErrorAction SilentlyContinue
if ($runningVcmi) {
    [System.Windows.Forms.MessageBox]::Show("Close VCMI and VCMI Launcher before installing the BILLADENC4 runtime, then run this installer again. No files were changed.", "BILLADENC4 Runtime")
    exit 1
}

function Test-VcmiFolder([string]$Path) {
    return $Path -and (
        (Test-Path -LiteralPath (Join-Path $Path "VCMI_client.exe")) -or
        (Test-Path -LiteralPath (Join-Path $Path "VCMI_launcher.exe")) -or
        (Test-Path -LiteralPath (Join-Path $Path "VCMI_server.exe"))
    )
}

$candidates = @(
    (Join-Path $env:ProgramFiles "VCMI"),
    $(if (${env:ProgramFiles(x86)}) { Join-Path ${env:ProgramFiles(x86)} "VCMI" })
) | Where-Object { $_ }

$target = $candidates | Where-Object { Test-VcmiFolder $_ } | Select-Object -First 1
if (-not $target) {
    $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $dialog.Description = "Choose your VCMI 1.7.5 program folder. It should contain VCMI_client.exe or VCMI_launcher.exe."
    $dialog.ShowNewFolderButton = $false

    if ($dialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) {
        Write-Host "Installation cancelled."
        exit 0
    }
    $target = $dialog.SelectedPath
}

if (-not (Test-VcmiFolder $target)) {
    [System.Windows.Forms.MessageBox]::Show("This does not look like a VCMI program folder. No files were changed.", "BILLADENC4 Runtime")
    exit 1
}

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backup = Join-Path $target "BILLADENC4-backup-$stamp"
New-Item -ItemType Directory -Force -Path $backup | Out-Null

foreach ($file in $required) {
    $targetFile = Join-Path $target $file
    if (Test-Path -LiteralPath $targetFile) {
        Copy-Item -LiteralPath $targetFile -Destination (Join-Path $backup $file) -Force
    }
    Copy-Item -LiteralPath (Join-Path $scriptDir $file) -Destination $targetFile -Force
}

[System.Windows.Forms.MessageBox]::Show("BILLADENC4 runtime installed. Level 8 recruitment previews and all engine rules are enabled. Backup created in: $backup", "BILLADENC4 Runtime")
Write-Host "Installed BILLADENC4 runtime to: $target"
Write-Host "Backup: $backup"
