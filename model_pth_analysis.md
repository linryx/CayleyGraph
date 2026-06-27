# model.pth Analysis
*Generated: 2026-06-19*

## File Location
`transformer/Summer_2026/workspace/_scratch/model.pth`

## What's Inside

It's a `HookedTransformer` (TransformerLens) checkpoint with these top-level keys:

| Key | Content |
|---|---|
| `config` | Model hyperparameters |
| `model` | Final weights (state dict) |
| `optimizer` / `scheduler` | Training state |
| `checkpoints` | Periodic weight snapshots |
| `checkpoint_epochs` | Epochs at each snapshot (every 100, up to 25,000) |
| `train_losses` / `test_losses` | Full loss history |
| `train_accuracies` / `test_accuracies` | Full accuracy history |

## Model Architecture (`config`)

- **1 layer**, **4 attention heads**, `d_model=256`, `d_head=64`, `d_mlp=256`
- **Bidirectional attention**, no layer norm (`normalization_type=None`)
- `d_vocab=5` (input tokens), `d_vocab_out=2` (binary classification)
- Context length: 22 tokens
- Activation: ReLU
- Positional embedding: standard
- Seed: 999
- Total parameters: 393,216

## Model Weight Tensors

| Tensor | Shape |
|---|---|
| `embed.W_E` | `[5, 256]` |
| `pos_embed.W_pos` | `[22, 256]` |
| `blocks.0.attn.W_Q` | `[4, 256, 64]` |
| `blocks.0.attn.W_K` | `[4, 256, 64]` |
| `blocks.0.attn.W_V` | `[4, 256, 64]` |
| `blocks.0.attn.W_O` | `[4, 64, 256]` |
| `blocks.0.attn.b_Q` | `[4, 64]` |
| `blocks.0.attn.b_K` | `[4, 64]` |
| `blocks.0.attn.b_V` | `[4, 64]` |
| `blocks.0.attn.b_O` | `[256]` |
| `blocks.0.attn.mask` | `[22, 22]` |
| `blocks.0.attn.IGNORE` | `[]` |
| `blocks.0.mlp.W_in` | `[256, 256]` |
| `blocks.0.mlp.b_in` | `[256]` |
| `blocks.0.mlp.W_out` | `[256, 256]` |
| `blocks.0.mlp.b_out` | `[256]` |
| `unembed.W_U` | `[256, 2]` |
| `unembed.b_U` | `[2]` |

## Training Results

| Metric | Start | End | Best |
|---|---|---|---|
| Train loss | 0.6983 | 0.5497 | — |
| Test loss | 0.6982 | 0.5839 | — |
| Train accuracy | 50.0% | 71.3% | 71.4% |
| Test accuracy | 50.0% | 68.8% | 68.9% |

- Trained for 25,000 epochs; checkpoints saved every 100 epochs
- ~2.5% train/test accuracy gap suggests mild overfitting

## How to Load

```python
import sys, types, torch
import transformer_lens

# Shim needed because checkpoint was saved with an older TransformerLens version
shim = types.ModuleType('transformer_lens.HookedTransformerConfig')
shim.HookedTransformerConfig = transformer_lens.HookedTransformerConfig
sys.modules['transformer_lens.HookedTransformerConfig'] = shim

checkpoint = torch.load('workspace/_scratch/model.pth', map_location='cpu', weights_only=False)

config    = checkpoint['config']
weights   = checkpoint['model']
train_acc = checkpoint['train_accuracies']
test_acc  = checkpoint['test_accuracies']
```

## Potential Next Steps

1. **Plot training curves** — full 25,000-epoch history; look for phase transitions
2. **Run inference** — reconstruct model from `config` + `model` weights and run new inputs
3. **Mechanistic interpretability** — use TransformerLens hooks for attention patterns, QK/OV circuits, logit lens
4. **Analyze weight matrices** — SVD of `W_E`, attention circuit analysis (`W_Q @ W_K^T`), unembedding `W_U`
5. **Compare to Summer 2025 checkpoint** — `transformer/Summer_2025/workspace/_scratch/model.pth`
