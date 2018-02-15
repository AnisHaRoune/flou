Param
(
  [string]$COM
)

$port= new-Object System.IO.Ports.SerialPort $COM, 9600, None, 8, one
Register-ObjectEvent -InputObject $port -EventName DataReceived -Action {printBuffer} | Out-Null

function global:printBuffer
{
    do
    {
        $port.Read($buffer, 0, $port.BytesToRead)
        Write-Host -NoNewline $buffer
    }
    while ([string]::IsNullOrEmpty($buffer))
}

try
{
    Write-Host -NoNewline "Ouverture du port $COM... "
    $port.Open()
    Write-Host "Port $COM ouvert."

    Write-Host "Démarrage du contrôle de la plateforme."
    while ($port.IsOpen)
    {
        $command = Read-Host
        $port.WriteLine($command)
    }
}
catch
{
    Write-Host -Foreground Red -Background Black $_.Exception.Message
}
finally
{
    Write-Host "Fin du contrôle de la plateforme."
    $port.Close()
    Write-Host "Port $COM fermé."
}