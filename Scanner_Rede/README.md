# 🔍 Network Scanner - Projeto de Segurança

Um scanner de rede simples mas eficiente desenvolvido em Python para análise de hosts e serviços em redes TCP/IP.

## 📋 Funcionalidades

✅ **Ping Sweep** - Descoberta de hosts ativos via ICMP  
✅ **Port Scanning** - Varredura de portas TCP com multi-threading  
✅ **Banner Grabbing** - Identificação de banners de serviços  
✅ **Detecção de Serviços** - Mapeamento automático de portas conhecidas  
✅ **Relatórios HTML** - Geração de relatórios estilizados e profissionais  
✅ **Multiplataforma** - Suporte para Windows, Linux e macOS  

## 🚀 Requisitos

- Python 3.7+
- Bibliotecas padrão (sem dependências externas)
- Permissões de root/administrador para ICMP

## 📦 Instalação

```bash
# Clonar ou baixar o projeto
cd Scanner_Rede

# Executar o script
python network_scanner.py
```

## 💻 Uso

### Execução Interativa

```bash
python network_scanner.py
```

Quando solicitado, insira um intervalo de rede válido:
```
Digite o intervalo de rede válido (ex: 192.168.1.0/24): 192.168.1.0/24
```

### Exemplo de Uso no Código

```python
from network_scanner import NetworkScanner

# Criar instância do scanner
scanner = NetworkScanner("192.168.1.0/24")

# Executar ping sweep
hosts_ativos = scanner.ping_sweep()
print(f"Hosts encontrados: {hosts_ativos}")

# Escanear portas em cada host
portas = [21, 22, 80, 443, 3306, 3389]
for host in hosts_ativos:
    scanner.port_scan(host, portas)

# Gerar relatório
scanner.generate_report()
```

## 🔧 Configuração

### Serviços Suportados

O scanner detecta automaticamente os seguintes serviços:

| Porta | Serviço |
|-------|---------|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 110 | POP3 |
| 143 | IMAP |
| 443 | HTTPS |
| 3306 | MySQL |
| 3389 | RDP |
| 5900 | VNC |
| 6379 | Redis |

Para adicionar mais serviços, edite o método `service_detection()`.

## 📊 Classe Principal: NetworkScanner

### Atributos

```python
self.network_range    # Intervalo de rede (ex: 192.168.1.0/24)
self.active_hosts     # Lista de hosts ativos
self.open_ports       # Dicionário com portas abertas por host
self.banners          # Dicionário com banners dos serviços
```

### Métodos

#### `ping_sweep()`
Realiza varredura ICMP para descobrir hosts ativos.

**Retorno:** Lista de IPs ativos

**Suporte:**
- Windows: `ping -n 1 -w 2000`
- Linux/macOS: `ping -c 1 -W 2`

#### `port_scan(host, ports)`
Escaneia portas abertas e captura banners.

**Parâmetros:**
- `host` (str): Endereço IP do host
- `ports` (list): Lista de portas a escanear

**Retorno:** Lista de portas abertas

#### `service_detection(host, port)`
Identifica o serviço executado em uma porta.

**Parâmetros:**
- `host` (str): Endereço IP
- `port` (int): Número da porta

**Retorno:** Nome do serviço (str)

#### `generate_report()`
Gera um relatório HTML estilizado.

**Arquivo gerado:** `scan_report_YYYYMMDD_HHMMSS.html`

## 🎨 Relatório HTML

O relatório gerado inclui:

- 📊 Resumo de hosts descobertos
- 🖥️ Listagem detalhada de cada host
- 🔌 Portas abertas com serviços identificados
- 🏷️ Banners capturados dos serviços
- ⏰ Data e hora de execução

### Estilos Aplicados

- Cores profissionais (azul, verde, vermelho, roxo)
- Bordas laterais coloridas para diferenciação
- Responsivo e centrado
- Sombras e arredondamentos para melhor visualização

## ⚙️ Detecção de SO

O scanner detecta automaticamente o sistema operacional e ajusta os comandos:

```python
if platform.system().lower() == "windows":
    # Comandos específicos do Windows
elif platform.system().lower() == "linux" or platform.system().lower() == "darwin":
    # Comandos para Linux e macOS
```

## 🔒 Considerações de Segurança

⚠️ **Aviso Legal:** Este scanner é destinado apenas para fins educacionais e testes autorizados.

- Use apenas em redes das quais você tem permissão
- Respeite as leis locais sobre segurança de informação
- Obtenha autorização antes de realizar varreduras
- Não use para fins maliciosos

## 📈 Performance

- **Multi-threading:** Até 100 workers simultâneos
- **Timeout:** 2 segundos por conexão
- **Velocidade:** Varredura de redes inteiras em minutos

## 🐛 Troubleshooting

### Erro: "Permission denied"
```bash
# No Linux/macOS, execute com sudo
sudo python network_scanner.py
```

### Erro: "Invalid network range"
```python
# Formatos válidos:
192.168.1.0/24      # CIDR notation
192.168.1.0/255.255.255.0  # Netmask
```

### Nenhum host descoberto
- Verifique a conectividade com a rede
- Firewall pode estar bloqueando ICMP
- Certifique-se que os hosts estão ligados

## 📚 Estrutura do Código

```
network_scanner.py
├── Imports
├── NetworkScanner (Classe Principal)
│   ├── __init__()
│   ├── ping_sweep()
│   ├── port_scan()
│   ├── service_detection()
│   └── generate_report()
└── __main__ (Execução)
```

## 🔄 Fluxo de Execução

```
1. Entrada de intervalo de rede
   ↓
2. Ping Sweep (Descoberta de hosts)
   ↓
3. Port Scan (Para cada host ativo)
   ↓
4. Banner Grabbing (Captura de informações)
   ↓
5. Geração de Relatório HTML
   ↓
6. Arquivo salvo: scan_report_*.html
```

## 📝 Logs e Saída

O scanner exibe:
- Status de descoberta de hosts
- Mensagem de geração de relatório
- Nome do arquivo HTML gerado

## 🚀 Melhorias Futuras

- [ ] Suporte a varredura UDP
- [ ] Integração com banco de dados
- [ ] API REST para automação
- [ ] Dashboard em tempo real
- [ ] Detectores de vulnerabilidades
- [ ] Integração com ferramentas OSINT

## 👨‍💻 Desenvolvedor

Desenvolvido por: [Caique Emanuel](https://www.linkedin.com/in/caique-emanuel-847684267)
Projeto de Segurança - Network Scanner  
Objetivo: Análise e mapeamento de redes

## 📄 Licença

Este projeto é fornecido para fins educacionais.

---

**Última atualização:** Janeiro de 2026  
**Status:** ✅ Funcional e Testado
