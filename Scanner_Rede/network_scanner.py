import socket
import subprocess
import ipaddress
import platform
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class NetworkScanner():
    def __init__(self, network_range):

        self.network_range = network_range
        self.active_hosts = []
        self.open_ports = {}
        self.banners = {}  
        
    def ping_sweep(self):
        #Varredura ICMP para descobrir hosts ativos
        network = ipaddress.ip_network(self.network_range)

        def check_host(ip):
            try:
                if platform.system().lower() == "windows":
                    subprocess.check_output(['ping', '-n', '1', '-w', '2000', str(ip)], stderr=subprocess.DEVNULL)
                elif platform.system().lower() == "linux" or platform.system().lower() == "darwin":
                    subprocess.check_output(['ping', '-c', '1', '-W', '2', str(ip)], stderr=subprocess.DEVNULL)
                return str(ip)
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=100) as executor:
            results = executor.map(check_host, network.hosts())
        
        self.active_hosts = [ip for ip in results if ip]
        return self.active_hosts
    
    def port_scan(self, host, ports=[21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 5900, 6379]):
        #Varredura de portas TCP + Banner Grabbing
        open_ports = []

        def check_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((host, port))
                
                if result == 0:  
                    banner = ""
                    try:
                        banner = sock.recv(1024).decode().strip()
                    except:
                        banner = "Sem banner"
                    
                    # Armazena o banner
                    if host not in self.banners:
                        self.banners[host] = {}
                    self.banners[host][port] = banner
                    
                    sock.close()
                    return port
                
                sock.close()
                return None
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=100) as executor:
            results = executor.map(check_port, ports)

        open_ports = [port for port in results if port]

        if open_ports:
            self.open_ports[host] = open_ports
        
        return open_ports
    
    def service_detection(self, host, port):
        #Identificação simples de serviços ativos - futuramente, aprimorar com APIs
        services = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            3306: "MySQL",
            3389: "RDP",
            5900: "VNC",
            6379: "Redis"
        }
        return services.get(port, "Serviço Desconhecido")
    
    def generate_report(self):
        #Gera um relátorio simples em HTML
        report = f"""
        <html lang="pt-BR">
        <meta charset="UTF-8">
        <head>
            <title>Relatório de Varredura de Rede - {datetime.now()}</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f5f5f5;
                    color: #333;
                    padding: 20px;
                }}
                
                .container {{
                    max-width: 900px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }}
                
                h2 {{
                    color: #34495e;
                    margin-top: 20px;
                    margin-bottom: 15px;
                }}
                
                .host-info {{
                    background-color: #ecf0f1;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 4px solid #3498db;
                    border-radius: 4px;
                }}
                
                .port-info {{
                    background-color: #f9f9f9;
                    padding: 10px 15px;
                    margin: 8px 0 8px 20px;
                    border-left: 3px solid #2ecc71;
                    border-radius: 3px;
                    font-size: 14px;
                }}
                
                .open-port {{
                    color: #27ae60;
                    font-weight: bold;
                }}
                
                .service {{
                    color: #e74c3c;
                    font-weight: bold;
                }}
                
                .banner {{
                    color: #8e44ad;
                    font-size: 12px;
                    font-style: italic;
                }}
                
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #bdc3c7;
                    text-align: center;
                    color: #7f8c8d;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔍 Relatório de Varredura de Rede</h1>
                <h2>📊 Resumo: {len(self.active_hosts)} Hosts Ativos</h2>
        """
        for host in self.active_hosts:
            report += f'<div class="host-info"><b>🖥️ Host:</b> <span class="open-port">{host}</span>'
            if host in self.open_ports:
                for port in self.open_ports[host]:
                    service = self.service_detection(host, port)
                    banner = self.banners.get(host, {}).get(port, "Sem banner")
                    # Limita banner a 50 caracteres para melhor visualização
                    banner_truncado = banner[:50] + "..." if len(banner) > 50 else banner
                    report += f'<div class="port-info">🔌 <span class="open-port">Porta {port}</span> - <span class="service">{service}</span> - <span class="banner">Banner: {banner_truncado}</span></div>'
                report += '</div>'
        
        report += f"""
                <div class="footer">
                    <p>Relatório gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
                    <p>Scanner de Rede - Projetos de Segurança</p>
                </div>
            </div>
        </body>
        </html>
        """

        with open(f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html", "w", encoding='utf-8') as f:
            f.write(report)
        return report

if __name__ == "__main__":
    scanner = NetworkScanner(input("Digite o intervalo de rede válido (ex: 192.168.1.0/24): "))

    active_hosts = scanner.ping_sweep()

    for host in active_hosts[:5]:
        scanner.port_scan(host)
    print("Gerando relatório...")
    time.sleep(1)
    print("Verifique o arquivo HTML gerado para os resultados detalhados.")

    scanner.generate_report()