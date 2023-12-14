FROM public.ecr.aws/lambda/python:3.8

# Prepare dev tools
RUN yum -y update
RUN yum -y install wget libstdc++ autoconf automake libtool autoconf-archive pkg-config gcc gcc-c++ make libjpeg-devel libpng-devel libtiff-devel zlib-devel
RUN yum group install -y "Development Tools"

# Download leptonica and tesseact into /opt
WORKDIR /opt
RUN wget http://www.leptonica.org/source/leptonica-1.82.0.tar.gz && tar -zxvf leptonica-1.82.0.tar.gz
RUN wget https://github.com/tesseract-ocr/tesseract/archive/refs/tags/5.2.0.tar.gz && tar -zxvf 5.2.0.tar.gz
RUN rm -rf leptonica-1.82.0.tar.gz && rm -rf 5.2.0.tar.gz

# Build leptonica
WORKDIR /opt/leptonica-1.82.0
RUN ./configure && make -j && make install

# Build tesseract
WORKDIR /opt/tesseract-5.2.0
RUN ./autogen.sh
RUN PKG_CONFIG_PATH=/usr/local/lib/pkgconfig LIBLEPT_HEADERSDIR=/usr/local/include ./configure --with-extra-includes=/usr/local/include --with-extra-libraries=/usr/local/lib
RUN LDFLAGS="-L/usr/local/lib" CFLAGS="-I/usr/local/include" make -j && make install && /sbin/ldconfig

# Remove build src code
WORKDIR /opt
RUN rm -rf leptonica-1.82.0 && rm -rf tesseract-5.2.0

# Optional: install language packs
RUN wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata
RUN mv *.traineddata /usr/local/share/tessdata

ARG GIT_ACCESS_TOKEN

WORKDIR /app

COPY app.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt .
RUN pip3 install -r requirements.txt  --target "${LAMBDA_TASK_ROOT}"

CMD [ "app.handler" ]