DramaFever Subtitle Ripper (DFRip)
==================================

Easily download subtitle files for your favorite shows from [DramaFever](http://www.dramafever.com/).
You can either keep them in the original [TTML](http://www.w3.org/TR/ttaf1-dfxp/) format or convert them to the more 
commonly used [SRT](http://en.wikipedia.org/wiki/SubRip) subtitle format.

# Requirements

* Python 2.7.x
* [requests](http://docs.python-requests.org/en/latest/)
* [BeautifulSoup 4](http://www.crummy.com/software/BeautifulSoup/)

You can download and install these modules from [PyPi](https://pypi.python.org/pypi) with `pip`:

```
pip install requests
pip install beautifulsoup4
```

or 

```
pip install -r requirements.txt
```

or by going to the respective module's website.

# Usage

```
usage: dfrip.py [-h] [-f {srt,ttml,xml}] [-o FILENAME] [-v] SERIES EPISODE
Download subtitles from DramaFever and convert them into TTML or SRT.

positional arguments:
  SERIES                the ID of the series (usually four-digit number)
  EPISODE               the number of the episode

optional arguments:
  -h, --help            show this help message and exit
  -f {srt,ttml,xml}, --format {srt,ttml,xml}
                        the format the subtitles will be saved in (default:
                        xml)
  -o FILENAME, --out FILENAME
                        location of the output file or filename (default: .)
  -v, --verbose         increases output verbosity (default: False)
```

# Examples

Downloading the subtitles for episode 119 of _Running Man_.

1. Go to DramaFever's _Running Man_ page.
2. You will see the following in your browser's address bar: `http://www.dramafever.com/drama/3970/Running_Man/`.
Copy or remember the show's ID (3970).
3. Execute the following command to download the subtitles as TTML:

```
./dfrip.py 3970 119
```

Download the subtitles as SRT:

```
./dfrip.py 3970 119 -f srt
```
  
Download the subtitles to "running_man-119.srt" and show additional infos about the show:

```
./dfrip.py 3970 119 -v -f srt -o "running_man-119.srt"
```
