Windows DHCP Helper/Relay Migration Script
======
Designed to migrate/consolidate Windows DHCP Scopes and changing Cisco L3
devices settings (Switches/Routers) for IP Helper/DHCP Relay

Install
=======

```
git clone https://github.com/ekiojp/dhcp-relay-cisco
cd dhcp-relay-cisco
pip install -r requirements.txt
```

Usage
=======
- File: example-dhcp-dump.txt (DHCP dump after processed by script cleaner.py)
- File: common.py (functions used across the scripts)

## Steps
1) If you have more than 1 Windows DHCP, aggregate them using:
```
cat dhcp-server1-dump dhcp-server2-dump > master-dump
```

2) Run cleaner.py to remove duplicate and disabled scopes (also remove classes
and other data from the original Microsoft DHCP dumps)
```
./cleaner.py master-dump clean-master-dump
```

3) Use validator.py to generate a CSV file that validate the scope doing below:
- Ping the default gateway (DHCP OPTION 3)
- If successful, try telnet/ssh using up to 2 user/pass (tacacs) and 2 user/pass/enable
  (local accounts)
- Check if Cisco device use ip-helper or dhcp relay format, grab prompt,
  interface and peer hsrp prompt/IP if exist
- The program will a thread per device to speed up this
```
./validator.py clean-master-dump scopes.csv
```

4) There 2 utilities, grabber.py and pushing.py, the first will just make a
backup of current ip-helper/dhcp relay settings on each device using the CSV
file.
The second tool (pushing.py), delete any ip-helper/dhcp relay current settings
and configure new values
```
./grabber.py scopes.csv
```

