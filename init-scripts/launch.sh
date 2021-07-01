chmod -R a+rwx /data/mysql/
cd mysql
./start.sh
docker run -d -p 80:5000 oabuoun/web-calculator
