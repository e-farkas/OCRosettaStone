# state maching for OCRossetta

S0="welcome"
S1="low_power"
S2="screen_on"
S3="capture_image"
S4="run_obj_det"
S5="show_det_text"
S6="run_translation"
S7="show_translation"
S8="shut_down"

camera_button=true
power_button=false

STATE="$S0"                #initial state

while true; do
    case "$STATE" in
    "$S0")
        echo "welcome state"
        # need if statements here to control state switching
        if [ "$camera_button" = true ] ; then
          STATE="$S1"
        fi
        if [ "$power_button" = true ];
        then
          STATE="$S8"
        fi
        ;;
    "$S1")
        echo "$S1"
        # need if statements here to control state switching
        if [ "$camera_button" = true ] ;
        then
          STATE="$S2"
        fi
        if [ "$power_button" = true ] ;
        then
          STATE="$S8"
        fi
        ;;
    "$S2")
        echo "$S2"
        # need if statements here to control state switching
        if [ "$camera_button" = true ] ;
        then
          STATE="$S3"
        fi
        if [ "$power_button" = true ] ;
        then
          STATE="$S8"
        fi
        ;;
    "$S3")
        echo "$S3"
        # here we capture the image and save it to a folder 
        echo "Running cpp file and output to stdout"
        ./helloWorld < 1
        STATE="$S4"
        ;;
    "$S4")
        echo "$S4"
        # run the object detection
        STATE="$S5"
        ;;
    "$S5")
        echo "Show the detected text on the LCD"
        # need if statements here to control state switching
        if [ "$camera_button" = true ] ;
        then
          STATE="$S6"
        fi
        if [ "$power_button" = true ] ;
        then
          STATE="$S8"
        fi
        ;;
    "$S6")
        echo "run the translation model"
        STATE="$S7"
        ;;
    "$S7")
        echo "display the translation on the LCD" 
        camera_button=false
        power_button=true
        # need if statements here to control state switching
        if [ "$camera_button" = true ] ;
        then
          STATE="$S2"
        fi
        if [ "$power_button" = true ] ;
        then
          STATE="$S8"
        fi
        ;;
    "$S8")
        echo "Shutting down"
        # some command to shut down the pi
        break
        ;;
    esac
done
