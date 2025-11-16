"""
BERT4Rec - BERT for Sequential Recommendation
Models user viewing history as sequences
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class PositionalEncoding(nn.Module):
    """Positional encoding for sequences"""
    
    def __init__(self, d_model: int, max_len: int = 512, dropout: float = 0.1):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)
        
        # Create positional encoding matrix
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        """Add positional encoding"""
        x = x + self.pe[:, :x.size(1)]
        return self.dropout(x)


class BERT4Rec(nn.Module):
    """
    BERT4Rec model for sequential recommendations
    Uses masked language modeling on user sequences
    """
    
    def __init__(
        self,
        num_items: int,
        hidden_size: int = 256,
        num_layers: int = 2,
        num_heads: int = 4,
        dropout: float = 0.1,
        max_seq_length: int = 50
    ):
        super(BERT4Rec, self).__init__()
        
        self.num_items = num_items
        self.hidden_size = hidden_size
        self.max_seq_length = max_seq_length
        
        # Item embedding (add 2 for mask and padding tokens)
        self.item_embedding = nn.Embedding(num_items + 2, hidden_size, padding_idx=0)
        
        # Positional encoding
        self.pos_encoding = PositionalEncoding(hidden_size, max_seq_length, dropout)
        
        # Transformer encoder layers
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_size,
            nhead=num_heads,
            dim_feedforward=hidden_size * 4,
            dropout=dropout,
            activation='gelu',
            batch_first=True
        )
        
        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers
        )
        
        # Output layer
        self.output_layer = nn.Linear(hidden_size, num_items)
        
        # Layer normalization
        self.layer_norm = nn.LayerNorm(hidden_size)
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        """Initialize weights"""
        nn.init.xavier_uniform_(self.item_embedding.weight)
        nn.init.xavier_uniform_(self.output_layer.weight)
        nn.init.zeros_(self.output_layer.bias)
    
    def forward(self, input_ids, attention_mask=None):
        """
        Forward pass
        
        Args:
            input_ids: Sequence of item IDs [batch_size, seq_len]
            attention_mask: Attention mask [batch_size, seq_len]
        
        Returns:
            Logits for next item prediction [batch_size, seq_len, num_items]
        """
        # Embed items
        embeddings = self.item_embedding(input_ids)
        
        # Add positional encoding
        embeddings = self.pos_encoding(embeddings)
        
        # Layer normalization
        embeddings = self.layer_norm(embeddings)
        
        # Create attention mask for transformer
        if attention_mask is None:
            attention_mask = (input_ids != 0).float()
        
        # Invert mask for transformer (0 = attend, 1 = ignore)
        transformer_mask = (attention_mask == 0)
        
        # Pass through transformer
        output = self.transformer_encoder(
            embeddings,
            src_key_padding_mask=transformer_mask
        )
        
        # Project to item space
        logits = self.output_layer(output)
        
        return logits
    
    def predict(self, sequence, top_k=10, exclude_items=None):
        """
        Predict next items given a sequence
        
        Args:
            sequence: List of item IDs
            top_k: Number of recommendations
            exclude_items: Set of items to exclude
        
        Returns:
            List of (item_id, score) tuples
        """
        self.eval()
        
        with torch.no_grad():
            # Prepare input
            if len(sequence) > self.max_seq_length:
                sequence = sequence[-self.max_seq_length:]
            
            input_ids = torch.tensor([sequence], dtype=torch.long)
            
            # Get predictions
            logits = self.forward(input_ids)
            
            # Get predictions for last position
            last_logits = logits[0, -1, :]
            
            # Exclude items
            if exclude_items:
                last_logits[list(exclude_items)] = float('-inf')
            
            # Get top-K
            scores = F.softmax(last_logits, dim=0)
            top_scores, top_indices = torch.topk(scores, k=top_k)
            
            recommendations = [
                (int(idx), float(score))
                for idx, score in zip(top_indices, top_scores)
            ]
            
            return recommendations
    
    def recommend_for_user(self, user_sequence, top_k=10, exclude_items=None):
        """
        Get recommendations based on user's watching history
        
        Args:
            user_sequence: List of anime IDs user has watched (chronological)
            top_k: Number of recommendations
            exclude_items: Set of anime IDs to exclude
        
        Returns:
            List of recommendations
        """
        return self.predict(user_sequence, top_k, exclude_items)


class BERT4RecTrainer:
    """Trainer for BERT4Rec model"""
    
    def __init__(
        self,
        model: BERT4Rec,
        learning_rate: float = 0.001,
        mask_prob: float = 0.15,
        device: str = 'cuda'
    ):
        self.model = model.to(device)
        self.device = device
        self.mask_prob = mask_prob
        
        self.optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        self.criterion = nn.CrossEntropyLoss(ignore_index=0)
    
    def mask_sequence(self, sequence):
        """
        Apply random masking to sequence for training
        
        Args:
            sequence: Original sequence
        
        Returns:
            masked_sequence, target_sequence
        """
        masked_seq = sequence.clone()
        targets = sequence.clone()
        
        # Create mask (don't mask padding)
        mask = torch.rand(sequence.shape) < self.mask_prob
        mask = mask & (sequence != 0)
        
        # Apply mask token (num_items + 1)
        masked_seq[mask] = self.model.num_items + 1
        
        # Only compute loss on masked positions
        targets[~mask] = 0
        
        return masked_seq, targets
    
    def train_step(self, sequences):
        """Single training step"""
        self.model.train()
        self.optimizer.zero_grad()
        
        # Mask sequences
        masked_seqs, targets = self.mask_sequence(sequences)
        
        # Forward pass
        logits = self.model(masked_seqs)
        
        # Compute loss
        loss = self.criterion(
            logits.view(-1, self.model.num_items),
            targets.view(-1)
        )
        
        # Backward pass
        loss.backward()
        self.optimizer.step()
        
        return loss.item()
