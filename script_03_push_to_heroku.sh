cd barb-iot-temp
git add ./data/interim && \
git add -u && \
git commit -m "autoCommit_data" && \
git push heroku master
cd ..
