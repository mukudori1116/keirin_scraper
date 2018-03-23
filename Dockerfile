FROM conda/miniconda3-centos7

RUN yum -y upgrade
RUN yum -y reinstall glibc-common
RUN yum groupinstall -y "Development Tools"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# CMD ["scrapy", "crawl", "Webspider", "-s", "JOBDIR=crawls/somespider-1"]
