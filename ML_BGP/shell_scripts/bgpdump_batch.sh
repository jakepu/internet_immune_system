for f in update*
do
    ~/Downloads/bgpdump/bgpdump -m -u $f >> ./merged.txt
done