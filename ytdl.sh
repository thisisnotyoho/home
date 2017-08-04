while read line
    do
    youtube-dl -x --audio-format mp3 --audio-quality 1 -f bestaudio --add-metadata -i --yes-playlist "$line"
done

