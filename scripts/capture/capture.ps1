Param
(
    [Parameter(Mandatory=$true)]
    [string] $COM,
    [Parameter(Mandatory=$true)]
    [int] $number_of_captures,
    [Parameter(Mandatory=$true)]
    [int] $distance,
    [Parameter(Mandatory=$true)]
    [string] $unity,
    [int] $number_of_captures_by_step = 1,
    [string] $capture_name = "capture"
)

$directory = Get-Location

if (($unity -ne "cm") -and ($unity -ne "mm") -and ($unity -ne "um"))
{
    Write-Error "unity must be cm, mm or um."
}
else
{
    New-Item -ItemType Directory -Name "captures" -Force | Out-Null
    $port = new-Object System.IO.Ports.SerialPort $COM, 9600, None, 8, one

    try
    {
        Write-Host "Opening $COM..."
        $port.Open()
        Write-Host "$COM open."
        Write-Host "Begin platform control."

        for($i = 0; $i -lt $number_of_captures; $i++)
        {
            for($j = 0; $j -lt $number_of_captures_by_step; $j++)
            {
                # Start-Process -NoNewWindow -Wait -FilePath "$directory\ffmpeg-3.4.2-win32-static\bin\ffmpeg.exe" -ArgumentList "-f dshow -i video='STC-MBS231U3V(16H6167)' -vframes 1 '$directory\captures\$capture_name-$j-$i.png' -y"
                Invoke-Expression ".\ffmpeg-3.4.2-win32-static\bin\ffmpeg.exe -f dshow -rtbufsize 128M -i video='STC-MBS231U3V(16H6167)' -vf vflip -vframes 1 'captures\$capture_name-$j-$i.png' -y"
            }

            $command = "m$distance$unity"
            Write-Host $command
            $port.WriteLine($command)
            do
            {
                $ouput = $port.ReadExisting()
                Write-Host -NoNewline $ouput                
                $end = $ouput -match '\n'
            } until ($end)
        }
    }
    catch
    {
        Write-Error $_.Exception.Message
    }
    finally
    {
        Write-Host "End of platform control."
        Get-EventSubscriber | Unregister-Event
        Get-Job | Remove-Job -Force
        $port.Close()
        Write-Host "$COM closed."
    }
}