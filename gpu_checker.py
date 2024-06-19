import torch

print("PyTorch Version: ", torch.__version__)
print("CUDA Available: ", torch.cuda.is_available())
print("CUDA Version: ", torch.version.cuda)
print("cuDNN Version: ", torch.backends.cudnn.version())
print("Number of GPUs: ", torch.cuda.device_count())
if torch.cuda.is_available():
    print("GPU Name: ", torch.cuda.get_device_name(0))

print(torch.__path__)
import sys
import sys
print(sys.path)
