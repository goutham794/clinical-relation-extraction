SWEEP_CONFIGS = {
    "NER" : {
        "mbert" : {
            'method': 'bayes',  # grid, random, bayesian optimization
            'metric': {
                'name': 'f1_score',
                'goal': 'maximize'
            },
            'parameters': {
                'learning_rate': {
                    'values': [5e-5, 4e-5, 3e-5]
                },
                'batch_size': {
                    'values': [16, 32, 64, 128]
                },
                'num_train_epochs': {
                'values': [4, 5, 6]
                },
                'optimizer': {
                    # 'values': ["Adam", "AdamW"]
                    'values': ["AdamW"]
                },
                'scheduler': {
                    'values': ["linear_schedule_with_warmup", "cosine_schedule_with_warmup", "constant_schedule", "polynomial_decay_schedule_with_warmup"]
                }
            }
        }
    }
}