# ev3host setup

### Summary

ev3host is the python script which listens to connections from ev3swarm. It can be setup to run as a service, or you can run it from the command line to see any debug output.  At some point, I will make a pre-configured disk image available. Barring that, here is how to setup ev3host. If you know your Linux, just make `setup.sh` executable and run it as root on your ev3dev install. Otherwise, keep reading.

### Setting up ev3dev

1. Download and flash [ev3dev](http://www.ev3dev.org/) to a MicroSD card.
2. Insert the MicroSD card into your ev3 unit, power it up. You should see the
ev3dev logo. It will take a long time for its first boot.
3. Insert your USB Wi-Fi adapter, use the on-screen menu to power it up, connect to your network.
4. From your computer, make sure that you can ssh to your ev3. The IP address should be listed at the top of the screen. The default username is `robot`. The password is `maker`. For example, if you are using the terminal on OSX or Linux and the ev3 ip address is 192.168.0.2, you would type the command `ssh robot@192.168.0.102` and enter `maker` when prompted for a password.

### Setting up ev3host

1. Secure copy these files to the ev3host.
	- If you are a Windows user, you can try [WinSCP](https://winscp.net/eng/download.php). 
	- If you are at an OSX or Linux terminal, navigate to where you downloaded this repository and type `scp -r ev3host robot@192.168.0.102:`
2. SSH in to your ev3
3. Navigate to the ev3host directory you just copied over: `cd ev3host`
4. Make `setup.sh` executable: `chmod +x setup.sh`
5. Run it as root: `sudo ./setup.sh` (and enter the password `maker` when prompted)
6. The install script will download any necessary files and configure the ev3host service