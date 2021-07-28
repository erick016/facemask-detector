# Running this project

These demo steps assume that you are using a Windows 10 machine. 
Demo link: https://youtu.be/gGyDyFNz2hM
Complete code repository: https://github.com/erick016/facemask-detector 
Our code isolated for reading purposes (only what we wrote): https://github.com/JackWang071/CS688-Facemask-Detection
These are the steps to set up the run environment, with the correct dependencies, for the demo:
Use Windows PowerShell to git clone the uTensor Helloworld and Create-Face-Data-from-Images repos
Download the Real-Time-Medical-Mask-Detection dataset in Github
Extract Real-Time-Medical-Mask-Detection directly inside the root directory of uTensor Helloworld
Move poll_and_send.py to Create-Face-Data-from-Images root directory
Replace default uTensor main.cpp with custom main_original.cpp file
Move mask_conv.ipynb to root directory of uTensor Helloworld, this notebook takes a custom image set as input
Install Anaconda 3, November 2020 version
Open Anaconda Powershell in administrator mode
Create new Python 3.6.8 environment, run: 
conda create -n myenv python=3.6.8 --no-default-packages
conda activate myenv
Use pip to install the following dependencies:
pip install mbed-cli
pip install utensor-cgen jupyterlab
pip install -Iv pyelftools==0.25
pip install -Iv protobuf==3.11.3
pip install -Iv opencv-python==4.5.1.48
pip install -Iv pyserial==3.5
pip install -Iv pillow==8.0.1
pip install -Iv tensorflow==2.1.0
Open mask_conv.ipynb using Jupyter Notebook, 
jupyter notebook mask_conv.ipynb
Go to Kernel in the main menu, restart and run all cells to build the neural network using the MaskedFace-Net dataset images. This should generate a my_model.cpp file inside the uTensor directory. Press Ctrl+C on the Anaconda Powershell to exit.
Before compiling, run this command:
pip install mbed-greentea
This will make sure the board changes the led from red to green when it finishes compiling
Unfortunately, the video doesn’t show this and was only caught after the recording. It did not affect the outcome but will explain why the led stays red after compiling. I tested it myself and it worked the same before and after installing mbed-greentea
To compile and install the neural network into the ST board, run this command: 
mbed deploy (only necessary the first time)
mbed compile -m auto -t GCC_ARM -f

Check the PATH environment variable, make sure that the folder containing the GCC_ARM binary is there. Use the following command in case it is not:
mbed config -G GCC_ARM_PATH "C:\Program Files (x86)\GNU Tools ARM Embedded\6 2017-q2-update\bin"
