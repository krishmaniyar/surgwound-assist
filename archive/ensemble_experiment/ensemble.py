import torch
import torch.nn as nn
from scipy.optimize import minimize
from sklearn.metrics import f1_score
import numpy as np

class EnsemblePredictor:
    def __init__(self, models, class_mappings):
        """
        models: dict of {'model_name': model_instance}
        """
        self.models = models
        self.attributes = list(class_mappings.keys())
        self.weights = {attr: np.ones(len(models)) / len(models) for attr in self.attributes}
        
    def predict_probs(self, inputs):
        """
        inputs: dict of {'model_name': input_tensor}
        Returns: dict of {attribute: prob_tensor}
        """
        model_names = list(self.models.keys())
        
        all_probs = {attr: [] for attr in self.attributes}
        
        for name in model_names:
            model = self.models[name]
            inp = inputs[name]
            
            with torch.no_grad():
                outputs = model(inp)
                
            # For MLPs, output is already logits for a specific attribute, but since this is an ensemble,
            # wait, MLPs are per attribute. So models is actually a nested dict:
            # {'dinov2': {'location': model, ...}, 'clip': {...}, 'cnn': cnn_model}
            
            if name == 'cnn':
                for attr in self.attributes:
                    probs = torch.softmax(outputs[attr], dim=1).cpu().numpy()
                    all_probs[attr].append(probs)
            else:
                for attr in self.attributes:
                    attr_model = self.models[name][attr]
                    outputs = attr_model(inp)
                    probs = torch.softmax(outputs, dim=1).cpu().numpy()
                    all_probs[attr].append(probs)
                    
        ensemble_probs = {}
        for attr in self.attributes:
            stacked_probs = np.stack(all_probs[attr], axis=0) # (num_models, batch_size, num_classes)
            w = self.weights[attr].reshape(-1, 1, 1)
            weighted_probs = np.sum(stacked_probs * w, axis=0)
            ensemble_probs[attr] = weighted_probs
            
        return ensemble_probs

def optimize_weights(val_probs_dict, val_targets_dict, attributes, model_names):
    """
    Finds optimal ensemble weights per attribute on the validation set to maximize Macro-F1.
    val_probs_dict[attr][model_name] = (N, C) numpy array
    val_targets_dict[attr] = (N,) numpy array
    """
    optimized_weights = {}
    
    for attr in attributes:
        print(f"Optimizing ensemble weights for {attr}...")
        targets = val_targets_dict[attr]
        
        # Stack probabilities from different models
        # Shape: (num_models, N, C)
        stacked_probs = np.stack([val_probs_dict[attr][name] for name in model_names], axis=0)
        
        def loss_func(w):
            w = w / np.sum(w) # Normalize
            w_reshaped = w.reshape(-1, 1, 1)
            weighted_probs = np.sum(stacked_probs * w_reshaped, axis=0)
            preds = np.argmax(weighted_probs, axis=1)
            # Minimize negative Macro-F1
            return -f1_score(targets, preds, average='macro', zero_division=0)
            
        initial_w = np.ones(len(model_names)) / len(model_names)
        bounds = [(0, 1) for _ in range(len(model_names))]
        constraints = ({'type': 'eq', 'fun': lambda w: 1 - sum(w)})
        
        result = minimize(loss_func, initial_w, bounds=bounds, constraints=constraints, method='SLSQP')
        optimized_w = result.x / np.sum(result.x)
        optimized_weights[attr] = optimized_w
        
        print(f"Optimal weights for {attr}: {dict(zip(model_names, optimized_w))}")
        print(f"Best Ensemble Macro-F1: {-result.fun:.4f}")
        
    return optimized_weights
