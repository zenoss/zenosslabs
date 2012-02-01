#!/bin/bash
ls -1 ./roles | xargs -n1 knife role from file

