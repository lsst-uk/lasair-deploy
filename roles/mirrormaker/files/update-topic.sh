#!/bin/bash
# Update our topic names.
topiclist=(
    #"ztf_$(date -d '2 days ago' +%Y%m%d)_programid1"
    #"ztf_$(date -d yesterday +%Y%m%d)_programid1"
    "ztf_$(date -d today +%Y%m%d)_programid1"
    )

# https://stackoverflow.com/a/11360591
topicstr="${topiclist[@]}"
topicstr=${topicstr// /,}


#
# Stop the MirrorMaker process.
sudo docker-compose \
    --file "${HOME}/mirror-compose.yml" \
    -p mirrormaker \
    down

#
# Update the topic names.
sed -E -i '
    /whitelist/,/]/ {
        /(whitelist|])/ !{
            s/"[^"]*"/"'${topicstr}'"/
            }
        }
    ' mirror-compose.yml

#
# Start the MirrorMaker process.
sudo docker-compose \
    --file "${HOME}/mirror-compose.yml" \
    -p mirrormaker \
    up --detach \
        mirrormaker
