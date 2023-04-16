# Route tools & configurations
## Non-cn-routes
Autorun [dndx/nchnroutes](https://github.com/dndx/nchnroutes) on github workflow

API powered by cloudflare workers

update configs by api like
```bash
0 2 * * * curl -s https://api.9-ch.com/ncr?device=tun0  -o /etc/bird/routes4.conf
0 2 * * * curl -s https://api.9-ch.com/ncr?mode=6&device=tun0  -o /etc/bird/routes6.conf
```

api params:

    mode: 
        - 4 : ipv4(default)
        - 6 : ipv6
    device: 
        - eth0 : (default)
        - [string] : device name
# CN-ASN
```
#./asn_cn.py -h
usage: asn_cn.py [-h] [-o <file>] [-s [{apnic,he,ipip} ...]] [-v]

Generate China ASN list for BIRD.

optional arguments:
  -h, --help            show this help message and exit
  -o, --output <file>   write to file(default: asn_cn.conf)
  -s, --source [{apnic,he,ipip} ...]
                        multiple sources can be used at the same time (default: apnic he ipip)
  -v, --version         show program's version number and exit
```
