# Stáhne fotky apartmánu z inzerátu na ceskehory.cz do assets\img\
# Spuštění (PowerShell, ve složce webu):  .\stahnout-fotky.ps1
# Poznámka: fotky patří majitelům apartmánu. Pro ostrý web je lepší použít jejich originály
# (vyšší rozlišení). Tenhle skript slouží k tomu, aby měl návrh hned reálné fotky.

$ErrorActionPreference = "Stop"
$base = "https://www.ceskehory.cz/objekty/data/hotely/apartmanmili/"
$files = @("imagew.jpg", "x1a.jpg", "x2a.jpg", "x3a.jpg", "x4a.jpg", "x5a.jpg")
$dest = Join-Path $PSScriptRoot "assets\img"
New-Item -ItemType Directory -Force -Path $dest | Out-Null

foreach ($f in $files) {
    $target = Join-Path $dest $f
    try {
        Invoke-WebRequest -Uri ($base + $f) -OutFile $target -UserAgent "Mozilla/5.0"
        $kb = [math]::Round((Get-Item $target).Length / 1KB)
        Write-Host "OK   $f ($kb kB)"
    } catch {
        Write-Host "CHYBA $f : $($_.Exception.Message)" -ForegroundColor Red
    }
}
Write-Host "`nHotovo. Spusťte 'python build.py' (nebo otevřete index.html)."
