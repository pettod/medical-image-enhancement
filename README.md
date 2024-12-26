# Medical Image Enchancement

## Install

```bash
conda create -n cell python=3.10.16
conda activate cell
conda install pytorch=2.3.1 torchvision
pip install -r requirements.txt
```

## How to run

1. `python backend.py`
1. Open `http://localhost:8080/` in your browser

## See the public IP4 address on Macbook

`ipconfig getifaddr en0`

## Running on AWS

1. Launch EC2 instance
1. Go to the instance
1. Click "Security" tab
1. Open "Inbound rules"
1. Scroll right and click the security group (e.g. launch-wizard-11)
1. Click the group ID
1. Click "Edit inbound rules"
1. HTTP, 80, Anywhere-IPv4 (0.0.0.0/0)
1. Save rules
1. Go to the ubuntu instance
1. Run: `which python`
1. Copy that and run: `sudo path/to/python backend.py --port 80`
