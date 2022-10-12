FROM public.ecr.aws/lambda/python:3.8

# Prepare dev tools
RUN yum -y update
RUN yum -y install wget libstdc++ autoconf automake libtool autoconf-archive pkg-config gcc gcc-c++ make libjpeg-devel libpng-devel libtiff-devel zlib-devel
RUN yum group install -y "Development Tools"

# Build leptonica
WORKDIR /opt
RUN wget http://www.leptonica.org/source/leptonica-1.82.0.tar.gz
RUN ls -la
RUN tar -zxvf leptonica-1.82.0.tar.gz
WORKDIR ./leptonica-1.82.0
RUN ./configure
RUN make -j
RUN make install
RUN cd .. && rm leptonica-1.82.0.tar.gz

# Build tesseract
RUN wget https://github.com/tesseract-ocr/tesseract/archive/refs/tags/5.2.0.tar.gz
RUN tar -zxvf 5.2.0.tar.gz
WORKDIR ./tesseract-5.2.0
RUN ./autogen.sh
RUN PKG_CONFIG_PATH=/usr/local/lib/pkgconfig LIBLEPT_HEADERSDIR=/usr/local/include ./configure --with-extra-includes=/usr/local/include --with-extra-libraries=/usr/local/lib
RUN LDFLAGS="-L/usr/local/lib" CFLAGS="-I/usr/local/include" make -j
RUN make install
RUN /sbin/ldconfig
RUN cd .. && rm 5.2.0.tar.gz

# Optional: install language packs
RUN wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata
RUN mv *.traineddata /usr/local/share/tessdata

ARG GIT_ACCESS_TOKEN

WORKDIR /app

COPY app.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt .
RUN pip3 install -r requirements.txt  --target "${LAMBDA_TASK_ROOT}"

CMD [ "app.handler" ]