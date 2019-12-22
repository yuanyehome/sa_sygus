for file in ./open_tests/*
do
    echo ''
    echo $file
    echo '\033[32mtesting\033[0m'
    time python main.py $file
    echo ''
done