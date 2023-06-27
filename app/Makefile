test:
	clear
	sh ../install.sh > /dev/null 2>&1
	sh ../remove.sh > /dev/null 2>&1
	python3 -m unittest -v tests/test-service.py
	sh ../install.sh
	python3 -m unittest -v tests/test-install.py
	systemctl start hermesd
	sleep 10 > /dev/null 2>&1
	python3 -m unittest -v tests/test-dashboard.py
	systemctl restart hermesd
	python3 -m unittest -v tests/test-file.py
	systemctl stop hermesd
	sh ../remove.sh > /dev/null 2>&1
	python3 -m unittest -v tests/test-remove.py
