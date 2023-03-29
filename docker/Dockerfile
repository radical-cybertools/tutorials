
# https://docs.docker.com/engine/reference/builder/#automatic-platform-args-in-the-global-scope
ARG BUILDPLATFORM=linux/amd64
ARG PY_VER=3.9

FROM --platform=${BUILDPLATFORM} jupyter/minimal-notebook:python-${PY_VER}

ENV JUPYTER_ENABLE_LAB=yes

USER root

# system packages
RUN apt-get update  -y && \
    apt-get install -y curl gnupg sudo

# add user to sudoers
RUN adduser ${NB_USER} sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/no_pass

# general jupyter deps
RUN mamba install -y -n base -c conda-forge \
    nb_conda_kernels \
 && mamba clean -a -f -y \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "/home/${NB_USER}"

USER ${NB_UID}

# config for nb_conda_kernels
RUN printf '\n\
{ \n\
  "CondaKernelSpecManager": { \n\
    "kernelspec_path": "--user" \n\
  } \n\
} \n\
' > $(jupyter --config-dir)/jupyter_config.json

ARG TUTORIAL_NAME=default
ENV RADICAL_PILOT_DBURL=mongodb://guest:guest@mongodb:27017/default

# conda environment for RCT components
RUN mamba create -y -n rct \
    python=${PY_VER} \
    ipykernel \
    radical.pilot \
    radical.entk \
    radical.analytics

# tutorials
WORKDIR /tutorials/
COPY --chown=${NB_UID}:${NB_GID} ./${TUTORIAL_NAME} ./

RUN if [[ -f ./setup.sh ]] ; then \
       bash setup.sh && rm setup.sh ; \
    fi

RUN if [[ -f ./environment.yml ]] ; then \
       mamba env update -n rct -f ./environment.yml && rm environment.yml ; \
    fi

