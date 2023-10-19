import torch
import torch.nn as nn

class CNN_Transformer(nn.Module):
    def __init__(self):
        super(CNN_Transformer, self).__init__()

        self.cap_linear_layer = nn.Linear(1, 512)
        self.final_linear_layer = nn.Linear(512, 1)

        self.conv_layer = nn.Conv1d(3, 512, kernel_size=16, stride=8)
        self.encoder_layer = nn.TransformerEncoderLayer(d_model=512, nhead=8, batch_first=True)
        self.decoder_layer = nn.TransformerDecoderLayer(d_model=512, nhead=8, batch_first=True)

    def forward(self, my_data, capacity):
        my_data = my_data.permute(0, 2, 1)
        embedded_data = self.conv_layer(my_data)
        embedded_data = embedded_data.permute(0, 2, 1)
        encoded_data = self.encoder_layer(embedded_data)

        tgt = self.cap_linear_layer(capacity)
        tgt = tgt.unsqueeze(1)
        decoded_data = self.decoder_layer(tgt, encoded_data)
        decoded_data = decoded_data.squeeze(1)
        output_cap = self.final_linear_layer(decoded_data)
        return output_cap
    

class GRU_CNN(nn.Module):
    def __init__(self):
        super(GRU_CNN, self).__init__()

        self.conv_block = nn.Sequential(
            nn.Conv1d(3, 64, kernel_size=32, padding='same'),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, padding="same"),
            
            nn.Conv1d(64, 64, kernel_size=32, padding='same'),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, padding="same"),
            
            nn.Conv1d(64, 64, kernel_size=32, padding='same'),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, padding="same"),
            
            nn.Conv1d(64, 64, kernel_size=32, padding='same'),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, padding="same"),
            
            nn.Conv1d(64, 64, kernel_size=32, padding='same'),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, padding="same"),
            
            nn.Conv1d(64, 64, kernel_size=32, padding='same'),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, padding="same")
        )

        self.flatten = nn.Flatten()
        self.dense1 = nn.Linear(64, 64)

        self.gru = nn.GRU(3, 256, batch_first=True)
        self.dense2 = nn.Linear(256, 64)

        self.concat = nn.Linear(128, 1)

    def forward(self, input_stream):
        x1 = self.conv_block(input_stream)
        x1 = self.flatten(x1)
        x1 = self.dense1(x1)

        _, x2 = self.gru(input_stream)
        x2 = x2.squeeze(0)
        x2 = self.dense2(x2)

        combined = torch.cat((x1, x2), dim=1)
        output = self.concat(combined)

        return output