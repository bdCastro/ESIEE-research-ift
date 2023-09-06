# Author: Bruno Luiz Dias Alves de Castro
# @bdCastro
# Version: 1.0
# Date: 2023-06-29

# Description: this script generates a salience map using the sm library, converts the result into a seed file
# with the number of segments sent as parameter, that is used in the ift-demo library to generate a segmentation

# Usage: ./sm-ift.sh <input_file> <number_of_segments> <output_file>

mkdir -p results
mkdir -p tmp

DIR=$(pwd -P)
IMG=${DIR}/$1
K=$2

PREFIX=${IMG%%.*}
SUFIX=${IMG##*/}
IMG_ID=${SUFIX%%.*}

GRAD_FILE=${DIR}/tmp/grad.pgm
SEED_FILE=${DIR}/tmp/seeds.txt
OUT_FILE=${DIR}/results/${IMG_ID}_ws_${K}.ppm

# generate salience map
cd ./sm
linux/bin/pgm2graph ${IMG} 0 /tmp/_1.graph
linux/bin/extinctionvalues /tmp/_1.graph 1 /tmp/sm.graph /tmp/BM.txt
cp /tmp/sm.graph ../tmp/sm.graph

cd ..

python sm-to-seed.py tmp/sm.graph ${K} ${SEED_FILE}

cd ift-demo/demo/gradient
./gradient ${IMG}
mv ${PREFIX}_grad.pgm ${GRAD_FILE}
cd -

# mkdir -p ift-demo/demo/watershed/seeds
# mkdir -p ift-demo/demo/watershed/images
# cp ${SEED_FILE} ift-demo/demo/watershed/seeds
# cp ${IMG} ift-demo/demo/watershed/images
# cp ${GRAD_FILE} ift-demo/demo/watershed/images

cd ift-demo/demo/watershed
./watershed ${IMG} ${GRAD_FILE} ${SEED_FILE}
mv ${PREFIX}_result.ppm ${OUT_FILE}

# rm -d ../tmp