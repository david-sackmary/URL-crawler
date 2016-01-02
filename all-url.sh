# Combine all CSV of URL in working directory into one unique sorted list
cat *.csv > all.csv
sort all.csv -o all_sorted.csv
uniq -c all_sorted.csv all_uniq.csv
