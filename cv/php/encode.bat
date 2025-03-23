@echo off
setlocal enabledelayedexpansion

set "key=iota"
set "input_file=your_script.php"  REM Change this to your file name
set "output_file=encoded_script.bin"

REM Clear the output file
echo. > "%output_file%"

REM Read the input file and encode it
for /f "delims=" %%a in ('type "%input_file%"') do (
    set "line=%%a"
    set "encoded_line="
    for /l %%i in (0,1,255) do (
        set /a "char=!line:~%%i,1! ^ !key:~%%i %% key:~0,1!"
        set "encoded_line=!encoded_line!!char!"
    )
    echo !encoded_line! >> "%output_file%"
)

echo File encoded as "%output_file%"
