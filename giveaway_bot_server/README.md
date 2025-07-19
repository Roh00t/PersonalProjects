## Deployment

To use this you need to buy a domain. Then add the following DNS records:

I'll assume that you are running this with

- Public ip: 210.210.210.210 (You can find yours here https://whatismyipaddress.com/)
- Localhost ip: 192.168.0.10 (Open a console and write `ip a` or `ifconfig` on mac/linux, and `ipconfig` on windows. It starts with 192.168 and is naer your public ip)
- Domain: example.com

### DNS records
```bash
Type: A
Name: coderhack.net
Content: 1XX.1X.1XX.1XX
TTL: Auto
```

```bash
Type: MX
Name: coderhack.net
Content: coderhack.net
Priority: 10
TTL: Auto
```
### Port forwarding
On whatever computer you are running you will have to make sure your router is port forwarded for the port 25 and routes its traffic to the private ip of where the code will run. If it will run on 192.168.0.10, port forward 192.168.0.10 port 25. If you don't know how to do it your ISP might be blocking you or your router is just bad, there are tons of guides online, even on my channel.

On Router:
```bash
External Port: 25
Internal IP: 192.168.1.53
Internal Port: 25
Protocol: TCP
```
### Testing SMTP Reachability
Test SMTP Reachability (Is your mail bot alive?)

Once you’ve launched main.py, test from the outside world:
💻 From another server or VPS:
```bash
telnet coderhack.net 25
```
RESULT:: 220 coderhack.net ESMTP HarpyMail Ready

### Project Structure

gleam-bot/
├── main.py               # SMTP server + email logger
├── emailgen.py           # Random email generator
├── gleam_entry.py        # Gleam giveaway form submitter
├── parser.py             # Email log scanner for Gleam links
├── requirements.txt      # All Python dependencies
├── Dockerfile            # Docker build config
└── README.md             # This file

### Code changes
In the `handle_RCPT` function, change the domain `coderhack.net` to `example.com` (yours in there)

At the bottom of the script, change the `hostname='192.168.x.x'` 
set it to your own private ipv4 ONLY IF 0.0.0.0 RESULTS IN PORT FORWARDING NOT WORKING 
(Sometimes some operating systems ask that you explicitly use the 192.168 address otherwise port forwarding does not work, like windows)

## Running
### 🧱 Setup Instructions
### 🧰 1. Install Docker
https://docs.docker.com/get-docker/


### 🔨 2. Build the Docker Image
```bash
docker build -t gleam-bot-full .
```

### 🛰 3. Run the Container
```bash
docker run -d -p 25:25 --name gleam_bot gleam-bot-full
```
This:
	• Exposes port 25 to receive email via your domain (e.g., coderhack.net)
	• Launches the SMTP server and logs verification emails into mail_log.txt


### 🧪 4. Test Gleam Entry Automation
Run inside the container or from a script:
```bash
python gleam_entry.py
```
It will:
	•	Generate a random email like gfa0x2s9@coderhack.net
	•	Submit to the Gleam form
	•	Wait for verification email to arrive

## 📦 Python Dependencies:
If running outside Docker:
Run inside the container or from a script:
```bash
pip install -r requirements.txt
```