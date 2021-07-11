# De-interlacing and color correcting badly captured analog video

## Step 1: take a couple of screenshots from the video
At this point the video is already digitized.
Take a handful of video screenshots
Using VLC Media Player, you can choose *Video > Take Snapshot* from the main menu.  Images are saved in your home folder's Picture folder.

## Step 2: adjust colors with GIMP Color Curves and export curves to file
Choose *Colors > Curves* from the main menu in GIMP, change the curves until you are happy (you can save them using the + button), and export as *gimp-curve.txt*, as follows:

![export GIMP color curves](https://github.com/bjaan/[reponame]/blob/curve2ffmpeg/image.jpg?raw=true)

Example file: *vhs-gimp-curves.txt*

## Step 3: curve2ffmpeg - convert GIMP color curves to FFMPEG color curves

Convert a GIMP curve into FFMPEG curve code

Orginal author is **NapoleonWils0n**, their project is over here https://github.com/NapoleonWils0n/curve2ffmpeg, who also uploaded the following [YouTube Video](https://youtu.be/s4xL0msZYuY) on how to do this process.

This script was slightly modified to allow it to write the output file to the same folder and directly as a Python script, without the need of an installation.

usage:

```shell
python curve2ffmpeg.py -i gimp-curve.txt
```

This save the converted FFMPEG curves as `gimp-curve-ffmpeg.txt`.

Example file: *vhs-gimp-curves-ffmpeg.txt*

## Step 4: reduce resolution to typical orginal video resolution, run de-interlace, color correction, re-encoding through FFMPEG

### Step 4.1 video filtering parameters for FFMPEG
As the video-filtering parameters tend to get long, these are stored in a separate file.

Create a new file with the `.filters` file name extension:

Start with:
```
scale=640x480
,setsar=1:1
,yadif
,crop=622:480:0:0
,
```
and put contents of the FFMPEG curve file, created in the previous step and which starts with `curves=master=`, after it.

The example line `,crop=622:480:0:0` can be left off when you don't need to additionally crop the video.  Parameters are `width:height:leftX:topY`.

Example file: *vhs.filters*

## Step 4.2 run FFMPEG

Run the following command to start the conversion:

`ffmpeg -i "analog_video_file_input.webm" -filter_script:v vhs.filters -pix_fmt yuv420p -c:v libx264 -profile:v high -level 4.2 -preset veryslow -crf 19 -c:a aac -b:a 256k "analog_video_file_output.mp4"`

Example parameters:
* `analog_video_file_input.webm` - input video file - any format that FFMPEG supports
* `vhs.filters` - video-filtering parameters file, created in *step 4.1*
* `analog_video_file_output.mp4` - output video file - preferable `.mp4` or `.mkv`

`-pix_fmt yuv420p` is needed as the color correction algorithm changes the pixel format.