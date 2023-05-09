import Graphs
import tensorflow as tf

print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

#### Run an episode ###
Graphs.run_cycles()