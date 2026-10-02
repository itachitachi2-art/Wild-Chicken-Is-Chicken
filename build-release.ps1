param([string]$GameDir = "")
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$mod = Join-Path $here 'WildChickenIsChicken'
& (Join-Path $mod 'build.ps1') -GameDir $GameDir
$dll = Join-Path $mod 'WildChickenIsChicken.dll'
if (-not (Test-Path -LiteralPath $dll)) { throw 'Compiled mod DLL is missing.' }
$stage = Join-Path $here ('release-' + [guid]::NewGuid().ToString('N'))
$output = Join-Path $here 'WildChickenIsChicken-v0.1.1-install.zip'
try {
    $target = Join-Path $stage 'WildChickenIsChicken'
    New-Item -ItemType Directory -Path $target -Force | Out-Null
    foreach ($name in @('Config', 'UIAtlases', 'ItemIcons', 'ModInfo.xml', 'WildChickenIsChicken.dll')) {
        Copy-Item -LiteralPath (Join-Path $mod $name) -Destination $target -Recurse
    }
    $instructions = 'Wild Chicken Is Chicken v0.1.1' + [Environment]::NewLine +
        'Extract and copy WildChickenIsChicken into your Mods directory. Disable EAC.' + [Environment]::NewLine +
        'To update, fully exit the game before replacing the old mod folder.'
    [System.IO.File]::WriteAllText((Join-Path $target 'README.txt'), $instructions, (New-Object System.Text.UTF8Encoding($true)))
    $temporaryZip = Join-Path $stage 'install.zip'
    Compress-Archive -LiteralPath $target -DestinationPath $temporaryZip
    Move-Item -LiteralPath $temporaryZip -Destination $output -Force
} finally {
    if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
}
Write-Host "[WildChickenIsChicken] Install ZIP: $output"
