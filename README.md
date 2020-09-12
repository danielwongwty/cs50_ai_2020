# Summary of the Configuring Process

## Starting point

I start by using the same model as handwriting.py shown in the lecture, but
just change the `input_shape` (`IMG_HEIGHT`, `IMG_WIDTH`, 3) and number of
neuron for the output layer (`NUM_CATEGORIES`) according to the requirement of
our classification problem. I get about 6% accuracy after running a training of
10 epochs.

## Testing

Then I change the following config one by one. And the efficiency are shown as
below:

### Number of Neuron in Fully-Connected Layer

| Number of Neuron | Accuracy at Last Epoch | Time/step at Last Epoch |
|:----------------:|:----------------------:|:-----------------------:|
| 128              | 0.0576                 | 3s 6ms                  |
| 256              | 0.6794                 | 3s 6ms                  |
| 512              | 0.8995                 | 4s 8ms                  |
| 1024             | 0.9180                 | 5s 10ms                 |

### Number of Neuron in Convolutional Layer

| Number of Neuron | Accuracy at Last Epoch | Time/step at Last Epoch |
|:----------------:|:----------------------:|:-----------------------:|
| 8                | 0.0576                 | 2s 4ms                  |
| 16               | 0.0576                 | 2s 5ms                  |
| 32               | 0.0576                 | 3s 6ms                  |
| 64               | 0.0576                 | 4s 8ms                  |
| 128              | 0.0566                 | 6s 12ms                 |

### Number of Fully-Connected Layer

| Number of Layer  | Accuracy at Last Epoch | Time/step at Last Epoch |
|:----------------:|:----------------------:|:-----------------------:|
| 1                | 0.0576                 | 3s 6ms                  |
| 2                | 0.0532                 | 3s 6ms                  |
| 3                | 0.0554                 | 3s 6ms                  |

### Number of Convolutional Layer

| Number of Layer  | Accuracy at Last Epoch | Time/step at Last Epoch |
|:----------------:|:----------------------:|:-----------------------:|
| 1                | 0.0576                 | 3s 6ms                  |
| 2                | 0.8969                 | 3s 6ms                  |
| 3                | 0.8922                 | 3s 6ms                  |

## Configuring

According to the above stat, I mix the above settings to get a satisfying
configuration (accuracy > 90%). Here is the summary:

- Convolutional Layer 1 (64 filters, 3 x 3 kernal)
- Max-Pooling (2 x 2)
- Convolutional Layer 2 (64 filters, 3 x 3 kernal)
- Max-Pooling (2 x 2)
- Flatterning
- Fully-connected layer (size: 256)
- Dropout (size: 0.5)
- Output layer (size: 43)
