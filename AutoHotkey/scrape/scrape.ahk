#SingleInstance Force

; Activate the script when pressing a hotkey combination
^+u::
{
    ; Get the URL of the active tab in Google Chrome
    url := GetChromeURL()

    ; Copy the URL to the clipboard
    Clipboard := url

    ; RunWait, python "F:/working/@/scrape/scrape.py"

    ; Replace "python" with the path to your Python executable if necessary
    pythonExe := "python"

    ; Replace "script.py" with the path to your Python script
    pythonScript := "C:/Users/Administrator/Documents/AutoHotkey/scrape/scrape.py"

    ; Run the Python script without showing the console window
    Run, % pythonExe " " pythonScript, , Hide

    ; Display the URL in a message box
    ; MsgBox, The URL of the active tab is: %url%
    return
}

GetChromeURL() {
    ; Find the Google Chrome window
    WinGet, chromeWindow, ID, ahk_exe chrome.exe

    ; Activate the Chrome window
    WinActivate, ahk_id %chromeWindow%

    ; Send the appropriate keystrokes to copy the URL
    Send, ^l
    Sleep, 50
    Send, ^c
    Sleep, 50

    ; Retrieve the URL from the clipboard
    url := Clipboard

    ; Return the URL
    return url
}