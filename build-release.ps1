param([string]$GameDir = "")
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$mod = Join-Path $here 'WildChickenIsChicken'
& (Join-Path $mod 'build.ps1') -GameDir $GameDir
$dll = Join-Path $mod 'WildChickenIsChicken.dll'
if (-not (Test-Path -LiteralPath $dll)) { throw 'Compiled mod DLL is missing.' }
$stage = Join-Path $here ('release-' + [guid]::NewGuid().ToString('N'))
$output = Join-Path $here 'WildChickenIsChicken-v0.1.2-install.zip'
try {
    $target = Join-Path $stage 'WildChickenIsChicken'
    New-Item -ItemType Directory -Path $target -Force | Out-Null
    foreach ($name in @('Config', 'UIAtlases', 'ItemIcons', 'ModInfo.xml', 'WildChickenIsChicken.dll', 'src', 'build.cmd', 'build.ps1', 'README.txt')) {
        Copy-Item -LiteralPath (Join-Path $mod $name) -Destination $target -Recurse
    }
    foreach ($name in @('build.cmd', 'build-release.cmd', 'build-release.ps1', 'README.md', 'START-HERE.txt', 'CHANGELOG.md', 'VALIDATION.md')) {
        Copy-Item -LiteralPath (Join-Path $here $name) -Destination $stage
    }
    $temporaryZip = Join-Path $here ('install-' + [guid]::NewGuid().ToString('N') + '.zip')
    Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $temporaryZip
    Move-Item -LiteralPath $temporaryZip -Destination $output -Force
} finally {
    if ($temporaryZip -and (Test-Path -LiteralPath $temporaryZip)) { Remove-Item -LiteralPath $temporaryZip -Force }
    if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
}
Write-Host "[WildChickenIsChicken] Install ZIP: $output"
