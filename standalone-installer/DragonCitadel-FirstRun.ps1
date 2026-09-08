param(
    [string]$SourcePath = "",
    [switch]$Quiet
)

Add-Type -AssemblyName System.Windows.Forms
$ErrorActionPreference = "Stop"

$installDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$dirsPath = Join-Path $installDir "config\dirs.json"

function Show-Info([string]$Message) {
    if (-not $Quiet) {
        [System.Windows.Forms.MessageBox]::Show(
            $Message,
            "Dragon Citadel",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Information
        ) | Out-Null
    }
}

function Show-Error([string]$Message) {
    if (-not $Quiet) {
        [System.Windows.Forms.MessageBox]::Show(
            $Message,
            "Dragon Citadel",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Error
        ) | Out-Null
    }
}

function Get-DataDirectory([string]$Root) {
    if (-not $Root -or -not (Test-Path -LiteralPath $Root)) {
        return $null
    }

    $required = @("H3bitmap.lod", "H3sprite.lod", "H3ab_bmp.lod", "H3ab_spr.lod", "Heroes3.snd")
    foreach ($candidate in @($Root, (Join-Path $Root "Data"))) {
        if (-not (Test-Path -LiteralPath $candidate -PathType Container)) {
            continue
        }
        $missing = @($required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $candidate $_) -PathType Leaf) })
        if ($missing.Count -eq 0) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }
    return $null
}

function Add-Candidate([System.Collections.Generic.List[string]]$List, [string]$Path) {
    if ($Path -and (Test-Path -LiteralPath $Path) -and -not $List.Contains($Path)) {
        $List.Add($Path)
    }
}

function Link-Or-Copy([string]$Source, [string]$Destination, [switch]$AlwaysCopy) {
    if (Test-Path -LiteralPath $Destination) {
        $sourceInfo = Get-Item -LiteralPath $Source
        $destinationInfo = Get-Item -LiteralPath $Destination
        if ($sourceInfo.Length -eq $destinationInfo.Length) {
            return
        }
        [System.IO.File]::Delete($Destination)
    }

    if (-not $AlwaysCopy) {
        try {
            New-Item -ItemType HardLink -Path $Destination -Target $Source -ErrorAction Stop | Out-Null
            return
        } catch {
        }
    }
    Copy-Item -LiteralPath $Source -Destination $Destination -Force
}

try {
    if (-not (Test-Path -LiteralPath $dirsPath)) {
        throw "Missing isolated profile configuration: $dirsPath"
    }

    $dirs = Get-Content -LiteralPath $dirsPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $profileRoot = [Environment]::ExpandEnvironmentVariables($dirs.userDataPath)
    $configRoot = [Environment]::ExpandEnvironmentVariables($dirs.userConfigPath)
    $logsRoot = [Environment]::ExpandEnvironmentVariables($dirs.userLogsPath)
    $savesRoot = [Environment]::ExpandEnvironmentVariables($dirs.userSavePath)

    foreach ($directory in @($profileRoot, $configRoot, $logsRoot, $savesRoot, (Join-Path $profileRoot "Data"), (Join-Path $profileRoot "Mp3"))) {
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
    }

    $existingProfileData = Get-DataDirectory $profileRoot
    $imported = $false
    if (-not $existingProfileData) {
        $candidates = [System.Collections.Generic.List[string]]::new()
        if ($SourcePath) {
            Add-Candidate $candidates $SourcePath
        }

        $documents = [Environment]::GetFolderPath("MyDocuments")
        Add-Candidate $candidates (Join-Path $documents "My Games\vcmi")
        Add-Candidate $candidates "C:\GOG.com\Heroes of Might and Magic 3 Complete"
        Add-Candidate $candidates "C:\GOG Games\Heroes of Might and Magic 3 Complete"

        $registryRoots = @(
            "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*",
            "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
            "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*"
        )
        foreach ($entry in Get-ItemProperty $registryRoots -ErrorAction SilentlyContinue) {
            if ($entry.DisplayName -match "Heroes of Might.*Magic.*III" -and $entry.InstallLocation) {
                Add-Candidate $candidates $entry.InstallLocation
            }
        }

        $sourceData = $null
        foreach ($candidate in $candidates) {
            $sourceData = Get-DataDirectory $candidate
            if ($sourceData) {
                break
            }
        }

        if (-not $sourceData -and -not $Quiet) {
            $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
            $dialog.Description = "Choose your legal Heroes III Complete / Shadow of Death folder, or an existing VCMI data folder."
            $dialog.ShowNewFolderButton = $false
            if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
                $sourceData = Get-DataDirectory $dialog.SelectedPath
            }
        }

        if (-not $sourceData) {
            throw "Heroes III Complete / Shadow of Death data was not found. Install a legal copy or select its folder and run Dragon Citadel again. Heroes III HD Edition is not compatible."
        }

        $targetData = Join-Path $profileRoot "Data"
        $dataFiles = @(
            "H3ab_ahd.snd",
            "H3ab_ahd.vid",
            "H3ab_bmp.lod",
            "H3ab_spr.lod",
            "H3bitmap.lod",
            "H3sprite.lod",
            "Heroes3.snd",
            "VIDEO.VID",
            "HiScore.dat"
        )
        foreach ($name in $dataFiles) {
            $sourceFile = Join-Path $sourceData $name
            if (Test-Path -LiteralPath $sourceFile -PathType Leaf) {
                Link-Or-Copy $sourceFile (Join-Path $targetData $name) -AlwaysCopy:($name -eq "HiScore.dat")
            }
        }

        $sourceRoot = Split-Path -Parent $sourceData
        $sourceMusic = Join-Path $sourceRoot "Mp3"
        if (Test-Path -LiteralPath $sourceMusic -PathType Container) {
            $excludedMusic = "^(CoveTown|Dargem|Factory|HotACamp|HIGHLANDS|WASTELAND)"
            Get-ChildItem -LiteralPath $sourceMusic -File -Filter "*.mp3" | Where-Object { $_.Name -notmatch $excludedMusic } | ForEach-Object {
                Link-Or-Copy $_.FullName (Join-Path (Join-Path $profileRoot "Mp3") $_.Name)
            }
        }

        Set-Content -LiteralPath (Join-Path $profileRoot "import-source.txt") -Value $sourceData -Encoding UTF8
        $imported = $true
    }

    $modSettings = [ordered]@{
        activeMods = $null
        activePreset = "dragon-citadel-only"
        presets = [ordered]@{
            "dragon-citadel-only" = [ordered]@{
                mods = @("vcmi", "core", "dragon-citadel", "chinese-maps-collection")
                settings = [ordered]@{
                    "dragon-citadel" = [ordered]@{
                        "creator-tools" = $false
                        "endgame-rules" = $true
                    }
                }
            }
        }
        validatedMods = [ordered]@{}
    }
    $modSettings | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $configRoot "modSettings.json") -Encoding UTF8

    $settingsPath = Join-Path $configRoot "settings.json"
    if (Test-Path -LiteralPath $settingsPath) {
        $settings = Get-Content -LiteralPath $settingsPath -Raw | ConvertFrom-Json
    } else {
        $settings = [pscustomobject]@{}
    }

    foreach ($section in @("general", "launcher", "mods", "video")) {
        if (-not $settings.PSObject.Properties[$section]) {
            $settings | Add-Member -NotePropertyName $section -NotePropertyValue ([pscustomobject]@{})
        }
    }
    if (-not $settings.video.PSObject.Properties["resolution"]) {
        $settings.video | Add-Member -NotePropertyName "resolution" -NotePropertyValue ([pscustomobject]@{})
    }

    $settings.general | Add-Member -Force -NotePropertyName "language" -NotePropertyValue "polish"
    $settings.general | Add-Member -Force -NotePropertyName "saveFrequency" -NotePropertyValue 1
    $settings.general | Add-Member -Force -NotePropertyName "autosaveCountLimit" -NotePropertyValue 1
    $settings.general | Add-Member -Force -NotePropertyName "useSavePrefix" -NotePropertyValue $false
    $settings.general | Add-Member -Force -NotePropertyName "savePrefix" -NotePropertyValue ""
    $settings.general | Add-Member -Force -NotePropertyName "startTurnAutosave" -NotePropertyValue $true
    $settings.launcher | Add-Member -Force -NotePropertyName "setupCompleted" -NotePropertyValue $true
    $settings.mods | Add-Member -Force -NotePropertyName "validation" -NotePropertyValue "full"
    $settings.video | Add-Member -Force -NotePropertyName "fullscreen" -NotePropertyValue $false
    $settings.video.resolution | Add-Member -Force -NotePropertyName "width" -NotePropertyValue 800
    $settings.video.resolution | Add-Member -Force -NotePropertyName "height" -NotePropertyValue 600
    $settings | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $settingsPath -Encoding UTF8

    if ($imported) {
        Show-Info "Heroes III data was imported automatically. Dragon Citadel now uses an isolated profile with the required core, Dragon Citadel and bundled Maps Collection modules enabled."
    }
    exit 0
} catch {
    Show-Error $_.Exception.Message
    Write-Error $_
    exit 1
}
