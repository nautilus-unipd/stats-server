# Statistics server

Simple webserver to view images and logs from a remote server.

## Setup Guide

1. Clone the repository and enter the folder `stats-server`:
 ```bash
git clone git@github.com:nautilus-unipd/stats-server.git
cd stats-server
 ```
2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```bash 
pip install -r requirements.txt
```

4. Run the server:
```bash
flask run
```


---
## TODO
- [ ] Implement the log viewer
- [ ] Improve usability 
- [ ] Expand this TODO list
