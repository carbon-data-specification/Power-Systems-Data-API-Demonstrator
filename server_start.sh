#!/bin/sh
python power_systems_data_api_demonstrator/seed/seed.py && uvicorn power_systems_data_api_demonstrator.src.application:get_app --host 0.0.0.0 --port 10000
