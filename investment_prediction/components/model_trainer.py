


class ModelTrainer:
        logging.info("Flatten input (to support multivariate input)")
        combined_train_X = utils.flattern_input(combined_train_X)
        combined_test_X = utils.flattern_input(combined_test_X)