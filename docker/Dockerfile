
# https://docs.docker.com/engine/reference/builder/#automatic-platform-args-in-the-global-scope
ARG BUILDPLATFORM=linux/amd64
ARG PY_VER=3.9

FROM --platform=${BUILDPLATFORM} jupyter/minimal-notebook:python-${PY_VER}

ENV JUPYTER_ENABLE_LAB=yes

USER root

# system packages
RUN apt-get update -y && \
    apt-get install -y curl gnupg

# General jupyter deps

RUN mamba install -y -n base -c conda-forge \
    nb_conda_kernels \
 && mamba clean -a -f -y \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "/home/${NB_USER}"

USER ${NB_UID}

# Config for nb_conda_kernels

RUN printf '\n\
{ \n\
  "CondaKernelSpecManager": { \n\
    "kernelspec_path": "--user" \n\
  } \n\
} \n\
' > $(jupyter --config-dir)/jupyter_config.json

# Conda environment for RCT components

RUN mamba create -y -n rct \
    python=${PY_VER} \
    ipykernel \
    radical.pilot \
    radical.entk

# Tutorials

WORKDIR /tutorials/
COPY --chown=${NB_UID}:${NB_GID} ./ ./

