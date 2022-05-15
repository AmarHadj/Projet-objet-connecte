1 – S’assurer d’avoir assemblé les composant électroniques
2 – Dans un terminal, exécuter les commandes suivantes : 
•	sudo python3 -m pip install --upgrade requests
•	pip3 install azure-iot-device
•	piip3 install mariadb
3 – Ouvrir le fichier Main.py sur le Raspberry pi et l’exécuter
4 – Ajouter les variables d’environnement suivantes : 
•	IotHubConnectionString : HostName=ObjetsConnectesHub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=GyH0kvk7bYcQKlg/A8wIneGPxHEMDITk7YqYUd1PUR0=
•	EventHubConsumerGroup : consumer_group
5 – Ouvrir l’application web dans Visual studio code. Y ouvrir un terminal, s’assurer d’être dans le dossier web-apps-node-iot-hub-data-visualization et exécuter ces commandes : npm install puis npm start
6 – Dans un navigateur web, se rendre sur localhost:3000
