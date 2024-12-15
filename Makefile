.PHONY: generate_dataset, get_model, train, inference

PARSER_DIR = app/parser
SRC_DIR = app/src

generate_dataset:
	@cd ${PARSER_DIR} && python generate_dataset.py

get_model:
	@cd ${SRC_DIR} && python get_model.py

train:
	@cd ${SRC_DIR} && python train.py

inference:
	@cd ${SRC_DIR} && python inference.py