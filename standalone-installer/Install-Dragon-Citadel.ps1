param(
    [string]$Destination = "$env:LOCALAPPDATA\Programs\Dragon Citadel Projects",
    [string]$DataSource = '',
    [ValidateSet('Keep','polish','english','german','chinese','japanese','russian','spanish','french')][string]$Language = 'Keep',
    [switch]$Fourth,
    [switch]$Graphics,
    [switch]$NoShortcut
)
$ErrorActionPreference = 'Stop'
$env:PSModulePath = (Join-Path $PSHOME 'Modules') + ';' + $env:PSModulePath
$Destination = [IO.Path]::GetFullPath($Destination)
if ($Destination.TrimEnd('\') -eq [IO.Path]::GetPathRoot($Destination).TrimEnd('\')) { throw 'Wybierz osobny katalog instalacji.' }
$payload = Join-Path $PSScriptRoot 'payload'
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'payload-manifest.json') -Raw | ConvertFrom-Json
foreach ($file in $manifest.files) {
    $path = Join-Path $payload $file.path
    $resolved = [IO.Path]::GetFullPath($path)
    if (-not $resolved.StartsWith(([IO.Path]::GetFullPath($payload) + '\'),[StringComparison]::OrdinalIgnoreCase)) { throw 'Nieprawidlowa sciezka pakietu.' }
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -ne $file.sha256) { throw "Uszkodzony plik pakietu: $($file.path)" }
}
$candidates = @($DataSource, "$env:USERPROFILE\Documents\My Games\vcmi\Data", "$env:LOCALAPPDATA\Dragon Citadel\Profile\Data") | Where-Object { $_ }
if ($DataSource) { $candidates = @($DataSource, (Join-Path $DataSource 'Data')) + $candidates }
$gameData = $null
foreach ($candidate in $candidates) {
    $missing = @('H3bitmap.lod','H3sprite.lod','H3ab_bmp.lod','H3ab_spr.lod') | Where-Object { -not (Test-Path -LiteralPath (Join-Path $candidate $_)) }
    if (-not $missing) { $gameData = $candidate; break }
}
if (-not $gameData) { throw 'Podaj -DataSource z katalogiem Data wlasnej instalacji Heroes III Complete / Shadow of Death lub VCMI. Pakiet nie zawiera danych gry.' }
$running = Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -and $_.ExecutablePath.StartsWith(($Destination + '\'),[StringComparison]::OrdinalIgnoreCase) -and $_.Name -in @('VCMI_client.exe','VCMI_server.exe','VCMI_launcher.exe') }
if ($running) { throw 'Zamknij uruchomiona gre w docelowym katalogu przed aktualizacja.' }
$backup = Join-Path $Destination ('.backups\' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
foreach ($file in $manifest.files) {
    $source = Join-Path $payload $file.path; $target = Join-Path $Destination $file.path
    if (Test-Path -LiteralPath $target) {
        if ((Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash -eq $file.sha256) { continue }
        $old = Join-Path $backup $file.path; New-Item -ItemType Directory -Path (Split-Path -Parent $old) -Force | Out-Null; Copy-Item -LiteralPath $target -Destination $old
    }
    New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
    Copy-Item -LiteralPath $source -Destination $target -Force
}
$profile = Join-Path $Destination 'Profile'
foreach ($part in @('Data','config','logs','Saves','cache','Mp3')) { New-Item -ItemType Directory -Path (Join-Path $profile $part) -Force | Out-Null }
foreach ($file in Get-ChildItem -LiteralPath $gameData -File | Where-Object { $_.Extension -in @('.lod','.snd','.vid') }) {
    $target = Join-Path (Join-Path $profile 'Data') $file.Name
    if (-not (Test-Path -LiteralPath $target)) { Copy-Item -LiteralPath $file.FullName -Destination $target }
}
$musicCandidates = @((Join-Path (Split-Path -Parent $gameData) 'Mp3'), (Join-Path (Split-Path -Parent $gameData) 'Music'))
foreach ($musicDirectory in $musicCandidates) {
    if (Test-Path -LiteralPath $musicDirectory) {
        foreach ($track in Get-ChildItem -LiteralPath $musicDirectory -Filter '*.mp3' -File) {
            $target = Join-Path (Join-Path $profile 'Mp3') $track.Name
            if (-not (Test-Path -LiteralPath $target)) { Copy-Item -LiteralPath $track.FullName -Destination $target }
        }
    }
}
function Save-Json([string]$Path, $Value) {
    $text = $Value | ConvertTo-Json -Depth 100
    $text = [regex]::Replace($text,'\\u(0026|0027|003c|003e)', {param($m) [string][char][Convert]::ToInt32($m.Groups[1].Value,16)})
    [IO.File]::WriteAllText($Path,$text,(New-Object Text.UTF8Encoding($false)))
}
Save-Json (Join-Path $Destination 'config\dirs.json') @{ userDataPath=$profile; userSavePath=(Join-Path $profile 'Saves'); userLogsPath=(Join-Path $profile 'logs'); userConfigPath=(Join-Path $profile 'config'); userCachePath=(Join-Path $profile 'cache') }
$modsPath = Join-Path $profile 'config\modSettings.json'
if (Test-Path -LiteralPath $modsPath) { $mods = Get-Content -LiteralPath $modsPath -Raw -Encoding UTF8 | ConvertFrom-Json } else { $mods = [pscustomobject]@{activePreset='Dragon Citadel - projekty';presets=[pscustomobject]@{};validatedMods=[pscustomobject]@{}} }
$wog = @{}
Get-ChildItem -LiteralPath (Join-Path $Destination 'Mods\wake-of-gods\Mods') -Directory | ForEach-Object { $wog[$_.Name.ToLowerInvariant()] = $false }
$wog['level8units'] = [bool]$Fourth
$roots = @('core','vcmi','dragon-citadel'); if ($Fourth) { $roots += 'wake-of-gods' }
$preset = @{ mods=$roots;settings=@{'dragon-citadel'=@{'endgame-rules'=$true;'fourth-upgrades'=[bool]$Fourth;'graphics-enhancement'=[bool]$Graphics;'tum'=$false;'third-upgrades'=$false;'chinese-fonts'=$true;'japanese-fonts'=$true};'wake-of-gods'=$wog} }
$mods.presets | Add-Member -Force -NotePropertyName 'Dragon Citadel - projekty' -NotePropertyValue $preset
$mods.activePreset = 'Dragon Citadel - projekty'; Save-Json $modsPath $mods
$settingsPath = Join-Path $profile 'config\settings.json'
if (-not (Test-Path -LiteralPath $settingsPath)) { Save-Json $settingsPath @{general=@{language='polish';enableOverlay=$true};mods=@{validation='full'};launcher=@{setupCompleted=$true};video=@{fullscreen=$false;resolution=@{width=800;height=600}}} }
if ($Language -ne 'Keep') {
    $gameSettings = Get-Content -LiteralPath $settingsPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if (-not $gameSettings.general) { $gameSettings | Add-Member -Force -NotePropertyName general -NotePropertyValue ([pscustomobject]@{}) }
    $gameSettings.general | Add-Member -Force -NotePropertyName language -NotePropertyValue $Language
    Save-Json $settingsPath $gameSettings
}
& (Join-Path $Destination 'Manage-Dragon-Citadel.ps1') -ApplyOnly -Language $Language -Runtime $Destination -Profile $profile
if (-not $NoShortcut) {
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'Smocza Cytadela - projekty.lnk'))
    $shortcut.TargetPath = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
    $shortcut.Arguments = '-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "' + (Join-Path $Destination 'Manage-Dragon-Citadel.ps1') + '" -Runtime "' + $Destination + '" -Profile "' + $profile + '"'
    $shortcut.WorkingDirectory = $Destination; $shortcut.Save()
}
Save-Json (Join-Path $Destination 'installation-receipt.json') @{package=$manifest.package;installedAt=(Get-Date -Format o);runtime=$Destination;profile=$profile;fourth=[bool]$Fourth;graphics=[bool]$Graphics;originalDataSource=$gameData;verifiedPayloadFiles=$manifest.files.Count;backup=$backup}
Write-Output "Zainstalowano Smocza Cytadele: $Destination. Trzecie ulepszenia integralne; czwarte=$Fourth; krajobrazy=$Graphics."
