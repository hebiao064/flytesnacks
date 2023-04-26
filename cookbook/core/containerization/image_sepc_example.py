"""
.. _image_spec_example:

Building Image without Dockerfile
---------------------------------

.. tags:: Containerization, Intermediate

Image Spec is a way to specify how to build a container image without a Dockerfile. The image spec by default will be
converted to an `Envd <https://envd.tensorchord.ai/>`__ config, and the `Envd builder
<https://github.com/flyteorg/flytekit/blob/master/plugins/flytekit-envd/flytekitplugins/envd/image_builder.py#L12-L34
>`__ will build the image for you. However, you can also register your own builder to build the image using other tools.

For every :py:class:`flytekit.PythonFunctionTask` task or a task decorated with the ``@task`` decorator,
you can specify rules for binding container images. By default, flytekit binds a single container image, i.e.,
the `default Docker image <https://ghcr.io/flyteorg/flytekit>`__, to all tasks. To modify this behavior,
use the ``container_image`` parameter available in the :py:func:`flytekit.task` decorator, and pass an
:py:class:`flytekit.image_spec.ImageSpec` object.

 Flytekit will build the image before registering the workflow, and replace the image name in the workflow spec with
 the newly built image name.

.. note::
    If the Docker image is not available publicly, refer to :ref:`Pulling Private Images<private_images>`.
"""

from flytekit import task, workflow
from flytekit.image_spec.image_spec import ImageSpec
import pandas as pd


# %%
# Image Spec
# ==========
#
# People can specify python packages, apt packages, and environment variables. Those packages will be added on top of
# the `default image <https://github.com/flyteorg/flytekit/blob/master/Dockerfile>`__.
image_spec = ImageSpec(packages=["pandas", "numpy"],
                       python_version="3.9",
                       apt_packages=["git"],
                       env={"Debug": "True"},
                       registry="pingsutw")


# %%
# Both t1 and t2 will use the image built from the image spec.
@task(image_spec=image_spec)
def t1():
    df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})
    print(df)


@task(image_spec=image_spec)
def t2():
    print("hello")


# %%
# t3 don't specify image_spec, so it will use the default image.
# You can also pass imageSpec yaml file to the ``pyflyte run`` or ``pyflyte register`` command to override it.
# For instance:
#
# .. yaml::
#   python_version: 3.11
#   packages:
#     - pandas
#     - numpy
#   apt_packages:
#     - git
#   env:
#     Debug: "True"
#
#
# .. code-block::
#
#   pyflyte run --remote --image image.yaml image_spec_example.py wf
@task()
def t3():
    print("flyte")


@workflow()
def wf():
    t1()
    t2()
    t3()


if __name__ == '__main__':
    wf()

