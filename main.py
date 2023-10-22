import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from tqdm import tqdm
import yaml
from sklearn.model_selection import train_test_split

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from model import CNN_Transformer
from dataset import load_NASA, BatteryDataset

# Load the YAML configuration file
with open('config.yaml', 'r') as file:
    cfg = yaml.safe_load(file)

# # Access the variables
NUM_CYCLES = cfg['NUM_CYCLES']
FEATURE_DIM = cfg['NUM_CYCLES']
EPOCHS = cfg['EPOCHS']
LEARNING_RATE = cfg['LEARNING_RATE']
BATCH_SIZE = cfg['BATCH_SIZE']

# Load data
battery_dict = load_NASA(folder='NASA_DATA', scale_data=True)
dataset = BatteryDataset(battery_dict, num_cycles=NUM_CYCLES)
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# NN model
model = CNN_Transformer(feature_dim=FEATURE_DIM, num_cycles=NUM_CYCLES)

# Loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Training loop
model.train()
for epoch in tqdm(range(EPOCHS)):    
    for inputs, outputs in dataloader:
        # Convert inputs and outputs to PyTorch tensors
        inputs = inputs.float()
        outputs = outputs.float()

        # Zero the gradients
        optimizer.zero_grad()

        # Forward pass
        predicted_outputs = model(inputs, outputs[:,:-1])

        # Compute the loss
        loss = criterion(predicted_outputs, outputs[:,-1].unsqueeze(-1))

        # Backward pass
        loss.backward()

        # Update the weights
        optimizer.step()

    # Print the loss for monitoring after each epoch
    print(f"Epoch [{epoch+1}/{EPOCHS}], Loss: {loss.item()}")

# After the training loop, you can save the trained model if needed
torch.save(model.state_dict(), 'trained_model.pth')