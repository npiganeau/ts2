; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "TS2"
#define MyAppVersion "0.7.4"
#define MyAppPublisher "TS2 Team"
#define MyAppURL "http://ts2.github.io"
#define MyAppExeName "ts2.exe"
#define PythonVersion "3.6"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{EA342016-D18E-440E-BF2F-DF1EAED885DA}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName=Train Signalling Simulation
DisableProgramGroupPage=yes
LicenseFile=build\exe.win32-{#PythonVersion}\doc\COPYING.txt
OutputDir=dist
OutputBaseFilename={#MyAppName}-{#MyAppVersion}-setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"; InfoAfterFile: "build\exe.win32-{#PythonVersion}\doc\README.txt"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"; InfoAfterFile: "build\exe.win32-{#PythonVersion}\doc\README_fr.txt"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "build\exe.win32-{#PythonVersion}\ts2.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "build\exe.win32-{#PythonVersion}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Flags: nowait postinstall skipifsilent 64bit; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"

