# Путь к общему лог-файлу
$logPath = "\\srv-ad.dnestrschool1.online\share\Logonlogs\UserLogons.csv"

# Создание папки для логов, если она не существует
$logFolder = Split-Path -Path $logPath
if (-not (Test-Path -Path $logFolder)) {
    New-Item -Path $logFolder -ItemType Directory
}

# Создание файла лога с заголовками, если он не существует
if (-not (Test-Path -Path $logPath)) {
    "UserName,LogonTime,ComputerName" | Out-File -FilePath $logPath -Encoding UTF8
}

# Сбор информации о пользователе
$userName = $env:USERNAME
$logonTime = Get-Date -Format "yy-MM-dd HH:mm"
$computerName = $env:COMPUTERNAME

# Запись информации в лог-файл
$csvLine = "$userName,$logonTime,$computerName"
Add-Content -Path $logPath -Value $csvLine -Encoding UTF8

Write-Host "Информация о входе пользователя $userName записана"