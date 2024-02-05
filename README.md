# game-ost-downloader

A small program for bulk downloading game OSTs from <http://downloads.khinsider.com/>.

## How To Use

You can download the current version of the application from the [releases page](https://github.com/matteo-molnar/game-ost-downloader/releases).

You will need to provide URLs of the sountracks you would like to download from khinsider. An example of a valid URL is <https://downloads.khinsider.com/game-soundtracks/album/moss-book-2018>. You will also need to specify an output dirctory where the program will save the downloaded files.

![screenshot](/assets/screenshot.png)

## Install For Local Development

The only thing you need to install is python3: <https://www.python.org/downloads/>

Tested and working with python 3.11.5.

You can create a virtual environment in the repo and install the required dependencies with these commands from the project root:

```bash
 virtualenv .venv
 activate .venv  #This will vary by OS
 pip install -r requirements.txt
```

If you want to do things quick and dirty and not create a venv, you will still need to install the script dependencies globally:

```bash
pip install -r requirements.txt
```
