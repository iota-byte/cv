@echo off
setlocal enabledelayedexpansion

set "key=iota"
set "input_file=encoded_script.bin"  REM Change this to your encoded file name
set "output_file=decoded_script.php"

REM Clear the output file
echo. > "%output_file%"

REM Read the input file and decode it
for /f "delims=" %%a in ('type "%input_file%"') do (
    set "line=%%a"
    set "decoded_line="
    for /l %%i in (0,1,255) do (
        set /a "char=!line:~%%i,1! ^ !key:~%%i %% key:~0,1!"
        set "decoded_line=!decoded_line!!char!"
    )
    echo !decoded_line! >> "%output_file%"
)

echo File decoded as "%output_file%"
