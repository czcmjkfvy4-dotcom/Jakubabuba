param(
    [string]$VcmiSource = "C:\Program Files\VCMI",
    [string]$IsccPath = "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
    [string]$VcmiSourceCode = "C:\Users\GRACOMM\Documents\Codex\2026-06-16\ustaw-karte-graficzna-nvidia-rtx-jako\vcmi-source-1.7.5-billaden",
    [string]$MapPackSource = "C:\Users\GRACOMM\Documents\praca\vcmi-map-pack-downloads\chinese-maps-collection-extracted\chinese-maps-collection-main\chinese-maps-collection"
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$modRoot = Split-Path -Parent $here
$staging = Join-Path $here "staging"
$engine = Join-Path $staging "engine"

function Reset-LocalDirectory([string]$Path) {
    $full = [System.IO.Path]::GetFullPath($Path)
    $allowed = [System.IO.Path]::GetFullPath($here) + [System.IO.Path]::DirectorySeparatorChar
    if (-not $full.StartsWith($allowed, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to reset directory outside installer workspace: $full"
    }
    if ([System.IO.Directory]::Exists($full)) {
        Get-ChildItem -LiteralPath $full -Recurse -Force | ForEach-Object {
            $_.Attributes = $_.Attributes -band (-bnot [System.IO.FileAttributes]::ReadOnly)
        }
        [System.IO.Directory]::Delete($full, $true)
    }
    [System.IO.Directory]::CreateDirectory($full) | Out-Null
}

function Invoke-Robocopy([string]$Source, [string]$Destination, [string[]]$ExtraArguments = @()) {
    $arguments = @($Source, $Destination, "/E", "/NFL", "/NDL", "/NJH", "/NJS", "/NP") + $ExtraArguments
    & robocopy.exe @arguments | Out-Null
    if ($LASTEXITCODE -ge 8) {
        throw "Robocopy failed with exit code $LASTEXITCODE while copying $Source"
    }
}

if (-not (Test-Path -LiteralPath (Join-Path $VcmiSource "VCMI_client.exe"))) {
    throw "VCMI 1.7.5 source folder not found: $VcmiSource"
}
if (-not (Test-Path -LiteralPath $IsccPath)) {
    throw "Inno Setup compiler not found: $IsccPath"
}
if (-not (Test-Path -LiteralPath (Join-Path $MapPackSource "mod.json"))) {
    throw "Bundled map pack source not found: $MapPackSource"
}

& python (Join-Path $here "prepare_assets.py")
if ($LASTEXITCODE -ne 0) {
    throw "Installer asset preparation failed."
}

Reset-LocalDirectory $staging
Invoke-Robocopy $VcmiSource $engine @("/XF", "unins000.exe", "unins000.dat")

$modsRoot = Join-Path $engine "Mods"
if (Test-Path -LiteralPath $modsRoot) {
    Get-ChildItem -LiteralPath $modsRoot -Directory | Where-Object { $_.Name -ne "vcmi" } | ForEach-Object {
        [System.IO.Directory]::Delete($_.FullName, $true)
    }
}

$modDestination = Join-Path $modsRoot "dragon-citadel"
New-Item -ItemType Directory -Path $modDestination -Force | Out-Null
Invoke-Robocopy $modRoot $modDestination @(
    "/XD", (Join-Path $modRoot ".git"), (Join-Path $modRoot "standalone-installer"), (Join-Path $modRoot "tools"),
    "/XF", "*.pyc", "VCMI_client.exe", "VCMI_lib.dll", "VCMI_server.exe",
    "INSTALL BILLADENC4 RUNTIME.CMD", "Install-BILLADENC4-Runtime.ps1"
)

$mapPackDestination = Join-Path $modsRoot "chinese-maps-collection"
New-Item -ItemType Directory -Path $mapPackDestination -Force | Out-Null
Invoke-Robocopy $MapPackSource $mapPackDestination

foreach ($runtimeFile in @("VCMI_client.exe", "VCMI_lib.dll", "VCMI_server.exe")) {
    Copy-Item -LiteralPath (Join-Path $modRoot $runtimeFile) -Destination (Join-Path $engine $runtimeFile) -Force
}

Copy-Item -LiteralPath (Join-Path $here "DragonCitadel-FirstRun.ps1") -Destination $engine -Force
Copy-Item -LiteralPath (Join-Path $here "Launch-Dragon-Citadel.ps1") -Destination $engine -Force
Copy-Item -LiteralPath (Join-Path $here "assets\dragon-citadel.ico") -Destination (Join-Path $engine "DragonCitadel.ico") -Force
Copy-Item -LiteralPath (Join-Path $here "dirs.json") -Destination (Join-Path $engine "config\dirs.json") -Force

$licenses = Join-Path $engine "licenses"
New-Item -ItemType Directory -Path $licenses -Force | Out-Null
if (Test-Path -LiteralPath (Join-Path $VcmiSourceCode "license.txt")) {
    Copy-Item -LiteralPath (Join-Path $VcmiSourceCode "license.txt") -Destination (Join-Path $licenses "VCMI-license.txt") -Force
}
if (Test-Path -LiteralPath (Join-Path $VcmiSourceCode "AUTHORS.h")) {
    Copy-Item -LiteralPath (Join-Path $VcmiSourceCode "AUTHORS.h") -Destination (Join-Path $licenses "VCMI-authors.txt") -Force
}
Copy-Item -LiteralPath (Join-Path $here "LEGAL.txt") -Destination (Join-Path $licenses "Dragon-Citadel-standalone-notice.txt") -Force

Push-Location $here
try {
    & $IsccPath (Join-Path $here "DragonCitadel.iss")
    if ($LASTEXITCODE -ne 0) {
        throw "Inno Setup compilation failed with exit code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}

$output = Join-Path $here "output\Smocza_Cytadela_Complete_Edition_1.5.7_Setup.exe"
if (-not (Test-Path -LiteralPath $output)) {
    throw "Installer output was not created: $output"
}

Get-Item -LiteralPath $output | Select-Object FullName, Length, LastWriteTime
Get-FileHash -LiteralPath $output -Algorithm SHA256
