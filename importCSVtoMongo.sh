for entry in *".csv"
do
  echo importing files to mongodb
  mongoimport --host 10.8.2.5 --port 27017 --username "admin" --password "passadmin33" --authenticationDatabase admin -d  P2_WEC -c WEC --type csv --file $entry --headerline
  mv $entry archive/$entry
done
echo "end of import of CSV to mongodb."