#!/bin/bash
cd /var/www/
sudo rm -rf mazepuzzlebox.old/
sudo mv mazepuzzlebox/ mazepuzzlebox.old
sudo tar -xzf /tmp/mpb.tar.gz 
sudo chown www-data:www-data -R mazepuzzlebox
sudo cp mazepuzzlebox.old/mazepuzzlebox/mpb.db mazepuzzlebox/mazepuzzlebox/
sudo vim mazepuzzlebox/mazepuzzlebox/settings.py
sudo /etc/init.d/apache2 restart
