systemctl stop hermesd

rm -rf /etc/hermesd/
rm -rf /hermesd/
rm /lib/systemd/system/hermesd.service

systemctl daemon-reload