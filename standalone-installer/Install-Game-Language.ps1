param(
    [Parameter(Mandatory=$true)][ValidateSet('polish','english','german','chinese','japanese','russian','spanish','french')][string]$Language,
    [Parameter(Mandatory=$true)][string]$Runtime,
    [string]$Cache = "$env:LOCALAPPDATA\Dragon Citadel\LanguagePackages"
)
$ErrorActionPreference = 'Stop'
$env:PSModulePath = (Join-Path $PSHOME 'Modules') + ';' + $env:PSModulePath
$catalog = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'game-language-packages.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$package = $catalog.PSObject.Properties[$Language].Value
$target = Join-Path $Runtime ('Mods\' + $package.id)
$stamp = Join-Path $target '.dragon-citadel-package.sha256'
if ((Test-Path -LiteralPath $stamp) -and ((Get-Content -LiteralPath $stamp -Raw).Trim() -eq $package.sha256) -and (Test-Path -LiteralPath (Join-Path $target 'mod.json'))) { return }
if (Test-Path -LiteralPath $target) { throw "Existing language package needs verification; preserved at $target" }
New-Item -ItemType Directory -Force -Path $Cache | Out-Null
$archive = Join-Path $Cache ($package.id + '-' + $package.sha256 + '.zip')
if (-not (Test-Path -LiteralPath $archive)) {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $partial = $archive + '.' + [Guid]::NewGuid().ToString('N') + '.partial'
    Invoke-WebRequest -UseBasicParsing -Uri $package.source -OutFile $partial
    if ((Get-FileHash -LiteralPath $partial -Algorithm SHA256).Hash.ToLowerInvariant() -ne $package.sha256) { throw 'Downloaded language archive checksum mismatch.' }
    Move-Item -LiteralPath $partial -Destination $archive
}
if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $package.sha256) { throw 'Cached language archive checksum mismatch.' }
$stage = Join-Path $Cache ('unpack-' + [Guid]::NewGuid().ToString('N'))
Expand-Archive -LiteralPath $archive -DestinationPath $stage
$roots = @(Get-ChildItem -LiteralPath $stage -Directory | Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'mod.json') })
if ($roots.Count -ne 1) { throw 'Unexpected language package layout.' }
$metadata = Get-Content -LiteralPath (Join-Path $roots[0].FullName 'mod.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($metadata.language -ne $Language -or $metadata.modType -ne 'Translation') { throw 'Unexpected language package metadata.' }
New-Item -ItemType Directory -Force -Path (Join-Path $Runtime 'Mods') | Out-Null
Copy-Item -LiteralPath $roots[0].FullName -Destination $target -Recurse
[IO.File]::WriteAllText($stamp, $package.sha256)
