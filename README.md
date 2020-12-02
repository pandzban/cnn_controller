# cnn_controller
Project of controller managing convolutional neural network layer computations in high level HDL. 

Layer has fixed number of outputs, dependent on the size of input matrix.
The input, output and filter are 2D mapped memories, meaning that they are addressed by columns and rows, as seen on a raster image.
Dimensions are being set by python parameters on top of the .py file.
The output dimensions are given by formula:
 OUTPUT_DIM = INPUT_DIM - FILTER_DIM + 1, as often seen in convolution operation.
Project uses only positive fixed-point arithmetic due to me not having enough time for implementing negative values operations.
The stride parameter is equal 1 and zero padding is not used in this implementation.
Input and output values can be accessed by word, with use of req and valid signals.

The top schematic can be seen below:
![mass statistics of network learning](https://i.postimg.cc/0y80YDcw/schematic.png)

There is posted the generated Verilog file aswell.

It was done as project for my university course called "Digital design using high level Hardware Description Languages".
I used MyHDL package for Python, allowing me to use more abstract functional and structural description of my module.
