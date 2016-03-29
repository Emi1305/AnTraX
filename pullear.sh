for d in `ls -d */`; do cd ./"$d"; git pull; cd ..; done
