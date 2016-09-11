FROM tiangolo/uwsgi-nginx
COPY diagnosticui/nginx.conf /etc/nginx/conf.d/nginx.conf
COPY diagnosticui/wwwroot /wwwroot
COPY services /services
COPY services_stubs /services_stubs
COPY services/run_services.sh /services/run_services.sh
COPY services/run_services.sh /services_stubs/run_services.sh
WORKDIR /services_stubs
RUN pip install flask flask-cors
CMD ./run_services.sh
