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
from torch.optim import AdamW
from transformers import BertTokenizer, BertModel
from lightning import Trainer
import pytorch_lightning as pl
import csv
from transformers import DistilBertModel, DistilBertTokenizer
from transformers import DistilBertForSequenceClassification


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
        return DataLoader(data, batch_size=self.batch_size, shuffle=True, num_workers = 4)

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
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        self.model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=n_classes)

        self.criterion = nn.CrossEntropyLoss()
        self.val_accuracy = torchmetrics.classification.Accuracy(task="multiclass",
                                                                 num_classes=n_classes)
        self.train_accuracy = torchmetrics.classification.Accuracy(task="multiclass",
                                                                   num_classes=n_classes)
        self.val_f1 = torchmetrics.classification.F1Score(task="multiclass", num_classes=n_classes)


    def forward(self, input_ids, attention_mask):
        outputs = self.model(input_ids=input_ids.to(self.device), attention_mask=attention_mask.to(self.device))
        #logits = outputs.logits
        return outputs

    def training_step(self, batch, batch_idx):
        sequences, labels = batch
        inputs = self.tokenizer(sequences, padding=True, truncation=True, return_tensors="pt")
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']
        outputs = self.forward(input_ids, attention_mask)
        logits = outputs.logits
        loss = self.criterion(logits, labels)
        self.log('train_loss', loss)
        self.train_accuracy(logits, labels)
        return loss

    def validation_step(self, batch, batch_idx):
        sequences, labels = batch
        inputs = self.tokenizer(sequences, padding=True, truncation=True, return_tensors="pt")
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']
        outputs = self.forward(input_ids, attention_mask)
        logits = outputs.logits
        loss = self.criterion(logits, labels)
        self.log('val_loss', loss)
        self.val_accuracy(logits, labels)
        self.val_f1(logits, labels)

    def configure_optimizers(self):
        '''
        return optimizer for the model
        '''
        return AdamW(self.parameters(), lr=2e-5)

if __name__ == "__main__":


# After training the model

# Make predictions on the test dataset
    batch_size = 128
    root_path = "/jet/home/jjung5/NN/Protein_class"
    datamodule = PAFDatamodule(root_path, batch_size)
    family_id_mapping = pickle.load(open(f"{root_path}/selected_families.pkl", "rb"))
    # Load test data
    test_dataloader = datamodule.test_dataloader()

    # Load model
    model = ProteinClassifier(n_classes=25)
    model = model.to(device)  # Move model to appropriate device

    # Initialize a PyTorch Lightning Trainer
    trainer = pl.Trainer(max_epochs=5, accelerator='gpu' if torch.cuda.is_available() else 'cpu')

    # Perform training
    trainer.fit(model, datamodule.train_dataloader(), datamodule.val_dataloader())

    # Set model to evaluation mode
    model.eval()

    predictions = []
    sequence_names = []

    # Iterate over the test dataloader
    for batch in test_dataloader:
        sequences = batch  # Unpack the batch without labels
        with torch.no_grad():
        # Tokenize sequences
            inputs = model.tokenizer(sequences, padding=True, truncation=True, return_tensors="pt")
            inputs = {k: v.to(device) for k, v in inputs.items()}

        # Forward pass
            logits = model(**inputs).logits

    # Get predicted class indices
        predicted_indices = logits.argmax(dim=1).tolist()
        predicted_family_ids = [family_id_mapping[i] for i in predicted_indices]
        predictions.extend(predicted_family_ids)

    # Get sequence names from the dataset
    sequence_names = datamodule.get_names("test")

    # Create DataFrame with sequence names and predicted family IDs
    submission = pd.DataFrame({'sequence_name': sequence_names, 'family_id': predictions})

    # Write the DataFrame to a CSV file
    submission.to_csv('submission.csv', index=False)
    train_accuracy = model.train_accuracy.compute()
    val_accuracy = model.val_accuracy.compute()

    print(f"Training Accuracy: {train_accuracy}")
    print(f"Validation Accuracy: {val_accuracy}")
