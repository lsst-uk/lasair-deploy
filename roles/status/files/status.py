import os
import requests
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def now():
    return datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S %Z")


def test_up(url):
    status = {}
    try:
        response = requests.get(url, verify=False)
        status['detail'] = "status code: {}".format(response.status_code)
        if response.status_code == 200:
            status['value'] = "Up"
        else:
            status['value'] = "Error"
    except requests.exceptions.RequestException as e:
        status['detail'] = e.args[0]
        status['value'] = "Down"
    status['time'] = now()
    return status


def get_motd():
    motd = {
        "text": "No messages to display.",
        "time" : "-"
        }
    try:
        with open("motd.txt") as f:
            motd['text'] = f.read()
            mtime = os.stat("motd.txt").st_mtime
            motd['time'] = datetime.fromtimestamp(mtime, timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S %Z")
    except IOError:
        pass
    return motd


def print_html_doc(context):
    # Create the jinja2 environment.
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True,
                         autoescape=select_autoescape())
    print (j2_env.get_template('status.html').render(context))


if __name__ == '__main__':
    context = {
        "motd": get_motd(),
        # these should be IP addresses so they don't change if we redirect the DNS
        "ztf_status": test_up('https://192.41.122.132/'),
        "lsst_status": test_up('https://lasair-lsst.lsst.ac.uk/'),
    }
    print_html_doc(context)

