
# https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html
ARG REGISTRY=quay.io
ARG OWNER=jupyter
# https://quay.io/repository/jupyter/minimal-notebook?tab=tags
ARG IMAGE_TAG=python-3.11
# https://docs.docker.com/engine/reference/builder/#automatic-platform-args-in-the-global-scope
ARG BUILDPLATFORM=linux/amd64

FROM --platform=${BUILDPLATFORM} ${REGISTRY}/${OWNER}/minimal-notebook:${IMAGE_TAG}

ARG TUTORIAL_NAME=default

ENV JUPYTER_ENABLE_LAB=yes
ENV JUPYTER_SERVERAPP_LOG_LEVEL=40
ENV JUPYTER_DISABLE_FILE_VALIDATION=1
ENV MAMBA_ROOT_PREFIX=${CONDA_DIR}

USER root

# system packages
RUN apt-get update  -y && \
    apt-get install -y build-essential curl gnupg jq sudo

# add user to sudoers
RUN adduser ${NB_USER} sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/no_pass

# config kernel(s)
RUN conda update -n base -y mamba libmamba libmambapy \
 && mamba update -n base -y -c conda-forge conda \
 && mamba clean -a -f -y \
 && printf '#!/bin/bash \n\
\n\
eval "$(mamba shell.posix hook)" \n\
exec "$@" \n\
' > "${CONDA_DIR}/bin/kernelstart.sh" \
 && chmod +x "${CONDA_DIR}/bin/kernelstart.sh" \
 && sed -i 's/\[/\[\"kernelstart.sh\",/g' \
    "${CONDA_DIR}/share/jupyter/kernels/python3/kernel.json" \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "/home/${NB_USER}"

USER ${NB_UID}

# install RCT components
RUN eval "$(mamba shell.posix hook)" \
 && pip install radical.pilot radical.entk radical.analytics \
 && pip install radical.asyncflow

# tutorials
WORKDIR /tutorials/
COPY --chown=${NB_UID}:${NB_GID} ./${TUTORIAL_NAME} ./

RUN if [[ -f ./setup.sh ]] ; then \
       bash setup.sh && rm setup.sh ; \
    fi

RUN if [[ -f ./environment.yml ]] ; then \
       mamba env update -n base -f ./environment.yml && rm environment.yml ; \
    fi

