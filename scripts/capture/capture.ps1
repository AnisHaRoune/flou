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
    [int] $max_error_count = 10,
    [string] $camera_name = "STC-MBS231U3V(16H6167)"
)

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
                Write-Host "ffmpeg capture..."
                $distance_index = $distance * $i
				$distance_name = $distance_index.ToString().PadLeft(8, "0")
				$capture_index = $j.ToString().PadLeft(8, "0")
                $filepath = "captures\$distance_name-$unity-$capture_index.png"
                $result = .\ffmpeg-3.4.2-win32-static\bin\ffmpeg.exe -loglevel error -f dshow -rtbufsize 128M -i video="$camera_name" -vf vflip -vframes 1 "$filepath" -y 2>&1
                $error = $result -match "error"
                if ($error)
                {
                    Write-Warning "$result"
                    $j--
                    $error_count++

                    if ($error_count -ge $max_error_count)
                    {
                        throw "Too many ffmpeg error ($error_count), aborting."
                    }

                    Start-Sleep -Seconds 1
                }
                else
                {
                    Write-Host $filepath
                    $error_count = 0
                }
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