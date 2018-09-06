#! /usr/bin/env sh

direc=$1
out='/Volumes/cidcom_moo1/pbeef/trial-longitudinal/raw-collars/'
nodata=$out"nodata.md"
id=`shSDcardID "$direc"`
echo -n $direc" has ID "$id
outdir=$out$id


echo "Do you wish to move to "$outdir" ?"
select yn in "Yes" "No"; do
    case $yn in
        Yes )
        #   mkdir $outdir
          cp -r -v "$direc" "$outdir"
          break;;
        No )
          read -e -p "Name with no data: " test
          echo "- "$test >> $nodata
          exit;;
    esac
done
