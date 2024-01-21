# Use Ubuntu as a parent image
FROM ubuntu:20.04

# Install Python
RUN apt-get update && \
    apt-get install -y python3-pip

# Copy the requirements file into the container at /usr/src/app
COPY dep/python_requirements.txt /dep/python_requirements.txt

# Install Python packages from python_requirements.txt
RUN pip install --no-cache-dir -r /dep/python_requirements.txt

# Install Perl
RUN apt-get install -y perl && \
    rm -rf /var/lib/apt/lists/*

# Install cpanminus and modules
RUN apt-get update && apt-get install -y libmysqlclient-dev && cpan App::cpanminus
RUN cpanm IO::String DBI DBD::mysql
RUN apt-get install -y gcc

# Copy the tar.gz file into the container at /usr/src/app
# Replace 'path/to/your/file.tar.gz' with the actual path to your tar.gz file
COPY dep/RNAhybrid-2.1.2.tar.gz /dep/RNAhybrid/RNAhybrid-2.1.2.tar.gz
WORKDIR /dep/RNAhybrid

# Extract the tar.gz file to /temp and compile/install it
RUN tar -xzvf RNAhybrid-2.1.2.tar.gz --strip-components=1 && \
    ./configure && \
    make && \
    make install && \
    make clean

# Clean up the tar.gz file if it's no longer needed
# Uncomment the following line if you wish to remove the tar.gz file after extraction
 RUN rm /dep/RNAhybrid/RNAhybrid-2.1.2.tar.gz

# Copy the pyscripts directory into the container
COPY src /src

RUN chmod +x /src/*
ENV PATH /src:$PATH

COPY test_data/gene_names_short.txt /test_data/gene_names_short.txt
COPY test_data/sus_names.txt /test_data/sus_names.txt

# Perl & BioPerl dependencies
WORKDIR /dep/perl_dep

RUN mkdir src && cd src
RUN apt install -y git && git clone -b release-1-6-924 --depth 1 https://github.com/bioperl/bioperl-live.git
RUN mv bioperl-live bioperl-1.6.924
RUN git clone https://github.com/Ensembl/ensembl-git-tools.git && \
    export PATH=$PWD/ensembl-git-tools/bin:$PATH && \
    git ensembl --clone api

# Set additional paths for Perl modules
ENV PERL5LIB /dep/perl_dep/bioperl-1.6.924:/dep/perl_dep/ensembl/modules:/dep/perl_dep/ensembl-compara/modules:/dep/perl_dep/ensembl-variation/modules:/dep/perl_dep/ensembl-funcgen/modules:$PERL5LIB

WORKDIR /results

ENTRYPOINT ["python3", "/src/bindseek.py"]