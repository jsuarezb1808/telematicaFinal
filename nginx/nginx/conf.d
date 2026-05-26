upstream backend_servers {
    server 172.31.20.220:5000;
    server 172.31.24.225:5000;
}

server {
    listen 80;
    server_name proyectotelematica-kenia.duckdns.org;

    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name proyectotelematica-kenia.duckdns.org;

    ssl_certificate /etc/letsencrypt/live/proyectotelematica-kenia.duckdns.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/proyectotelematica-kenia.duckdns.org/privkey.pem;

    location / {
        proxy_pass http://backend_servers;

        proxy_http_version 1.0;
        proxy_set_header Connection close;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        add_header X-Backend $upstream_addr always;
    }
}