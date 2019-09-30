
#!/bin/bash

set -e

echo "Creating output directory $OUT_DIR..."
mkdir --parent $OUT_DIR

[ -f cv.tex ] || break

echo "Substituting version number ${GITHUB_SHA::7} in file cv.tex..."
sed -i -e "s/verSubstitution/${GITHUB_SHA::7}/" cv.tex

echo "Converting file cv.tex to pdf..."
xelatex cv.tex

cp *.pdf $OUT_DIR 2>/dev/null || :
