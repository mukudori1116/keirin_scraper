FROM conda/miniconda3-centos7

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# CMD ["scrapy", "crawl", "Webspider", "-s", "JOBDIR=crawls/somespider-1"]
