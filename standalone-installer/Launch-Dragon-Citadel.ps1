param(
    [string]$SourcePath = "",
    [switch]$SetupOnly
)

$ErrorActionPreference = "Stop"
$installDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$setupScript = Join-Path $installDir "DragonCitadel-FirstRun.ps1"
$client = Join-Path $installDir "VCMI_client.exe"

$quotedSetupScript = '"' + $setupScript.Replace('"', '\"') + '"'
$arguments = "-NoProfile -ExecutionPolicy Bypass -File $quotedSetupScript"
if ($SourcePath) {
    $quotedSourcePath = '"' + $SourcePath.Replace('"', '\"') + '"'
    $arguments += " -SourcePath $quotedSourcePath"
}

$setup = Start-Process -FilePath "powershell.exe" -ArgumentList $arguments -WorkingDirectory $installDir -Wait -PassThru -WindowStyle Hidden
if ($setup.ExitCode -ne 0 -or $SetupOnly) {
    exit $setup.ExitCode
}

if (-not (Test-Path -LiteralPath $client)) {
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.MessageBox]::Show(
        "VCMI_client.exe is missing. Reinstall Dragon Citadel.",
        "Dragon Citadel",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    ) | Out-Null
    exit 1
}

Start-Process -FilePath $client -ArgumentList "--nointro" -WorkingDirectory $installDir
exit 0
