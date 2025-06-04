## Color Nodes

This repository contains a lightweight collection of colour adjustment nodes
for ComfyUI.  They operate on images expressed as nested Python lists of
``(R, G, B)`` tuples.  The implementation avoids third-party dependencies so the
nodes run in restricted environments.  For full functionality you should
install the dependencies listed in ``requirements.txt`` which enables use of
packages such as Pillow.
