#!/bin/sh

install_path=/usr/local/bin
link_folder=/usr/local/bin
git_url="https://github.com/sp3t3rs/banglecli/"

git clone $git_url $install_path/banglecli/

# Install Python 3 requirements
pip3 install -r $install_path/banglecli/requirements.txt

# Allow bluepy to use BLE without running as root
find /usr/local/lib/ -name "bluepy-helper" -exec setcap 'cap_net_raw,cap_net_admin+eip' {} \;

# link script file to folder (that's in path )
# so that they can be executed directly
for file in $install_path/banglecli/apps/*
do
  chmod o+x $file 
  link_name=${file##*/}
  link_name=${link_name%.*}
  ln -fs $file $link_folder/$link_name
done

