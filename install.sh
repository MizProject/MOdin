#!/bin/bash

echo "MOdin - Alpha Version"
echo "Powered with Python + PyQt6 + odin4 (official leaked binary from samsung)\n"
echo "Note that the odin4 is rumored to be as a ci build internally so there wont be any new changes on the binary"

while true; do
    read -p "Are you sure to install MOdin? [y/n]: "  ans
    case $ans in
        y|Y ) 
            echo "Installing MOdin..."
            if [ "$(cat /etc/os-release | grep -m 1 -o 'Arch Linux')" ]; then
                STR="Arch Linux"
            elif [ "$(cat /etc/os-release | grep -m 1 -o 'Debian GNU/Linux')" ]; then
                STR="Debian GNU/Linux"
            else
                STR="generic"
            fi
            case $STR in
                "Arch Linux")
                    echo "Arch Detected, installing"
                    sudo pacman -S --noconfirm python python-pyqt6 python-pyusb
                    if [ -e "/usr/bin/paru" ]; then
                        paru -S --noconfirm odin4-cli
                    elif [ -e "/usr/bin/yay" ]; then
                        sudo yay -S odin4-cli 
                    else 
                        echo "Why arent you installing yay or paru bruh"
                        if [ -e "/usr/bin/git"  ]; then
                            git clone http://aur.archlinux.org/odin4-cli
                            cd odin4-cli
                            if [ -e "/usr/bin/makepkg" ]; then
                                makepkg -si
                            else
                                echo "This system is hopeless"
                                echo "Exit: reason: using arch but too many missing dependencies holy shid"
                                exit 1
                            fi
                        else
                            echo "why no git?"
                            exit 1
                        fi
                    fi
                    sudo cp variants/modin/main.py /usr/bin/modin
                    echo "MOdin is ready"
                    break
                    ;;
                "Debian GNU/Linux")
                    echo "Debian GNU/Linux found"
                    echo "Installing dependencies"
                    sudo apt update
                    sudo apt upgrade -y
                    sudo apt install python3 python3-pip python3-usb* python3-pyqt6* -y
                    echo "Downloading Odin4"
                    if [ -e "/usr/bin/aria2c" ]; then
                        aria2c -x 10 "https://mizproject.github.io/mizrepo/bin/amd64/samsung/flash/odin4.deb"
                        sudo apt install -y ./odin4.deb
                        if [ -e "/usr/bin/odin4" ] && [ -e "/etc/udev/rules.d/51-android.rules" ] ; then
                            echo "Installed odin4 via apt"
                        else 
                            echo "Failed to install odin4, aborting"
                            exit 1
                        fi
                    elif [ -e "/usr/bin/wget" ]; then 
                        wget "https://mizproject.github.io/mizrepo/bin/amd64/samsung/flash/odin4.deb"
                        sudo apt install -y ./odin4.deb
                        if [ -e "/usr/bin/odin4" ] && [ -e "/etc/udev/rules.d/51-android.rules" ] ; then
                            echo "Installed odin4 via apt"
                        else
                            echo "Failed to install odin4, aborting"
                            exit 1
                        fi
                    elif [ -e "/usr/bin/curl" ]; then 
                        curl "https://mizproject.github.io/mizrepo/bin/amd64/samsung/flash/odin4.deb" > odin4.deb
                        sudo apt install -y ./odin4.deb
                        if [ -e "/usr/bin/odin4" ] && [ -e "/etc/udev/rules.d/51-android.rules" ] ; then
                            echo "Installed odin4 via apt"
                        else
                            echo "Failed to install odin4, aborting"
                            exit 1
                        fi
                    else
                        echo "Could not find a download tool"
                        echo "Aborting"
                        exit 1
                    fi
                    sudo cp variants/modin/main.py /usr/bin/modin
                    echo "MOdin is ready"
                    break
                    ;;
                "generic")
                    echo "Could not determine the distro\n\nSadly for now , this script only supports Ubuntu, Debian GNU/Linux and Arch Linux"
                    echo "Aborting"
                    exit 1
                    break
                    ;;
            esac
            ;;
        N|n )
            echo "Abort"
            exit 1
            break
            ;;
    esac
done

echo -e "REMEBER\n\n\n\nPlease run modin to the terminal to run modin"  