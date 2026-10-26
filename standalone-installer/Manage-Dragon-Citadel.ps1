param(
    [ValidateSet('Keep','On','Off')][string]$FourthMode = 'Keep',
    [ValidateSet('Keep','On','Off')][string]$GraphicsMode = 'Keep',
    [ValidateSet('Keep','polish','english','german','chinese','japanese','russian','spanish','french')][string]$Language = 'Keep',
    [switch]$ApplyOnly,
    [switch]$Direct,
    [string]$Runtime = "$env:LOCALAPPDATA\Programs\VCMI-Billaden",
    [string]$Profile = "$env:USERPROFILE\Documents\My Games\vcmi"
)
$ErrorActionPreference = 'Stop'
$settingsPath = Join-Path $Profile 'config\modSettings.json'
$name = 'Dragon Citadel - projekty'
function Read-Fourth {
    $s = Get-Content -LiteralPath $settingsPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $p = $s.presets.PSObject.Properties[$name]
    if ($p) { return [bool]$p.Value.settings.'dragon-citadel'.'fourth-upgrades' }
    return $false
}
function Read-Graphics {
    $s = Get-Content -LiteralPath $settingsPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $p = $s.presets.PSObject.Properties[$name]
    if ($p) { return [bool]$p.Value.settings.'dragon-citadel'.'graphics-enhancement' }
    return $false
}
function Apply-Selection([bool]$enabled, [bool]$graphicsEnabled) {
    if (Get-Process VCMI_client,VCMI_server,VCMI_launcher -ErrorAction SilentlyContinue) {
        throw 'Zamknij gre i launcher VCMI przed zmiana zestawu ulepszen.'
    }
    $s = Get-Content -LiteralPath $settingsPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $p = $s.presets.PSObject.Properties[$name]
    if (-not $p) { throw 'Brak naprawionego zestawu Dragon Citadel - projekty.' }
    $p.Value.mods = @('core','vcmi','dragon-citadel')
    $effectiveLanguage = $Language
    if ($effectiveLanguage -eq 'Keep') {
        $effectiveLanguage = (Get-Content -LiteralPath (Join-Path $Profile 'config\settings.json') -Raw -Encoding UTF8 | ConvertFrom-Json).general.language
    }
    if ($effectiveLanguage -in @('polish','german','chinese','japanese','russian','spanish','french')) {
        & (Join-Path $PSScriptRoot 'Install-Game-Language.ps1') -Language $effectiveLanguage -Runtime $Runtime
        $translationId = $effectiveLanguage + '-translation'
        $p.Value.mods += $translationId
        $translationOptions = [pscustomobject]@{}
        $childFolder = Join-Path $Runtime ('Mods\' + $translationId + '\Mods')
        if (Test-Path -LiteralPath $childFolder) {
            Get-ChildItem -LiteralPath $childFolder -Directory | ForEach-Object {
                $childId = $_.Name.ToLowerInvariant()
                $translationOptions | Add-Member -Force -NotePropertyName $childId -NotePropertyValue ($childId -eq 'aitranslated')
            }
        }
        $p.Value.settings | Add-Member -Force -NotePropertyName $translationId -NotePropertyValue $translationOptions
    }
    if ($enabled) { $p.Value.mods += 'wake-of-gods' }
    $dc = $p.Value.settings.'dragon-citadel'
    if ($graphicsEnabled -and -not (Test-Path -LiteralPath (Join-Path $Runtime 'Mods\dragon-citadel\Mods\graphics-enhancement\mod.json')) -and -not (Test-Path -LiteralPath (Join-Path $Profile 'Mods\dragon-citadel\Mods\graphics-enhancement\mod.json'))) {
        throw 'Brak submoda krajobrazow bitew. Zainstaluj aktualny pakiet Smoczej Cytadeli.'
    }
    foreach ($pair in @{'fourth-upgrades'=$enabled; 'graphics-enhancement'=$graphicsEnabled; 'tum'=$false; 'third-upgrades'=$false; 'endgame-rules'=$true; 'chinese-fonts'=$true; 'japanese-fonts'=$true}.GetEnumerator()) {
        $dc | Add-Member -Force -NotePropertyName $pair.Key -NotePropertyValue $pair.Value
    }
    $p.Value.settings.'wake-of-gods' | Add-Member -Force -NotePropertyName level8units -NotePropertyValue $enabled
    $s.activePreset = $name
    $json = $s | ConvertTo-Json -Depth 100
    # Windows PowerShell 5 escapes HTML characters as unicode sequences.
    # VCMI's configuration reader does not decode these sequences correctly.
    $json = [regex]::Replace($json, '\\u(0026|0027|003c|003e)', {
        param($match)
        [string][char][Convert]::ToInt32($match.Groups[1].Value, 16)
    })
    $temporary = $settingsPath + '.dragon-citadel.tmp'
    [IO.File]::WriteAllText($temporary, $json, (New-Object Text.UTF8Encoding($false)))
    [IO.File]::Replace($temporary, $settingsPath, ($settingsPath + '.launcher-previous'), $true)
    if ($Language -ne 'Keep') {
        $gameSettingsPath = Join-Path $Profile 'config\settings.json'
        $gameSettings = Get-Content -LiteralPath $gameSettingsPath -Raw -Encoding UTF8 | ConvertFrom-Json
        if (-not $gameSettings.general) { $gameSettings | Add-Member -Force -NotePropertyName general -NotePropertyValue ([pscustomobject]@{}) }
        $gameSettings.general | Add-Member -Force -NotePropertyName language -NotePropertyValue $Language
        $gameJson = $gameSettings | ConvertTo-Json -Depth 100
        [IO.File]::WriteAllText(($gameSettingsPath + '.language.tmp'), $gameJson, (New-Object Text.UTF8Encoding($false)))
        [IO.File]::Replace(($gameSettingsPath + '.language.tmp'), $gameSettingsPath, ($gameSettingsPath + '.language-previous'), $true)
    }
}
function Start-Game {
    $client = Join-Path $Runtime 'VCMI_client.exe'
    if (-not (Test-Path -LiteralPath $client)) { throw 'Brak silnika BILLADENC4.' }
    Start-Process -FilePath $client -ArgumentList '--nointro' -WorkingDirectory $Runtime -WindowStyle Normal
}
$selected = Read-Fourth
$graphicsSelected = Read-Graphics
if ($GraphicsMode -eq 'On') { $graphicsSelected = $true }
if ($GraphicsMode -eq 'Off') { $graphicsSelected = $false }
if ($FourthMode -eq 'On') { $selected = $true }
if ($FourthMode -eq 'Off') { $selected = $false }
if ($ApplyOnly -or $Direct) {
    Apply-Selection $selected $graphicsSelected
    if ($Direct) { Start-Game }
    exit 0
}
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$form = New-Object Windows.Forms.Form
$form.Text = 'Smocza Cytadela - ulepszenia z projektow'
$form.ClientSize = New-Object Drawing.Size(570,360)
$form.StartPosition = 'CenterScreen'
$form.FormBorderStyle = 'FixedDialog'
$form.MaximizeBox = $false
$main = New-Object Windows.Forms.Label
$main.Location = New-Object Drawing.Point(20,20)
$main.Size = New-Object Drawing.Size(530,55)
$main.Text = "3. ulepszenie: integralna czesc Smoczej Cytadeli.`r`n63 formy klasycznych miast + 9 form Cytadeli z projektow."
$fourth = New-Object Windows.Forms.CheckBox
$fourth.Location = New-Object Drawing.Point(20,85)
$fourth.Size = New-Object Drawing.Size(530,30)
$fourth.Text = 'Wlacz 4. ulepszenie - opcjonalny submod TUM (63 formy)'
$fourth.Checked = $selected
$graphics = New-Object Windows.Forms.CheckBox
$graphics.Location = New-Object Drawing.Point(20,120)
$graphics.Size = New-Object Drawing.Size(530,30)
$graphics.Text = 'Wlacz krajobrazy bitew - opcjonalny submod graficzny'
$graphics.Checked = $graphicsSelected
$languageLabel = New-Object Windows.Forms.Label
$languageLabel.Location = New-Object Drawing.Point(20,170)
$languageLabel.Size = New-Object Drawing.Size(140,25)
$languageLabel.Text = 'Jezyk gry:'
$languageChoice = New-Object Windows.Forms.ComboBox
$languageChoice.Location = New-Object Drawing.Point(170,165)
$languageChoice.Size = New-Object Drawing.Size(380,30)
$languageChoice.DropDownStyle = 'DropDownList'
$languageChoice.DisplayMember = 'Label'
$languageChoice.ValueMember = 'Code'
$languageItems = @(
    [pscustomobject]@{Code='polish';Label='Polski'},
    [pscustomobject]@{Code='english';Label='English'},
    [pscustomobject]@{Code='german';Label='Deutsch'},
    [pscustomobject]@{Code='chinese';Label='简体中文'},
    [pscustomobject]@{Code='japanese';Label='日本語'},
    [pscustomobject]@{Code='russian';Label='Русский'},
    [pscustomobject]@{Code='spanish';Label='Español'},
    [pscustomobject]@{Code='french';Label='Français'}
)
$languageChoice.Items.AddRange([object[]]$languageItems)
$currentLanguage = (Get-Content -LiteralPath (Join-Path $Profile 'config\settings.json') -Raw -Encoding UTF8 | ConvertFrom-Json).general.language
if ($Language -ne 'Keep') { $currentLanguage = $Language }
if (-not $currentLanguage -or $currentLanguage -notin $languageItems.Code) { $currentLanguage = 'english' }
$languageChoice.SelectedItem = @($languageItems | Where-Object { $_.Code -eq $currentLanguage })[0]
$note = New-Object Windows.Forms.Label
$note.Location = New-Object Drawing.Point(20,220)
$note.Size = New-Object Drawing.Size(530,50)
$note.Text = "Nowe formy sprawdzaj w nowej grze. Stare zapisy zachowuja stare jednostki.`r`nWybierz opcje, zapisz ustawienia lub uruchom gre."
$save = New-Object Windows.Forms.Button
$save.Text = 'Zapisz ustawienia'
$save.Location = New-Object Drawing.Point(20,295)
$save.Size = New-Object Drawing.Size(200,40)
$save.Add_Click({ try { $script:Language = [string]$languageChoice.SelectedItem.Code; $form.UseWaitCursor=$true; Apply-Selection $fourth.Checked $graphics.Checked; [Windows.Forms.MessageBox]::Show($script:uiText.saved,$script:uiText.title) | Out-Null } catch { [Windows.Forms.MessageBox]::Show($_.Exception.Message,$script:uiText.error) | Out-Null } finally { $form.UseWaitCursor=$false } })
$play = New-Object Windows.Forms.Button
$play.Text = 'Uruchom gre'
$play.Location = New-Object Drawing.Point(300,295)
$play.Size = New-Object Drawing.Size(250,40)
$play.Add_Click({ try { $script:Language = [string]$languageChoice.SelectedItem.Code; $form.UseWaitCursor=$true; Apply-Selection $fourth.Checked $graphics.Checked; Start-Game; $form.Close() } catch { [Windows.Forms.MessageBox]::Show($_.Exception.Message,$script:uiText.error) | Out-Null } finally { $form.UseWaitCursor=$false } })
$uiCatalog = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'launcher-languages.json') -Raw -Encoding UTF8 | ConvertFrom-Json
function Update-LanguageLabels {
    $code = [string]$languageChoice.SelectedItem.Code
    if (-not $code -or -not $uiCatalog.PSObject.Properties[$code]) { $code='english' }
    $script:uiText = $uiCatalog.PSObject.Properties[$code].Value
    $form.Text=$script:uiText.title; $main.Text=$script:uiText.main
    $fourth.Text=$script:uiText.fourth; $graphics.Text=$script:uiText.graphics
    $languageLabel.Text=$script:uiText.language; $note.Text=$script:uiText.note
    $save.Text=$script:uiText.save; $play.Text=$script:uiText.play
}
$languageChoice.Add_SelectedIndexChanged({ Update-LanguageLabels })
Update-LanguageLabels
$form.Controls.AddRange(@($main,$fourth,$graphics,$languageLabel,$languageChoice,$note,$save,$play))
[void]$form.ShowDialog()
