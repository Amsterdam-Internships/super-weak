import torch

def init_device():
  if torch.cuda.is_available():
    device = torch.device("cuda")
    print("There are %d GPU(s) available." % torch.cuda.device_count())
    print("Using GPU: ", torch.cuda.get_device_name(0))

  else:
    print("No GPU available, using CPU instead.")
    device = torch.device("cpu")