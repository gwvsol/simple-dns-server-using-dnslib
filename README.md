## Simple DNS server using dnslib

Простой dns сервер с возможностью блокировки интернет ресурсов

***
### Краткое описание
DNS сервер использует библиотеку [dnslib](https://github.com/paulchakravarti/dnslib "GitHub")
Для настройки используется файл ```dns.conf```.

Файл имеет вид:
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
##### Описание параметров файла настройки

```ext_dns```   - IP адрес внешнего DNS сервера куда передаются запросы
 
```ext_port```  - порт внешнего DNS сервера

```loc_dns```   - локальный IP адрес для DNS запросов

```loc_port```  - локальный порт для DNS запросов

```bloc```      - перечень ресурсов, на которые будет дан ответ "ERR_NAME_NOT_RESOLVED"

```resolv```    - ресурсы находящиеся в локальной сети для которых будет выполнено 
                  разрешение имен на уровне этого DNS сервера
                  
> Примечание: при использовании ```docker``` парамерт ```loc_dns``` должен
> быть ```"0.0.0.0"```, кроме этого в коде необходимо сделать изменения
> строку
> ```#local_dns = conf['loc_dns']``` необходимо раскомментировать, а следующей за ней строку закоментировать
> ```local_dns = '0.0.0.0'```

##### Запуск сервиса в Docker

Создание образа Docker
```bash
git clone https://github.com/gwvsol/Simple-DNS-server-using-dnslib.git
cd Simple-DNS-server-using-dnslib/
docker build -t dns-proxy:latest .
```
Далее необходимо указать в файле ```dns.conf``` ресурсы к которым необходимо ограничить 
доступ из локальной сети

Запуск контейнера
```bash
docker run --name dns-proxy -p your_ip:53:53/udp -v $(pwd):/var/dns-proxy --rm -td dns-proxy:latest
```
