import datasets
import tempfile
import logging
import random
import config
import os
import yaml
import logging
import time

import transformers

logger = logging.getLogger(__name__)
global_config = None

#############################
########## Permissions ##########
#############################
model_name_to_id = {
  "bigger_model_name" : "06ad41e68cd839fb475a0c1a4ee7a3ad398228df01c9396a97788295d5a0f8bb"
}

#############################
########## LOGGING ##########
#############################
def initialize_config_and_logging(existing_config=None):
    global global_config
    global_config = build_config(existing_config)
    setup_logging(global_config)
    logger.debug("Config: " + str(yaml.dump(global_config.as_dict())))
    return global_config

def get_config():
    global global_config
    assert global_config is not None
    return global_config

def build_config(existing_config=None):
    configs = [
        # Using config library
        config.config_from_env(prefix="LLAMA", separator="_", lowercase_keys=True),
    ]

    if existing_config:
        if isinstance(existing_config, dict):
            configs.append(config.config_from_dict(existing_config))
        else:
            configs.append(existing_config)

    config_paths = get_config_paths()

    for path in reversed(config_paths):
        print("Loading builtin config from " + path)
        configs.append(config.config_from_yaml(path, read_from_file=True))

    return config.ConfigurationSet(*configs)

def get_config_paths():
    paths = []

def get_config_paths():
    paths = []

    config_name = "llama_config"
    config_base = "configs"

    base_config_path = os.path.join(config_base, config_name + ".yaml")
    if os.path.exists(base_config_path):
        paths.append(base_config_path)

    local_config_path = os.path.join(config_base, config_name + "_local.yaml")
    if os.path.exists(local_config_path):
        paths.append(local_config_path)

    home = os.path.expanduser("~")
    home_config_path = os.path.join(home, "." + config_name + ".yaml")
    if os.path.exists(home_config_path):
        paths.append(home_config_path)

    return paths

def setup_logging(arguments):
    logging_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    if arguments["verbose"]:
        logging.basicConfig(level=logging.DEBUG, format=logging_format)
    elif arguments["verbose_info"]:
        logging.basicConfig(level=logging.INFO, format=logging_format)
    else:
        logging.basicConfig(level=logging.WARNING, format=logging_format)

    root_logger = logging.getLogger()

    if arguments["verbose"]:
        root_logger.setLevel(logging.DEBUG)
    elif arguments["verbose_info"]:
        root_logger.setLevel(logging.INFO)
    else:
        root_logger.setLevel(logging.WARNING)

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("filelock").setLevel(logging.WARNING)
    logging.getLogger("smart_open").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)


##########################
########## DATA ##########
##########################
# Wrapper for data load, split, tokenize for training
def tokenize_and_split_data(training_config, tokenizer):
  initialized_config = initialize_config_and_logging(training_config)
  dataset_path = initialized_config["datasets"]["path"]
  use_hf = initialized_config["datasets"]["use_hf"]
  print("tokenize", use_hf, dataset_path)
  if use_hf:
    dataset = datasets.load_dataset(dataset_path)
  else:
    dataset = load_dataset(dataset_path, tokenizer)
  train_dataset = dataset["train"]
  test_dataset = dataset["test"]
  return train_dataset, test_dataset

# Tokenize and split data
def load_dataset(dataset_path, tokenizer):
    random.seed(42)
    finetuning_dataset_loaded = datasets.load_dataset("json", data_files=dataset_path, split="train")
    tokenizer.pad_token = tokenizer.eos_token
    max_length = training_config["model"]["max_length"]
    tokenized_dataset = finetuning_dataset_loaded.map(
        get_tokenize_function(tokenizer, max_length), # returns tokenize_function
        batched=True,
        batch_size=1,
        drop_last_batch=True
    )
    tokenized_dataset = tokenized_dataset.with_format("torch")
    split_dataset = tokenized_dataset.train_test_split(test_size=0.1, shuffle=True, seed=123)
    return split_dataset

# Get function for tokenization, based on config parameters
def get_tokenize_function(tokenizer, _max_length):

  def tokenize_function(examples):
    max_length = _max_length

    # Set pad token
    tokenizer.pad_token = tokenizer.eos_token

    if "question" in examples and "answer" in examples:
      text = examples["question"][0] + examples["answer"][0]
    elif "input" in examples and "output" in examples:
      text = examples["input"][0] + examples["output"][0]
    else:
      text = examples["text"][0]

    # Run tokenizer on all the text (the input and the output)
    tokenized_inputs = tokenizer(
        text,

        # Return tensors in a numpy array (other options are pytorch or tf objects)
        return_tensors="np",

        # Padding type is to pad to the longest sequence in the batch (other option is to a certain max length, or no padding)
        padding=True,
    )

    # Calculate max length
    max_length = min(
        tokenized_inputs["input_ids"].shape[1],
        max_length
    )

    if tokenized_inputs["input_ids"].shape[1] > max_length:
        logger.warn(
            f"Truncating input from {tokenized_inputs['input_ids'].shape[1]} to {max_length}"
        )

    tokenizer.truncation_side = "left"

    tokenized_inputs = tokenizer(
        text,
        return_tensors="np",
        truncation=True,
    )

    tokenized_inputs["labels"] = tokenized_inputs["input_ids"]

    return tokenized_inputs
  return tokenize_function


###########################
########## MODEL ##########
###########################

# Load model onto the right device (GPU if available), and load tokenizer
def load_model(training_config, load_base_model=False):
    model_load_path = ""
    model_load_path = training_config["model"]["pretrained_name"]
    logger.debug(f"Loading default model: {model_load_path}")
    model = AutoModelForCausalLM.from_pretrained(model_load_path)
    tokenizer = AutoTokenizer.from_pretrained(model_load_path)

    logger.debug("Copying model to device")

    device_count = torch.cuda.device_count()
    if device_count > 0:
        logger.debug("Select GPU device")
        device = torch.device("cuda")
    else:
        logger.debug("Select CPU device")
        device = torch.device("cpu")

    model.to(device)

    logger.debug("Copying finished...")
    if "model_name" not in training_config:
        model_name = model_load_path
    else:
        model_name = training_config["model_name"]

    return model, tokenizer, device, model_name

# Trainer class to include logging and history
class Trainer(transformers.Trainer):
    def __init__(
        self,
        model,
        model_flops,
        total_steps,
        args=None,
        data_collator=None,
        train_dataset=None,
        eval_dataset=None,
        tokenizer=None,
        model_init=None,
        compute_metrics=None,
        callbacks=None,
        optimizers=(None, None),
    ):
        super(Trainer, self).__init__(
            model,
            args,
            data_collator,
            train_dataset,
            eval_dataset,
            tokenizer,
            model_init,
            compute_metrics,
            callbacks,
            optimizers,
        )

        self.total_steps = total_steps
        self.model_flops = model_flops
        self.start_step = 0

    def training_step(self, model, inputs):
        if inputs["input_ids"].numel() == 0:

          print("Inputs: ", inputs)
          print("Inputs - input_ids", inputs["input_ids"])
          print("numel", inputs["input_ids"].numel())

          return torch.tensor(0)
        else:
          model.train()
          inputs = self._prepare_inputs(inputs)

          with self.compute_loss_context_manager():
              loss = self.compute_loss(model, inputs)

          if self.args.n_gpu > 1:
              loss = loss.mean()  # mean() to average on multi-gpu parallel training

          if self.do_grad_scaling:
              self.scaler.scale(loss).backward()
          else:
              self.accelerator.backward(loss)

          return loss.detach() / self.args.gradient_accumulation_steps

    def log(self, logs):
        """
        Log `logs` on the various objects watching training.
        Subclass and override this method to inject custom behavior.
        Args:
            logs (`Dict[str, float]`):
                The values to log.
        """
        if self.state.epoch is not None:
            logs["epoch"] = round(self.state.epoch, 2)

        self.update_log_timing(logs)

        output = {**logs, **{"step": self.state.global_step}}
        self.update_history(output)

        logger.debug("Step (" + str(self.state.global_step) + ") Logs: " + str(logs))
        self.control = self.callback_handler.on_log(
            self.args, self.state, self.control, logs
        )

    def update_log_timing(self, logs):
        if len(self.state.log_history) == 0:
            self.start_time = time.time()
            logs["iter_time"] = 0.0
            logs["flops"] = 0.0
            logs["remaining_time"] = 0.0
            self.start_step = self.state.global_step
        elif self.state.global_step > self.start_step:
            logs["iter_time"] = (time.time() - self.start_time) / (
                self.state.global_step - self.start_step
            )
            logs["flops"] = self.model_flops / logs["iter_time"]
            logs["remaining_time"] = (self.total_steps - self.state.global_step) * logs[
                "iter_time"
            ]

    def update_history(self, output):
        if "eval_loss" in output:
            return
        if len(self.state.log_history) > 0:
            smoothing_window = 100
            p = 1.0 / smoothing_window
            if "loss" in output:
                output["loss"] = output["loss"] * p + self.state.log_history[-1][
                    "loss"
                ] * (1.0 - p)
        self.state.log_history.append(output)


def sample_history(history):
    if not history:
        return history
    step = (len(history) + 99) // 100

    return history[0 : len(history) : step]

# Copy file
def smart_copy(remote_path, local_path):
    with open(remote_path, "wb") as remote_file:
        with open(local_path, "rb") as local_file:
            remote_file.write(local_file.read())