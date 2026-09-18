param(
    [string]$Root = "D:\MediaServer",
    [string]$InventoryCsv = "$PSScriptRoot\GOLDEN_inventory.csv",
    [string]$HashFile = "$PSScriptRoot\GOLDEN_inventory.sha256"
)

$ErrorActionPreference="Stop"

if(-not(Test-Path -LiteralPath $InventoryCsv -PathType Leaf)){
    throw "Inventory not found: $InventoryCsv"
}
if(-not(Test-Path -LiteralPath $HashFile -PathType Leaf)){
    throw "Hash file not found: $HashFile"
}

$expectedHash=(Get-Content -LiteralPath $HashFile -Raw).Trim()
$actualHash=(Get-FileHash -LiteralPath $InventoryCsv -Algorithm SHA256).Hash
if($expectedHash -ne $actualHash){
    throw "Inventory SHA256 mismatch. Restore aborted."
}

$rows=@(Import-Csv -LiteralPath $InventoryCsv)

foreach($c in @("Movies","Series","Anime","Cartoons")){
    New-Item -ItemType Directory -Force -Path (Join-Path $Root $c) | Out-Null
}

foreach($r in $rows){
    $dest=Join-Path $Root $r.RelativePath
    if(-not(Test-Path -LiteralPath $dest)){
        New-Item -ItemType Directory -Force -Path $dest | Out-Null
    }
}

Write-Host "Folder structure restored from verified GOLDEN_inventory.csv" -ForegroundColor Green
