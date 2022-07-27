# thread_idの一覧
thread_ids=`cat test.log | grep "Calculate START" | cut -d " " -f 3 | sed 's/thread-//g' | sort -n | uniq`
# thrad_idごとに処理時間の平均値を出す
echo "thread_id:time"
for thread_id in $thread_ids; do
    echo -n"" $thread_id":"
    cat test.log | grep thread-$thread_id | grep -e "Calculate START" -e "Calculate END" | \
    cut -d " " -f 1,2 | xargs -I DATE sh -c "date -d 'DATE' '+%s'" | \
    awk 'BEGIN{mean=0}
        {
            if (NR%2!=0){ start_time=$1;} \
            else {mean = mean + $1 - start_time}
        } \
        END{print mean}'
done