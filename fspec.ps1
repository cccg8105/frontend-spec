$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& python "$ScriptDir\cli\main.py" @args
exit $LASTEXITCODE
