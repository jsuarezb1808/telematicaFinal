# Temporary config used only for the initial Let's Encrypt challenge.
# Replace this file with your full SSL config after the certificate is issued.

upstream backend_servers {
    server 172.31.20.220:5000;
    server 172.31.24.225:5000;
}

server {
    listen 80;
    server_name proyectotelematica-kenia.duckdns.org;

    # Let's Encrypt ACME challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Temporarily serve HTTP while we don't have a cert yet.
    # After the cert is issued, replace this file with the SSL config.
    location / {
        proxy_pass http://backend_servers;
    }
}