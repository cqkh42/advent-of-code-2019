FROM jupyter/minimal-notebook:63d0df23b673
USER root
RUN apt-get update && apt-get install openssh-server -y
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
USER jovyan
WORKDIR /work
RUN mkdir -p ~/.jupyter/lab/user-settings/@jupyterlab/apputils-extension
RUN echo '{"theme": "JupyterLab Dark"}' > ~/.jupyter/lab/user-settings/@jupyterlab/apputils-extension/themes.jupyterlab-settings
