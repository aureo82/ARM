
# Script to add date & timestamp to lower left hand corner of a jpeg image
# (where the date and timestamp is obtained from EXIF data if available)

# First (and only) argument is the name of the file, and the output is in
# a file whose name is derived from the original name, in a test folder

#scp root@ip:photo_folder/* . #uncomment to retrieve data from a remote system

mkdir -p temp

for file in *.jpg
	do
	#TEXT=$(exif -mt "Date and Time" $file) #That is if you have exif data
	#[ -z "$TEXT" ] && exit 1
	#TEXT=$(stat "$file" --printf=%y) #That gives data of creation
	TEXT=$(basename "$file" ".jpg")
	Year=${TEXT:0:4}
	Month=${TEXT:4:2}
	Day=${TEXT:6:2}
	Hour=${TEXT:9:2}
	Minute=${TEXT:12:2}
	Second=${TEXT:15:2}
	STAMP="${Hour}:${Minute}:${Second}    ${Day}/${Month}/${Year}"
	OUTPUT="$(basename "$file" ".jpg").jpg"
	convert $file -fill white -undercolor '#00000080' -gravity South -annotate +0+5 "$STAMP" temp/"$OUTPUT"
	done

ls -1tr temp/*.jpg>files.txt

mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4 -o cam_out.avi -mf type=jpeg:fps=20 mf://@files.txt #uncomment to create timelapse

#remove temporal files
rm *.jpg
rm files.txt
rm -r temp