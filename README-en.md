## Simple DNS server using dnslib

Simple dns server with the ability to block Internet resources

***
### Description
The DNS server uses the library [dnslib](https://github.com/paulchakravarti/dnslib "GitHub")
The file is used for configuration ```dns.conf```.

The file ```dns.conf```:
```json
{
    "ext_dns": "8.8.8.8",
    "ext_port": 53,
    "loc_dns": "0.0.0.0",
    "loc_port": 53,
    "bloc": ["mail.ru", "yandex.com", "yandex.by"],
    "resolv": {
        "flask.loc": "192.168.1.30",
        "uwsgi.loc": "192.168.1.30"
    }
}
```
##### Description of configuration file options

```ext_dns```   - IP address of external DNS server where requests are sent
 
```ext_port```  - external DNS server port

```loc_dns```   - локальный IP адрес для DNS запросов

```loc_port```  - local IP address for DNS queries

```bloc```      - list of resources to which the answer will be given "ERR_NAME_NOT_RESOLVED"

```resolv```    - resources on the local network for which name resolving will be performed at the level of this DNS server
                  
> Note: if you use ```docker``` option ```loc_dns``` should
> be ```"0.0.0.0"```, except that the code should make changes
> сto line
> ```#local_dns = conf['loc_dns']``` uncomment, the following line comment out
> ```local_dns = '0.0.0.0'```


##### The launch of the service in Docker

Create a Docker image
```bash
git clone https://github.com/gwvsol/Simple-DNS-server-using-dnslib.git
cd Simple-DNS-server-using-dnslib/
docker build -t dns-proxy:latest .
```
Next, you must specify the file ```dns.conf``` resources to which you want to limit 
access from the local network

Starting the container
```bash
docker run --name dns-proxy -p 192.168.1.30:53:53/udp -v $(pwd):/var/dns-proxy --rm -td dns-proxy:latest
```
