# Download Git LFS installer
$url = "https://github.com/git-lfs/git-lfs/releases/download/v3.4.1/git-lfs-windows-v3.4.1.exe"
$output = "$env:TEMP\git-lfs-installer.exe"

Write-Host "Downloading Git LFS installer..."
Invoke-WebRequest -Uri $url -OutFile $output

Write-Host "Installing Git LFS..."
Start-Process -FilePath $output -ArgumentList "/VERYSILENT" -Wait

Write-Host "Installation complete. Please restart your terminal."
