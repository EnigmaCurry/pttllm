# Monkey-patch torch.load to use weights_only=True
import torch
original_torch_load = torch.load
def patched_torch_load(*args, **kwargs):
    kwargs['weights_only'] = kwargs.get('weights_only', True)
    return original_torch_load(*args, **kwargs)
torch.load = patched_torch_load


# Without this patch, you get this warning:
# FutureWarning: You are using torch.load with weights_only=False (the
# current default value), which uses the default pickle module
# implicitly. It is possible to construct malicious pickle data which
# will execute arbitrary code during unpickling (See
# https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models
# for more details). In a future release, the default value for weights_only will be flipped to True. This limits the functions that could be executed during unpickling. Arbitrary objects will no longer be allowed to be loaded via this mode unless they are explicitly allowlisted by the user via torch.serialization.add_safe_globals. We recommend you start setting weights_only=True for any use case where you don't have full control of the loaded file. Please open an issue on GitHub for any issues related to this experimental feature.
