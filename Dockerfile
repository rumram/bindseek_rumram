# Use Ubuntu as a parent image
FROM ubuntu:20.04

# Install Python
RUN apt-get update && \
    apt-get install -y python3.7 python3-pip

# Set the working directory in the container
WORKDIR /usr/src/app

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
COPY dep/RNAhybrid-2.1.2.tar.gz /dep/RNAhybrid-2.1.2.tar.gz

# Change directory to /temp (create if it doesn't exist)
WORKDIR /dep

# Extract the tar.gz file to /temp and compile/install it
RUN tar -xzvf RNAhybrid-2.1.2.tar.gz --strip-components=1 && \
    ./configure && \
    make && \
    make install && \
    make clean

# Clean up the tar.gz file if it's no longer needed
# Uncomment the following line if you wish to remove the tar.gz file after extraction
# RUN rm RNAhybrid-2.1.2.tar.gz

# Add /usr/src/pyscripts to PATH
ENV PATH="/usr/src/pyscripts:${PATH}"

# Copy the pyscripts directory into the container
# Replace 'path/to/your/pyscripts' with the actual path to your pyscripts directory
COPY src /src

COPY test_data/gene_names_short.txt /test_data/gene_names_short.txt
COPY test_data/sus_names.txt /test_data/sus_names.txt

# Ensembl and Perl
WORKDIR /dep/perl_dep

RUN mkdir src && cd src
RUN apt install -y git && git clone -b release-1-6-924 --depth 1 https://github.com/bioperl/bioperl-live.git
RUN mv bioperl-live bioperl-1.6.924
RUN git clone https://github.com/Ensembl/ensembl-git-tools.git && \
    export PATH=$PWD/ensembl-git-tools/bin:$PATH && \
    git ensembl --clone api

# Set environment variables
#ENV PERL5LIB ${PERL5LIB}:/usr/src/bioperl-1.6.924:/usr/src/ensembl/modules:/usr/src/ensembl-compara/modules:/usr/src/ensembl-variation/modules:/usr/src/ensembl-funcgen/modules
# Set additional paths for executables
ENV PATH /dep/perl_dep/src/bioperl-1.6.924:/dep/perl_dep/ensembl/modules:/dep/perl_dep/ensembl-compara/modules:/dep/perl_dep/ensembl-variation/modules:/dep/perl_dep/ensembl-funcgen/modules:$PATH

# Set additional paths for Perl modules
ENV PERL5LIB /dep/perl_dep/bioperl-1.6.924:/dep/perl_dep/ensembl/modules:/dep/perl_dep/ensembl-compara/modules:/dep/perl_dep/ensembl-variation/modules:/dep/perl_dep/ensembl-funcgen/modules:$PERL5LIB

WORKDIR /results

# Export the PERL5LIB variable
#RUN echo 'export PERL5LIB' >> /root/.bashrc


# Run app.py when the container launches
# Replace 'app.py' with the script you want to run
# CMD ["python", "app.py"]
#CMD ["python3.7", "/usr/src/pyscripts/workflow.py", "--genes_file", "gene_names_short.txt", "--species_file", "sus_names.txt", "--motif", "UCCCUGAG", "--rnahybrid_param", "3utr_human", "--mirna_sequence", "UCCCUGAGACCCUAACUUGUGA"]
