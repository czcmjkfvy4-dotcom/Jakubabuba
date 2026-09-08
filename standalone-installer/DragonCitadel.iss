#define MyAppName "Smocza Cytadela"
#define MyAppVersion "1.5.7"
#define MyAppPublisher "Billaden"
#define MyAppURL "https://github.com/czcmjkfvy4-dotcom/Jakubabuba"
#define MyAppExeName "VCMI_client.exe"

[Setup]
AppId={{D4A3E3C0-6DF6-4A6D-B3CE-C61D6C69CC55}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} - Complete Edition {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={localappdata}\Programs\Dragon Citadel
DefaultGroupName=Smocza Cytadela
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=output
OutputBaseFilename=Smocza_Cytadela_Complete_Edition_1.5.7_Setup
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
WizardImageFile=assets\wizard.bmp
WizardSmallImageFile=assets\wizard-small.bmp
SetupIconFile=assets\dragon-citadel.ico
UninstallDisplayIcon={app}\DragonCitadel.ico
InfoBeforeFile=LEGAL.txt
CloseApplications=yes
RestartApplications=no
SetupLogging=yes
ArchitecturesAllowed=x64compatible
VersionInfoVersion=1.5.7.0
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Dragon Citadel standalone VCMI edition
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

[Languages]
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "staging\engine\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\Smocza Cytadela"; Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ""{app}\Launch-Dragon-Citadel.ps1"""; WorkingDir: "{app}"; IconFilename: "{app}\DragonCitadel.ico"
Name: "{autodesktop}\Smocza Cytadela"; Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ""{app}\Launch-Dragon-Citadel.ps1"""; WorkingDir: "{app}"; IconFilename: "{app}\DragonCitadel.ico"; Tasks: desktopicon
Name: "{autoprograms}\Smocza Cytadela - importuj lub napraw dane"; Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{app}\Launch-Dragon-Citadel.ps1"" -SetupOnly"; WorkingDir: "{app}"; IconFilename: "{app}\DragonCitadel.ico"

[Tasks]
Name: "desktopicon"; Description: "Utworz skrot Smoczej Cytadeli na pulpicie"; GroupDescription: "Skroty:"; Flags: checkedonce

[Run]
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ""{app}\Launch-Dragon-Citadel.ps1"""; WorkingDir: "{app}"; Description: "Uruchom Smocza Cytadele"; Flags: postinstall nowait skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\install.log"

[Code]
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpWelcome then
  begin
    WizardForm.WelcomeLabel2.Caption :=
      'Osobna edycja Smoczej Cytadeli z silnikiem VCMI 1.7.5 i runtime BILLADENC4.' + #13#10 + #13#10 +
      'Instalator tworzy odizolowany profil z tym modem, wymaganymi skladnikami VCMI i duzym pakietem map.';
  end;
end;
