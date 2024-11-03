import dns.resolver

def fetch_dns_records(domain, dns_servers):
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
    dns_records = {}

    for server in dns_servers:
        print(f"\nChecking DNS records for {domain} using server {server}:")
        
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [server]  # Set the DNS server to the current location's server
        
        for record_type in record_types:
            try:
                answers = resolver.resolve(domain, record_type)
                dns_records[record_type] = [str(answer) for answer in answers]
            except dns.resolver.NoAnswer:
                dns_records[record_type] = 'No record found'
            except dns.resolver.NXDOMAIN:
                dns_records[record_type] = 'Domain does not exist'
                break
            except dns.resolver.NoNameservers:
                dns_records[record_type] = 'No name servers found'
                break
            except Exception as e:
                dns_records[record_type] = f'Error: {e}'

        # Display the results for this server
        for record_type, record_values in dns_records.items():
            print(f"{record_type} Records:")
            if isinstance(record_values, list):
                for value in record_values:
                    print(f"  {value}")
            else:
                print(f"  {record_values}")
            print()

# Comprehensive list of global DNS servers from various locations
dns_servers = [
    # Google Public DNS - Global
    "8.8.8.8", "8.8.4.4",
    
    # Cloudflare DNS - Global
    "1.1.1.1", "1.0.0.1",
    
    # Quad9 - Switzerland
    "9.9.9.9", "149.112.112.112",
    
    # OpenDNS - United States
    "208.67.222.222", "208.67.220.220",
    
    # Comodo Secure DNS - United States
    "8.26.56.26", "8.20.247.20",
    
    # Yandex DNS - Russia
    "77.88.8.8", "77.88.8.1",
    
    # Neustar DNS - Global
    "156.154.70.1", "156.154.71.1",
    
    # CleanBrowsing DNS - United States
    "185.228.168.9", "185.228.169.9",
    
    # FreeDNS - Austria
    "37.235.1.174", "37.235.1.177",
    
    # SafeDNS - Netherlands
    "195.46.39.39", "195.46.39.40",
    
    # Norton ConnectSafe - United States (may require a subscription)
    "199.85.126.10", "199.85.127.10",
    
    # DNS.Watch - Germany
    "84.200.69.80", "84.200.70.40",
    
    # OpenNIC - Japan
    "202.83.95.227", "193.183.98.154",
    
    # Alternate DNS - United States
    "76.76.19.19", "76.223.122.150",
    
    # AdGuard DNS - Global
    "94.140.14.14", "94.140.15.15",
    
    # Dyn DNS - United States (owned by Oracle)
    "216.146.35.35", "216.146.36.36",
    
    # Level3 DNS - United States
    "4.2.2.1", "4.2.2.2", "4.2.2.3", "4.2.2.4",
    
    # Hurricane Electric - United States
    "74.82.42.42",
    
    # SmartViper DNS - Russia
    "208.76.50.50", "208.76.51.51",
    
    # Public-Root DNS - Various locations
    "199.5.157.131", "208.71.35.137",
    
    # Baidu DNS - China
    "180.76.76.76",
    
    # AliDNS - China
    "223.5.5.5", "223.6.6.6",
    
    # Quad101 - Taiwan
    "101.101.101.101", "101.102.103.104",
]

# Specify the domain to query
domain = "fashionmodel.me"
fetch_dns_records(domain, dns_servers)
