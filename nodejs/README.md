Building bin/node
=================

wget https://nodejs.org/dist/v0.10.38/node-v0.10.38.tar.gz

tar zxvf node-v0.10.38.tar.gz

cd node-v0.10.38

./configure
make -j8


bin/node node-v0.10.38/deps/npm/bin/npm-cli.js install webcast-osx-audio
