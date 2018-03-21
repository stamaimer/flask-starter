FROM python
WORKDIR /flask-starter
COPY . /flask-starter
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host=pypi.douban.com
EXPOSE 5000
CMD ["/bin/sh", "start_script.sh"]