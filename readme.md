Autorun [dndx/nchnroutes](https://github.com/dndx/nchnroutes) on github workflow

API powered by cloudflare workers

update configs by api like
```bash
0 2 * * * curl -s https://api.xn--7ovq92diups1e.com/ncr?device=tun0  -o /etc/bird/routes4.conf
0 2 * * * curl -s https://api.xn--7ovq92diups1e.com/ncr?mode=6&device=tun0  -o /etc/bird/routes6.conf
```

api params:

    mode: 
        - 4 : ipv4(default)
        - 6 : ipv6
    device: 
        - eth0 : (default)
        - [string] : device name