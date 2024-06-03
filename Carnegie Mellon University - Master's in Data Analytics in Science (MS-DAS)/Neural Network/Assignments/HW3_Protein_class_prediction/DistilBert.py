import re
import pickle
import pandas as pd
import numpy as np
import torch
from lightning import LightningDataModule
from lightning import LightningModule
from torch.utils.data import DataLoader
import torchmetrics
from torch import nn
from torch.optim import Adam
from transformers import BertTokenizer, BertForSequenceClassification, AdamW, BertGenerationEncoder
from lightning import Trainer
import pytorch_lightning as pl
import csv
#from datamodule import PAFDatamodule
#from prot_bert import ProteinClassifier
#from transformers import BertTokenizer, BertGenerationEncoder

if torch.cuda.is_available():
    device = torch.device("cuda")
    print("GPU")
else:
    device = torch.device("cpu")
    print("CPU")

class PAFDatamodule(LightningDataModule):
    def __init__(self, root_path, batch_size):
        super().__init__()
        self.batch_size = batch_size
        self.root = root_path
        self.classes = pickle.load(open(f"{root_path}/selected_families.pkl", "rb"))

    def encode_classes(self, y):
        cls2idx = dict(zip(self.classes, range(len(self.classes))))
        return [cls2idx[i] for i in y]

    def get_dataset(self, part, with_target=True):
        file_path = f"{self.root}/{part}_data.csv"
        df = pd.read_csv(file_path)
        x = df.loc[:, "sequence"].values
        if with_target:

            if 'family_id' in df.columns:
                y = df.loc[:, "family_id"].values
                y = torch.tensor(self.encode_classes(y))
                x = list(zip(x, y))
            else:
                x = list(x)
        return x

    def get_unique(self, part, with_target = True):
        file_path = f"{self.root}/{part}_data.csv"
        df = pd.read_csv(file_path)
        if 'family_id' in df.columns:
            xj = df.loc[:, "family_id"].values
            return np.unique(xj)

    def get_names(self, part, with_target=True):
        file_path = f"{self.root}/{part}_data.csv"
        df = pd.read_csv(file_path)
        yz = df.loc[:, "sequence_name"].values
        return yz


    def train_dataloader(self):
        data = self.get_dataset("train")
        return DataLoader(data, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        data = self.get_dataset("val")
        return DataLoader(data, batch_size=self.batch_size, shuffle=False)

    def test_dataloader(self):
        data = self.get_dataset("test")
        return DataLoader(data, batch_size=self.batch_size, shuffle=False)

    def predict_dataloader(self):
        data = self.get_dataset("test")
        return DataLoader(data, batch_size=self.batch_size, shuffle=False)



class ProteinClassifier(pl.LightningModule):
    def __init__(self, n_classes=25):
        super().__init__()
        self.tokenizer = BertTokenizer.from_pretrained("Rostlab/prot_bert", do_lower_case=False)
        self.embedder = BertGenerationEncoder.from_pretrained("Rostlab/prot_bert")
        dmodel = 1024
        self.model = nn.Linear(dmodel, n_classes)

        self.criterion = nn.CrossEntropyLoss()
        self.val_accuracy = torchmetrics.classification.Accuracy(task="multiclass",
                                                                 num_classes=n_classes)
        self.train_accuracy = torchmetrics.classification.Accuracy(task="multiclass",
                                                                   num_classes=n_classes)
        self.val_f1 = torchmetrics.classification.F1Score(task="multiclass", num_classes=n_classes)


    def forward(self, x):
        lengths = torch.tensor([len(i) for i in x]).to(self.device)
        ids = self.tokenizer(x, add_special_tokens=True, padding="longest")
        input_ids = torch.tensor(ids['input_ids']).to(self.device)
        attention_mask = torch.tensor(ids['attention_mask']).to(self.device).to(self.dtype)
        with torch.no_grad():
            embeddings = self.embedder(input_ids=input_ids,
                                   attention_mask=attention_mask).last_hidden_state
        embeddings = embeddings.sum(dim=1)/lengths.view(-1, 1)
        logits = self.model(embeddings)
        return logits

    def training_step(self, batch, batch_idx):
        sequences, labels = batch
        logits = self.forward(sequences)
        loss = self.criterion(logits, labels)
        self.log('train_loss', loss)
        self.train_accuracy(logits, labels)
        return loss

    def validation_step(self, batch, batch_idx):
        '''
        make predictions and calculate validation accuracy/F1 score and save to self.log
        '''
        sequences, labels = batch
        logits = self.forward(sequences)
        loss = self.criterion(logits, labels)
        self.log('val_loss', loss)
        self.val_accuracy(logits, labels)
        self.val_f1(logits, labels)

    def configure_optimizers(self):
        '''
        return optimizer for the model
        '''
        return Adam(self.parameters(), lr=0.001)



if __name__ == "__main__":


# After training the model

# Make predictions on the test dataset
    predictions = []
    sequence_names = []
    batch_size = 128  # Choose your desired batch size
    root_path = "/jet/home/jjung5/NN/Protein_class"
    datamodule = PAFDatamodule(root_path, batch_size)

# Load training data
    train_dataloader = datamodule.train_dataloader()

# Load validation data
    val_dataloader = datamodule.val_dataloader()

# Load test data
    test_dataloader = datamodule.test_dataloader()
    model = ProteinClassifier(n_classes=25)

# Initialize a PyTorch Lightning Trainer
    trainer = pl.Trainer(
    max_epochs=5,
    accelerator='gpu' if torch.cuda.is_available() else 'cpu'  # Use GPU if available
    )

# Perform training
    trainer.fit(model, train_dataloader, val_dataloader)
    #model.eval()
    tokenizer = BertTokenizer.from_pretrained("Rostlab/prot_bert", do_lower_case=False)
    # Make predictions on the test dataset
    predictions = []
    sequence_names = []

    # Iterate over the test dataloader
    for batch in test_dataloader:
        with torch.no_grad():
            logits = model(batch)  # Pass sequences directly to the model
            print(logits)
        predicted_indices = logits.argmax(dim=1).tolist()  # Get the predicted class indices
        predictions.extend(predicted_indices)

# Get sequence names from the dataset
    test_dataset = datamodule.get_names("test")
    sequence_names = test_dataset  # Assuming sequence name is the second item in each data tuple
    test_vals = datamodule.get_unique('train')
    new_predict = []
    for i in predictions:
        new_predict.append(test_vals[i])
# Create DataFrame with sequence names and predicted family IDs
    submission = pd.DataFrame({'sequence_name': sequence_names, 'family_id': new_predict})

# Write the DataFrame to a CSV file
    submission.to_csv('submission.csv', index=False)
# Calculate and print training and validation accuracies
    train_accuracy = model.train_accuracy.compute()
    val_accuracy = model.val_accuracy.compute()

    print(f"Training Accuracy: {train_accuracy}")
    print(f"Validation Accuracy: {val_accuracy}")
