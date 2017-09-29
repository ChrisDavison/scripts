# shortsha - Generate n characters of a file's sha1 hash

Created a short utility script that I can use cross-platform to easily generate
sha1 hashes of a file.  Useful for checking duplicate files, and easy to add
into unix pipelines without lots of `| cut -f3 | sort |` type shenanigans
