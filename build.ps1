Invoke-Expression -Command "pyinstaller --windowed --name game-ost-downloader --icon=assets/music_note.ico .\src\main.py"
Compress-Archive -Path ".\dist\game-ost-downloader\" -DestinationPath ".\dist\game-ost-downloader.zip"
