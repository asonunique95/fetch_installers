# Fetch Installers

A reusable Python script to download the latest installers for 7-Zip, Notepad++, Google Chrome Enterprise, and WinSCP, organized into versioned folders.

## Features

- Downloads the latest versions automatically
- Organizes downloads into `{app}/{version}/` folders
- Supports selecting specific apps or all
- Skips on download failures
- Logs progress and errors
- Extracts Chrome version directly from MSI file properties

## Usage

### Download specific apps (comma-separated)
```bash
python fetch_installers.py --apps 7zip,notepad
```

### Download individual apps
```bash
python fetch_installers.py --7zip --notepad --chrome
```

### Download all apps
```bash
python fetch_installers.py --all
```

## Apps Supported

- **7zip**: Downloads the latest 64-bit Windows exe installer
- **notepad**: Downloads the latest Notepad++ installer exe
- **chrome**: Downloads the latest Google Chrome Enterprise MSI (64-bit)
- **winscp**: Downloads the latest WinSCP setup exe
- **webex**: Downloads the latest Webex MSI
- **zoom**: Downloads the latest Zoom MSI
- **zoomoutlook**: Downloads the latest Zoom Outlook Add-in MSI

## Requirements

- Python 3.x
- Internet connection

## Notes

- Downloads are organized into folders: `{app}/{version}/filename`
- Filenames preserve original names with version numbers
- Versions are parsed from filenames or fetched from APIs (Chrome uses Google version history API)
- For Chrome, uses the standalone enterprise MSI which always provides the latest version