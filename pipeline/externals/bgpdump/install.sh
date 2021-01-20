sudo apt-get install autoconf
sudo apt-get install -y libbz2-dev
sh ./bootstrap.sh
make
./bgpdump -T
