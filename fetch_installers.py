import argparse
import json
import logging
import os
import re
import urllib.request
import urllib.parse
from urllib.parse import urljoin
from html.parser import HTMLParser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])

def get_7zip_url():
    try:
        url = 'https://www.7-zip.org/download.html'
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
        # Find the first x64 exe link
        match = re.search(r'href="(a/7z\d+-x64\.exe)"', html)
        if match:
            return urljoin(url, match.group(1))
    except Exception as e:
        logging.error(f"Failed to get 7zip URL: {e}")
    return None

def get_notepad_url():
    try:
        url = 'https://notepad-plus-plus.org/downloads/'
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
        # Find the latest version
        match = re.search(r'href="/downloads/(v[\d.]+)/"', html)
        if match:
            version = match.group(1)
            return f'https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/{version}/npp.{version[1:]}.Installer.x64.exe'
    except Exception as e:
        logging.error(f"Failed to get notepad URL: {e}")
    return None

def get_chrome_url():
    # Fixed URL for latest enterprise MSI 64-bit
    return 'https://dl.google.com/dl/chrome/install/googlechromestandaloneenterprise64.msi'

def get_chrome_version():
    try:
        url = 'https://versionhistory.googleapis.com/v1/chrome/platforms/win/channels/stable/versions/all/releases?filter=endtime=none'
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
        return data['releases'][0]['version']
    except Exception as e:
        logging.warning(f"Failed to get chrome version: {e}")
        return 'latest'

def get_winscp_url():
    try:
        url = 'https://winscp.net/eng/download.php'
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
        # Find the setup exe link
        match = re.search(r'href="(/download/WinSCP-[\d.]+\-Setup\.exe/download)"', html)
        if match:
            return urljoin(url, match.group(1))
    except Exception as e:
        logging.error(f"Failed to get winscp URL: {e}")
    return None

def get_webex_url():
    return 'https://binaries.webex.com/WebexTeamsDesktop-Windows-Gold/Webex.msi'

def get_zoom_url():
    return 'https://zoom.us/client/latest/ZoomInstallerFull.msi'

def get_zoomoutlook_url():
    return 'https://zoom.us/client/latest/ZoomOutlookPluginSetup.msi'

def download_file(url, filename):
    try:
        logging.info(f"Downloading {filename} from {url}")
        urllib.request.urlretrieve(url, filename)
        logging.info(f"Downloaded {filename}")
    except Exception as e:
        logging.error(f"Failed to download {filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Download installers for specified apps.')
    parser.add_argument('--apps', type=str, help='Comma-separated list of apps: 7zip,notepad,chrome,winscp,webex,zoom,zoomoutlook or --all')
    parser.add_argument('--all', action='store_true', help='Download all apps')
    parser.add_argument('--7zip', action='store_true', help='Download 7-Zip')
    parser.add_argument('--notepad', action='store_true', help='Download Notepad++')
    parser.add_argument('--chrome', action='store_true', help='Download Google Chrome Enterprise')
    parser.add_argument('--winscp', action='store_true', help='Download WinSCP')
    parser.add_argument('--webex', action='store_true', help='Download Webex')
    parser.add_argument('--zoom', action='store_true', help='Download Zoom')
    parser.add_argument('--zoomoutlook', action='store_true', help='Download Zoom Outlook Add-in')
    args = parser.parse_args()

    apps = []
    if args.all:
        apps = ['7zip', 'notepad', 'chrome', 'winscp', 'webex', 'zoom', 'zoomoutlook']
    elif args.apps:
        apps = [app.strip() for app in args.apps.split(',')]
    
    # Add individual flags
    if args.__dict__.get('7zip'): apps.append('7zip')
    if args.notepad: apps.append('notepad')
    if args.chrome: apps.append('chrome')
    if args.winscp: apps.append('winscp')
    if args.webex: apps.append('webex')
    if args.zoom: apps.append('zoom')
    if args.zoomoutlook: apps.append('zoomoutlook')
    
    # Remove duplicates
    apps = list(set(apps))

    app_funcs = {
        '7zip': get_7zip_url,
        'notepad': get_notepad_url,
        'chrome': get_chrome_url,
        'winscp': get_winscp_url,
        'webex': get_webex_url,
        'zoom': get_zoom_url,
        'zoomoutlook': get_zoomoutlook_url
    }

    for app in apps:
        if app in app_funcs:
            url_func = app_funcs[app]
            url = url_func()
            if url:
                path = urllib.parse.urlparse(url).path
                if path.endswith('/download'):
                    filename = os.path.basename(path[:-9])
                else:
                    filename = os.path.basename(path)
                
                # Determine version
                if app == 'chrome':
                    version = get_chrome_version()
                elif app in ['webex', 'zoom', 'zoomoutlook']:
                    version = 'latest'
                elif app == '7zip':
                    match = re.search(r'7z(\d+)-x64\.exe', filename)
                    version = f"{match.group(1)[:2]}.{match.group(1)[2:]}" if match else 'unknown'
                elif app == 'notepad':
                    match = re.search(r'npp\.([\d.]+)\.Installer\.x64\.exe', filename)
                    version = match.group(1) if match else 'unknown'
                elif app == 'winscp':
                    match = re.search(r'WinSCP-([\d.]+)-Setup\.exe', filename)
                    version = match.group(1) if match else 'unknown'
                else:
                    version = 'unknown'
                
                folder = os.path.join(app, version)
                os.makedirs(folder, exist_ok=True)
                filepath = os.path.join(folder, filename)
                download_file(url, filepath)
            else:
                logging.warning(f"Skipping {app} due to URL fetch failure")
        else:
            logging.warning(f"Unknown app: {app}")

if __name__ == '__main__':
    main()