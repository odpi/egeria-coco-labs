# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.

# This build script corrects some permission issues needed to run
# on some enterprise k8s environments. see https://github.com/odpi/egeria-jupyter-notebooks/issues/9

# TODO: Move to later version
FROM docker.io/jupyter/base-notebook:2022-05-23

USER root

RUN chown -R $NB_UID:$NB_GID $HOME

# https://cloud.redhat.com/blog/jupyter-on-openshift-part-6-running-as-an-assigned-user-id
RUN chgrp -Rf root /home/$NB_USER && chmod -Rf g+w /home/$NB_USER

USER 1000
