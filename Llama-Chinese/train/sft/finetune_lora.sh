output_model=my_model_alpha16
# 需要修改到自己的输入目录
if [ ! -d ${output_model} ];then  
    mkdir ${output_model}
fi
export CUDA_HOME=/usr/local/cuda-12.2/
export NCCL_P2P_DISABLE=1
cp ./finetune.sh ${output_model}
deepspeed  finetune_clm_lora.py \
    --model_name_or_path ../../../Atom-7B-Chat \
    --train_files ../../data/train.csv \
    --validation_files  ../../data/val.csv \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --do_train \
    --do_eval \
    --use_fast_tokenizer false \
    --output_dir ${output_model} \
    --evaluation_strategy  steps \
    --max_eval_samples 400 \
    --learning_rate 1e-4 \
    --gradient_accumulation_steps 8 \
    --num_train_epochs 2 \
    --warmup_steps 400 \
    --load_in_bits 4 \
    --lora_r 8 \
    --lora_alpha 16 \
    --target_modules q_proj,k_proj,v_proj,o_proj,down_proj,gate_proj,up_proj \
    --logging_dir ${output_model}/logs \
    --logging_strategy steps \
    --logging_steps 10 \
    --save_strategy steps \
    --preprocessing_num_workers 10 \
    --save_steps 20 \
    --eval_steps 20 \
    --save_total_limit 2000 \
    --seed 80 \
    --disable_tqdm false \
    --ddp_find_unused_parameters false \
    --block_size 2048 \
    --report_to tensorboard \
    --overwrite_output_dir \
    --deepspeed ds_config_zero2.json \
    --ignore_data_skip true \
    --gradient_checkpointing \
    --ddp_timeout 18000000 \
    | tee -a ${output_model}/train.log
    


#    --resume_from_checkpoint my_model/checkpoint-100 \
    # --resume_from_checkpoint ${output_model}/checkpoint-20400 \
