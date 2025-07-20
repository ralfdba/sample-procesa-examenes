# sample-procesa-examenes
Procesa y crea recomendaciones medicas en formato *.docx

## Prerequisites
Before you begin, ensure you have the following installed on your Debian 12 system:
  * **Python 3**: Debian 12 (Bookworm) comes with Python 3 pre-installed.
  * **`python3-venv`**: This package is essential for creating isolated Python environments.

## Installation
Follow these steps to set up your project locally.
### 1\. Update System Packages
It's a good practice to update your system's package list first:
```bash
sudo apt update
sudo apt upgrade
```
### 2\. Install `python3-venv`
If you don't have it already, install the `python3-venv` package:
```bash
sudo apt install python3-venv
```
### 3\. Clone the Repository (or create your project directory)
If you're cloning this repository, use:
```bash
git clone https://github.com/ralfdba/sample-procesa-examenes
cd sample-procesa-examenes
```
If you're starting a new project, simply create a directory:
```bash
mkdir my_python_project
cd my_python_project
```
### 4\. Create a Virtual Environment
Create a virtual environment to manage project dependencies separately:
```bash
python3 -m venv venv
```
### 5\. Activate the Virtual Environment
Activate your newly created virtual environment:
```bash
source venv/bin/activate
```
Your terminal prompt should change to `(venv)` indicating the environment is active.
### 6\. Install Project Dependencies
With the virtual environment active, install the required Python libraries:
```bash
pip install PyMuPDF python-docx reportlab
```
## Usage
To run the main script:
```bash
python main.py
```
## Contributing
Feel free to fork this repository, make improvements, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.
