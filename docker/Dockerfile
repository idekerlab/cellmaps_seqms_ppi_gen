# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

RUN apt-get --allow-releaseinfo-change update
RUN apt-get install -y build-essential 

RUN mkdir /tmp/cellmaps_seqms_ppi_gen
COPY ./ /tmp/cellmaps_seqms_ppi_gen/
RUN pip install /tmp/cellmaps_seqms_ppi_gen

RUN rm -rf /tmp/cellmaps_seqms_ppi_gen

ENTRYPOINT ["/opt/conda/bin/cellmaps_seqms_ppi_gencmd.py"]

CMD ["--help"]
