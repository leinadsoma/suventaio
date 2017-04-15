upstream suventaio_server {
  server unix:/webapps/suventaio/run/gunicorn.sock fail_timeout=0;
}
server {
    listen   80;
    server_name suventa.zaresapp.com www.suventa.zaresapp.com paraisopay.zaresapp.com www.paraisopay.zaresapp.com;
    client_max_body_size 4G;
    access_log /webapps/suventaio/logs/nginx-access.log;
    error_log /webapps/suventaio/logs/nginx-error.log;
    location /static/ {
        alias   /webapps/suventaio/static/;
    }
    location /media/ {
        alias   /webapps/suventaio/media/;
    }
    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://suventaio_server;
            break;
        }
    }
    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root /webapps/suventaio/static/;
    }
}