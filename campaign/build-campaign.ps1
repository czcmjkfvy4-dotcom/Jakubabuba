param(
    [string] $OutputPath
)

$ErrorActionPreference = "Stop"

$campaignRoot = $PSScriptRoot
$modRoot = Split-Path -Parent $campaignRoot
$sourceRoot = Join-Path $campaignRoot "source"
$headerPath = Join-Path $sourceRoot "header.json"
$mapsRoot = Join-Path $sourceRoot "maps"

if (-not $OutputPath) {
    $outputDir = Join-Path $modRoot "Content\Maps"
    $OutputPath = Join-Path $outputDir "Smocza_Cytadela.vcmp"
}

if (-not (Test-Path -LiteralPath $headerPath)) {
    throw "Missing campaign header: $headerPath"
}

$header = Get-Content -Raw -LiteralPath $headerPath | ConvertFrom-Json
$missing = New-Object System.Collections.Generic.List[string]
$scenarioFiles = New-Object System.Collections.Generic.List[object]

foreach ($scenario in $header.scenarios) {
    $mapPath = [string] $scenario.map
    $relativeBase = $mapPath -replace "/", "\"
    $candidates = @(
        (Join-Path $sourceRoot ($relativeBase + ".vmap")),
        (Join-Path $sourceRoot ($relativeBase + ".h3m"))
    )
    $existing = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if ($existing) {
        $extension = [System.IO.Path]::GetExtension($existing)
        $scenarioFiles.Add([pscustomobject]@{
            Source = $existing
            Relative = ($relativeBase + $extension)
        })
    } else {
        $missing.Add(($mapPath + ".vmap or .h3m"))
    }
}

if ($missing.Count -gt 0) {
    Write-Host "Campaign package was not created. Missing scenario maps:"
    foreach ($entry in $missing) {
        Write-Host (" - " + $entry)
    }
    exit 2
}

$buildRoot = Join-Path $campaignRoot "build\smocza-cytadela-vcmp"
$buildRoot = [System.IO.Path]::GetFullPath($buildRoot)
$allowedRoot = [System.IO.Path]::GetFullPath($campaignRoot) + [System.IO.Path]::DirectorySeparatorChar
if (-not $buildRoot.StartsWith($allowedRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to reset a directory outside the campaign workspace: $buildRoot"
}
if (Test-Path -LiteralPath $buildRoot) {
    Remove-Item -LiteralPath $buildRoot -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $buildRoot | Out-Null
Copy-Item -LiteralPath $headerPath -Destination (Join-Path $buildRoot "header.json") -Force

foreach ($file in $scenarioFiles) {
    $destination = Join-Path $buildRoot $file.Relative
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $destination) | Out-Null
    Copy-Item -LiteralPath $file.Source -Destination $destination -Force
}

$outputDir = Split-Path -Parent $OutputPath
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

$zipPath = [System.IO.Path]::ChangeExtension($OutputPath, ".zip")
if (Test-Path -LiteralPath $zipPath) {
    Remove-Item -LiteralPath $zipPath -Force
}
if (Test-Path -LiteralPath $OutputPath) {
    Remove-Item -LiteralPath $OutputPath -Force
}

Compress-Archive -Path (Join-Path $buildRoot "*") -DestinationPath $zipPath -Force
Move-Item -LiteralPath $zipPath -Destination $OutputPath -Force

Write-Host "Campaign package created:"
Write-Host $OutputPath
