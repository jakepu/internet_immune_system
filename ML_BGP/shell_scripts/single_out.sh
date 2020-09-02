for f in update*
do
    ~/Downloads/bgpdump/bgpdump -m -u $f > ./results/$f.txt
done