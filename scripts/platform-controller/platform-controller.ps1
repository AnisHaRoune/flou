Param
(
  [string]$COM
)

function global:printBuffer
{
    Write-Host -NoNewline $port.ReadExisting()
}

$port = new-Object System.IO.Ports.SerialPort $COM, 9600, None, 8, one

try
{
    Write-Host "Ouverture du port $COM..."

    $port.Open()
    Register-ObjectEvent $port DataReceived -Action {printBuffer} | Out-Null

    Write-Host "Port $COM ouvert."

    Write-Host "Démarrage du contrôle de la plateforme."
    while ($port.IsOpen)
    {
        while ([Console]::KeyAvailable)
        {
            $key = [System.Console]::ReadKey()
            $port.Write($key.KeyChar)
            $port.BaseStream.FlushAsync()
        }
    }
}
catch
{
    Write-Error $_.Exception.Message
}
finally
{
    Write-Host "Fin du contrôle de la plateforme."
    Get-EventSubscriber | Unregister-Event
    Get-Job | Remove-Job -Force
    $port.Close()
    Write-Host "Port $COM fermé."
}