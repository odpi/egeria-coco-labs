# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.

# This build script corrects some permission issues needed to run
# on some enterprise k8s environments. see https://github.com/odpi/egeria-jupyter-notebooks/issues/9

# The published image tag is taken from the numerical version of
# our base image, and appended with the contents of .tag-append (file)
FROM quay.io/jupyter/minimal-notebook

#COPY ../config_coco_core.py /config_coco.py
#RUN chmod +x /config_coco.py

RUN pip install --no-cache-dir 'pyegeria>=0.7.35'
RUN pip install --no-cache-dir 'rich'

#    && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}" \

#ENTRYPOINT ["jupyter","notebook"]
#
#CMD ["python3", "/config_coco_core.py"]
#USER root

# Needed to dynamically add the selected user on startup - see link below
#RUN chmod g+w /etc/passwd
#
#RUN chown -R $NB_UID:$NB_GID $HOME
#
## https://cloud.redhat.com/blog/jupyter-on-openshift-part-6-running-as-an-assigned-user-id
#RUN chgrp -Rf root /home/$NB_USER && chmod -Rf g+w /home/$NB_USER && chgrp -Rf root /opt/conda && chmod -Rf g+w /opt/conda
#
#USER 1000
