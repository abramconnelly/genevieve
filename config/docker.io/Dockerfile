FROM ubuntu:14.10

RUN apt-get update && \
  apt-get install -y python-pip rabbitmq-server git wget python-celery build-essential \
    autoconf libtool pkg-config python-opengl python-imaging python-pyrex \
    idle-python2.7 python-dev rabbitmq-server tabix jq && \
  pip install virtualenv virtualenvwrapper

RUN useradd -m genevieve && echo 'genevieve:shakespeare' | chpasswd

RUN su -l genevieve -c " cd /home/genevieve && \
    git clone git://github.com/PersonalGenomesOrg/genevieve && \
    mkdir .virtualenvs && \
    echo 'export WORKON_HOME=/home/genevieve/.virtualenvs' >> .bashrc && \
    echo '. /usr/local/bin/virtualenvwrapper.sh' >> .bashrc && \
    echo 'export WORKON_HOME=/home/genevieve/.virtualenvs' >> .profile && \
    echo '. /usr/local/bin/virtualenvwrapper.sh' >> .profile "

COPY ./settings_local.py /home/genevieve/genevieve/genevieve/settings_local.py

RUN su genevieve -c " cd /home/genevieve/genevieve/external_data_files && \
    wget http://hgdownload-test.cse.ucsc.edu/goldenPath/hg19/bigZips/hg19.2bit && \
    wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz && \
    wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz.tbi "

RUN su -l genevieve bash -c " cd /home/genevieve && \
    mkvirtualenv genevieve && \
    workon genevieve && \
    cd genevieve && \
    pip install -r requirements.txt && \
    python manage.py migrate "

# ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz
# ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz.tbi
#

COPY ./startup_and_persist.sh /root/startup_and_persist.sh

EXPOSE 8000:8000 8080:80 8181:443

CMD [ "/root/startup_and_persist.sh" ]




