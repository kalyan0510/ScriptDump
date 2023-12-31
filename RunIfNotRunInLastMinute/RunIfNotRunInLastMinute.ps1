$registryPath = "HKCU:\Software\YourScriptName"  # Adjust as needed

# Create the registry key if it doesn't exist
if (!(Test-Path $registryPath)) {
    New-Item $registryPath -Force
}

# Get the last run timestamp from the registry, handling potential errors
$lastRunTimestamp = Get-ItemProperty $registryPath -Name LastRunTimestamp -ErrorAction SilentlyContinue
if (!$lastRunTimestamp) {
    # Property doesn't exist, create it with a default value
    New-ItemProperty $registryPath -Name LastRunTimestamp -Value ($currentTime.ToString("yyyy-MM-dd HH:mm:ss")) -PropertyType String
} else {
    # Property exists, convert the string value back to a DateTime object
    $lastRunTimestampValue = [DateTime]$lastRunTimestamp.LastRunTimestamp
}

$currentTime = Get-Date

# TODO change the timespan as you wish
# Execute script actions only if not run in the last minute
if ($currentTime - $lastRunTimestampValue -gt (New-TimeSpan -Seconds 10)) {
    Write-Output "Running the script..."

    # Your script actions here (e.g., sending an email)

    # $cmdCommand = 'echo "Hello, this is your command prompt! currentTime: \$currentTime, lastRunTime: \$($lastRunTime.LastWriteTime)" && pause'

    # # Start the cmd process
    # Start-Process -FilePath 'cmd.exe' -ArgumentList "/c $cmdCommand"
    net use T: /delete

    # TODO fill up spaces
    net use T: \\sshfs\kalyan@SERVERIPADDRESS!PORT /persistent:yes /user:kalyan PASSWDHERE


    # Update the timestamp in the registry (as a string)
    New-ItemProperty $registryPath -Name LastRunTimestamp -Value ($currentTime.ToString("yyyy-MM-dd HH:mm:ss")) -PropertyType String -Force  # Use -Force to overwrite any existing value
}
#pause
