Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

function Send-CheatCode {
    param([string]$Code)
    Start-Sleep -Milliseconds 150
    [System.Windows.Forms.SendKeys]::SendWait("{TAB}")
    Start-Sleep -Milliseconds 100
    [System.Windows.Forms.SendKeys]::SendWait($Code)
    Start-Sleep -Milliseconds 100
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
}

$form = New-Object System.Windows.Forms.Form
$form.Text = "Dragon Citadel Trainer"
$form.Size = New-Object System.Drawing.Size(360, 330)
$form.StartPosition = "CenterScreen"
$form.TopMost = $true

$label = New-Object System.Windows.Forms.Label
$label.Text = "Click the game window first, then use a button here."
$label.AutoSize = $true
$label.Location = New-Object System.Drawing.Point(18, 18)
$form.Controls.Add($label)

$cheats = @(
    @{ Text = "BILLADEN resources x10"; Code = "nwcbilladen" },
    @{ Text = "Gold and resources"; Code = "nwcshrubbery" },
    @{ Text = "All buildings"; Code = "nwczion" },
    @{ Text = "Win current battle"; Code = "nwcredpill" },
    @{ Text = "Reveal map"; Code = "nwcwhatisthematrix" },
    @{ Text = "More movement"; Code = "nwctrinity" },
    @{ Text = "Level up hero"; Code = "nwcneo" }
)

$y = 55
foreach ($cheat in $cheats) {
    $button = New-Object System.Windows.Forms.Button
    $button.Text = $cheat.Text
    $button.Tag = $cheat.Code
    $button.Size = New-Object System.Drawing.Size(300, 28)
    $button.Location = New-Object System.Drawing.Point(18, $y)
    $button.Add_Click({
        Send-CheatCode -Code $this.Tag
    })
    $form.Controls.Add($button)
    $y += 32
}

$close = New-Object System.Windows.Forms.Button
$close.Text = "Close"
$close.Size = New-Object System.Drawing.Size(300, 28)
$close.Location = New-Object System.Drawing.Point(18, ($y + 8))
$close.Add_Click({ $form.Close() })
$form.Controls.Add($close)

[void]$form.ShowDialog()
