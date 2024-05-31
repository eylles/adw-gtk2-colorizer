# adw-gtk2

![screenshot 1](screenshot1.png)
![screenshot 2](screenshot2.png)

## installation

make sure you got the murrine engine installed as that is the base for this theme.

for example on debian and derivates running the following command will suffice:

```sh
sudo apt install gtk2-engines-murrine
```


then just run make install


if your adw-gtk3 and adw-gtk3-dark themes are located in `~/.local/share/themes/` then install as:

```sh
make install INSTALL_DIR=~/.local/share/themes
```
