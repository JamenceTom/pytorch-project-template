import os

import torch
from config.cfg import Cfg
from torch.backends import cudnn

from utils.logger import setup_logger
from datasets import make_dataloader
from model import make_model
from solver import make_optimizer, WarmupMultiStepLR
from loss import make_loss

from processor import do_train


if __name__ == '__main__':

    Cfg.freeze()
    log_dir = Cfg.DATALOADER.LOG_DIR
    logger = setup_logger('pytorch-template', log_dir)
    logger.info("Running with config:\n{}".format(Cfg))

    os.environ['CUDA_VISIBLE_DEVICES'] = Cfg.MODEL.DEVICE_ID
    cudnn.benchmark = True
    # This flag allows you to enable the inbuilt cudnn auto-tuner to find the best algorithm to use for your hardware.

    train_loader, val_loader = make_dataloader(Cfg)
    model = make_model(Cfg)

    optimizer = make_optimizer(Cfg, model)
    scheduler = WarmupMultiStepLR(optimizer, Cfg.SOLVER.STEPS, Cfg.SOLVER.GAMMA,
                                  Cfg.SOLVER.WARMUP_FACTOR,
                                  Cfg.SOLVER.WARMUP_ITERS, Cfg.SOLVER.WARMUP_METHOD)
    loss_func = make_loss(Cfg)
    do_train(
            Cfg,
            model,
            train_loader,
            val_loader,
            optimizer,
            scheduler,  # modify for using self trained model
            loss_func,
        )
