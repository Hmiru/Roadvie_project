#LaMa 사용법 in Window
set TORCH_HOME=%cd%
set PYTHONPATH=%cd%
python bin/predict.py model.path=%cd%/big-lama indir=%cd%/data/input outdir=%cd%/data/output
