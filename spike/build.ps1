# Builds the spike as a PyInstaller one-directory app into spike/dist/<name>.
param([string]$Name = "spike", [string[]]$Exclude = @())
$root = Split-Path $PSScriptRoot -Parent
$args = @("--noconfirm", "--onedir", "--windowed", "--name", $Name,
          "--distpath", "$PSScriptRoot\dist", "--workpath", "$PSScriptRoot\build", "--specpath", "$PSScriptRoot\build")
foreach ($m in $Exclude) { $args += @("--exclude-module", $m) }
& "$root\.venv\Scripts\pyinstaller.exe" @args --paths $PSScriptRoot "$PSScriptRoot\main.py"
