[Setup]
AppName=ΑΔΑΜ
AppVersion=1.0
; ΣΗΜΑΝΤΙΚΟ 1: Εγκατάσταση στο AppData για να μη ζητάει Admin.
DefaultDirName={userappdata}\ADAM
; ΣΗΜΑΝΤΙΚΟ 2: Δηλώνουμε ότι τρέχει με ελάχιστα δικαιώματα.
PrivilegesRequired=lowest
OutputDir=Output
OutputBaseFilename=ADAM_Installer
Compression=lzma
SolidCompression=yes
DisableDirPage=yes

[Files]
; Πάρε όλα τα αρχεία του φακέλου dist\ADAM από το pyinstaller
Source: "dist\ADAM\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Registry]
; ΣΗΜΑΝΤΙΚΟ 3: Εγγραφή στο HKCU για το δεξί κλικ χωρίς Admin Rights.
Root: HKCU; Subkey: "Software\Classes\*\shell\OpenWithADAM"; ValueType: string; ValueData: "Αντιγραφή ΑΔΑΜ"; Flags: uninsdeletekey
; Προσθήκη εικονιδίου στο μενού (παίρνει το εικονίδιο από το ίδιο το .exe)
Root: HKCU; Subkey: "Software\Classes\*\shell\OpenWithADAM"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\ADAM.exe"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\*\shell\OpenWithADAM\command"; ValueType: string; ValueData: """{app}\ADAM.exe"" ""%1"""; Flags: uninsdeletekey
