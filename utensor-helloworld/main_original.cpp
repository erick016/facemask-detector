#include <stdio.h>

#include <cmath>

#include "input_image.h"  //contains the first sample taken from the MNIST test set
#include "mbed.h"
#include "models/my_model/my_model.hpp"  //gernerated model file"
#include "uTensor.h"


using namespace uTensor;

static mbed::UnbufferedSerial serial_port(USBTX, USBRX);

FileHandle *mbed::mbed_override_console(int fd)
{
    return &serial_port;
}

int argmax(const Tensor &logits) {
  uint32_t num_elems = logits->num_elems();
  float max_value = static_cast<float>(logits(0));
  int max_index = 0;
  for (int i = 1; i < num_elems; ++i) {
    float value = static_cast<float>(logits(i));
    if (value >= max_value) {
      max_value = value;
      max_index = i;
    }
  }
  return max_index;
}

static My_model model;

int char_to_hex(char c)
{
  if ( c >= 'a' && c <= 'f') { return (c - 97) + 10; }
  else if ( c >= '0' && c <= '9') { return c - 48; }
  else { return 0;}
}

  char new_input_image[1568];

  float new_input_image_flt[784];

int main(void) {

  while(1)
  {

  for (int j = 0; j < 1568; j++)
  {
    //printf("%d\r\n", j);
    new_input_image[j] = '0';
  }

  for (int k = 0; k < 784; k++)
  {
    //printf("%d\r\n", k);
    new_input_image_flt[k] = 0.0;
  }

  /*printf("Simple MNIST end-to-end uTensor cli example (device)\n");

  printf("Enter in 1,568 hex values (784 pairs ranging from 0 to 255) for a 28*28 grayscale image.");*/

  for (int l = 0; l < 1568; l++)
  {
    serial_port.read(new_input_image+l,1);
  }

  printf("<%s>\r\n", new_input_image);

  for (int i = 0; i < 784; i++)
  {
    new_input_image_flt[i] =  float((16 * char_to_hex(new_input_image[(i * 2)]) + char_to_hex(new_input_image[(i * 2) + 1])))/255;
    //printf("%d\r\n", int(new_input_image_flt[i] * 255));
  }

  // create the input/output tensor
  Tensor input_image = new RomTensor({1, 28, 28, 1}, flt, new_input_image_flt);
  Tensor logits = new RamTensor({1, 2}, flt);

  model.set_inputs({{My_model::input_0, input_image}})
      .set_outputs({{My_model::output_0, logits}})
      .eval();

  int max_index = argmax(logits);
  input_image.free();
  logits.free();

  if (max_index == 0)
  {
    printf("pred label: masked \r\n");
  }

  else
  {
    printf("pred label: unmasked \r\n");
  }

}

  return 0;
}
