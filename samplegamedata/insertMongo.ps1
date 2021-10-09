$files = Get-ChildItem .
foreach ($f in $files) {
  if ($f -Like "*.csv") {
    mongoimport -d wec -c gamedata --type csv --file $f --headerline
    Move-Item -Path $f -Destination archive\$f
  }
}