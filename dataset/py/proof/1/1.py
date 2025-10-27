import time
import torch
import torch.nn as nn
import torch.nn.functional as F

# Minimal mock model
class MockModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 3)
    
    def forward(self, feats):
        return self.linear(feats)


def entity_classify(n_epochs, model, data):
    feats, labels, train_idx, val_idx = data

    print("start training...")
    forward_time = []
    backward_time = []
    for epoch in range(n_epochs):
        t0 = time.time()
        logits = model(feats)
        loss = F.cross_entropy(logits[train_idx], labels[train_idx])
        t1 = time.time()
        loss.backward()
        t2 = time.time()

        forward_time.append(t1 - t0)
        backward_time.append(t2 - t1)
        print("Epoch {:05d} | Train Forward Time(s) {:.4f} | Backward Time(s) {:.4f}".
        format(epoch, forward_time[-1], backward_time[-1]))

        # Line under question in Python 1
        cross_entropy(logits[val_idx], labels[val_idx])
        val_acc = torch.sum(logits[val_idx].argmax(dim=1) == labels[val_idx]).item() / len(val_idx)
        print("Train Accuracy: {:.4f} | Train Loss: {:.4f} | Validation Accuracy: {:.4f} | Validation loss: {:.4f}".
        format(train_acc, loss.item(), val_acc, val_loss.item()))


def entity_classify_f(n_epochs, model, data):
    feats, labels, train_idx, val_idx = data

    print("start training...")
    forward_time = []
    backward_time = []
    for epoch in range(n_epochs):
        t0 = time.time()
        logits = model(feats)
        loss = F.cross_entropy(logits[train_idx], labels[train_idx])
        t1 = time.time()
        loss.backward()
        t2 = time.time()

        forward_time.append(t1 - t0)
        backward_time.append(t2 - t1)
        print("Epoch {:05d} | Train Forward Time(s) {:.4f} | Backward Time(s) {:.4f}".
        format(epoch, forward_time[-1], backward_time[-1]))

        # Line under question in Python 1 (edited to reflect the PR comment)
        F.cross_entropy(logits[val_idx], labels[val_idx])
        val_acc = torch.sum(logits[val_idx].argmax(dim=1) == labels[val_idx]).item() / len(val_idx)
        print("Train Accuracy: {:.4f} | Train Loss: {:.4f} | Validation Accuracy: {:.4f} | Validation loss: {:.4f}".
        format(train_acc, loss.item(), val_acc, val_loss.item()))


model = MockModel()
n_epochs = 10

feats = torch.randn(100, 10)
labels = torch.randint(0, 3, (100,))
train_idx = torch.arange(70)
val_idx = torch.arange(70, 100)

data = [feats, labels, train_idx, val_idx]

entity_classify(n_epochs, model, data)
entity_classify_f(n_epochs, model, data)
